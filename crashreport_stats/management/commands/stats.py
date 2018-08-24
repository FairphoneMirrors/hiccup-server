"""Manage Hiccup stats.

This module provides a command to compute statistics of
heartbeats, crashes, and versions sent from Hiccup clients.
"""
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, F, Q
from django.db.models.functions import TruncDate
import pytz

from crashreport_stats.models import (
    RadioVersion,
    RadioVersionDaily,
    StatsMetadata,
    Version,
    VersionDaily,
)
from crashreports.models import Crashreport, HeartBeat


# pylint: disable=too-few-public-methods
# Classes in this file inherit from each other and are not method containers.


class _ReportCounterFilter:
    """Filter reports matching a report counter requirements.

    Attributes:
        model (django.db.model): The report model.
        name (str): The human-readable report counter name.
        field_name (str): The counter name as defined in the stats model where
            it is a field.

    """

    def __init__(self, model, name, field_name):
        """Initialise the filter.

        Args:
            model (django.db.model): The report model.
            name (str): The human-readable report counter name.
            field_name (str): The counter name as defined in the stats model
                where it is a field.

        """
        self.model = model
        self.name = name
        self.field_name = field_name

    def filter(self, query_objects):
        """Filter the reports.

        Args:
            query_objects (QuerySet): The reports to filter.
        Returns:
            QuerySet: The reports matching this report counter requirements.

        """
        # pylint: disable=no-self-use
        # self is potentially used by subclasses.
        return query_objects


class HeartBeatCounterFilter(_ReportCounterFilter):
    """The heartbeats counter filter."""

    def __init__(self):
        """Initialise the filter."""
        super(HeartBeatCounterFilter, self).__init__(
            model=HeartBeat, name="heartbeats", field_name="heartbeats"
        )


class CrashreportCounterFilter(_ReportCounterFilter):
    """The crashreports counter filter.

    Attributes:
        include_boot_reasons (list(str)): The boot reasons assumed to
            characterise this crashreport ("OR"ed).
        exclude_boot_reasons (list(str)): The boot reasons assumed to *not*
            characterise this crashreport ("AND"ed).
        inclusive_filter (Q): The boot reasons filter for filtering reports
            that should be included.
        exclusive_filter (Q): The boot reasons filter for filtering reports
            that should *not* be included.

    """

    def __init__(
        self,
        name,
        field_name,
        include_boot_reasons=None,
        exclude_boot_reasons=None,
    ):
        """Initialise the filter.

        One or both of `include_boot_reasons` and `exclude_boot_reasons` must
        be specified.

        Args:
            name (str): The human-readable report counter name.
            field_name (str):
                The counter name as defined in the stats model where it is a
                field.
            include_boot_reasons (list(str), optional):
                The boot reasons assumed to characterise this crashreport
                ("OR"ed).
            exclude_boot_reasons (list(str), optional):
                The boot reasons assumed to *not* characterise this
                crashreport ("AND"ed).
        Raises:
            ValueError:
                None of `include_boot_reasons` and `exclude_boot_reasons` have
                been supplied.

        """
        if not include_boot_reasons and not exclude_boot_reasons:
            raise ValueError(
                "One or both of `include_boot_reasons` and "
                "`exclude_boot_reasons` must be specified."
            )

        super(CrashreportCounterFilter, self).__init__(
            model=Crashreport, name=name, field_name=field_name
        )

        # Cache the boot reasons inclusive filter
        self.include_boot_reasons = include_boot_reasons
        self.inclusive_filter = self._create_query_filter(include_boot_reasons)

        # Cache the boot reasons exclusive filter
        self.exclude_boot_reasons = exclude_boot_reasons
        self.exclusive_filter = self._create_query_filter(exclude_boot_reasons)

    @staticmethod
    def _create_query_filter(reasons):
        """Combine boot reasons into one filter.

        Args:
            reasons (list(str)): List of boot reasons to include in filter.
        Returns:
            django.db.models.query_utils.Q: Query that matches either of
                reasons as boot_reason if list is not empty, otherwise None.

        """
        if not reasons:
            return None

        query = Q(boot_reason=reasons[0])
        for reason in reasons[1:]:
            query = query | Q(boot_reason=reason)
        return query

    def filter(self, query_objects):
        """Filter the reports according to the inclusive and exclusive fitlers.

        Args:
            query_objects (QuerySet): The reports to filter.
        Returns:
            QuerySet: The reports matching this report counter requirements.

        """
        if self.inclusive_filter:
            query_objects = query_objects.filter(self.inclusive_filter)
        if self.exclusive_filter:
            query_objects = query_objects.exclude(self.exclusive_filter)

        return query_objects


class _StatsModelsEngine:
    """Stats models engine.

    An engine to update general stats (_VersionStats) and their daily
    counterparts (_DailyVersionStats).
    """

    def __init__(self, stats_model, daily_stats_model, version_field_name):
        """Initialise the engine.

        Args:
            stats_model (_VersionStats): The _VersionStats model to update
                stats for.
            daily_stats_model (_DailyVersionStats): The _DailyVersionStats
                model to update stats for.
            version_field_name (str): The version field name as specified in
                the stats models.

        """
        self.stats_model = stats_model
        self.daily_stats_model = daily_stats_model
        self.version_field_name = version_field_name

    def _valid_objects(self, query_objects):
        """Filter out invalid reports.

        Returns:
            QuerySet: All the valid reports.

        """
        # pylint: disable=no-self-use
        # self is potentially used by subclasses.
        return query_objects

    def _objects_within_period(self, query_objects, up_to, starting_from=None):
        """Retrieve the reports within a specific period of time.

        The objects are filtered considering a specific period of time to allow
        for comparable results between subclasses. The lower bound should be
        omitted for the first update but always set for later calls. The upper
        bound must be specified to avoid race conditions.

        Args:
            query_objects (QuerySet): The reports to filter.
            up_to (datetime): The maximum timestamp to consider (inclusive).
            starting_from (datetime, optional): The minimum timestamp to
                consider (exclusive).
        Returns:
            QuerySet: The reports received within a specific period of time.

        """
        # pylint: disable=no-self-use
        # self might be used by subclasses.
        query_objects = query_objects.filter(created_at__lte=up_to)
        if starting_from:
            query_objects = query_objects.filter(created_at__gt=starting_from)

        return query_objects

    def _unique_objects_per_day(self, query_objects):
        """Count the unique reports per version per day.

        Args:
            query_objects (QuerySet): The reports to count.
        Returns:
            QuerySet: The unique reports grouped per version per day.

        """
        return (
            query_objects.annotate(_report_day=TruncDate("date")).values(
                self.version_field_name, "_report_day"
            )
            # FIXME Agressively drop duplicates
            .annotate(count=Count("date", distinct=True))
        )

    def delete_stats(self):
        """Delete the general and daily stats instances.

        Returns:
            dict(str, int): The count of deleted entries per model name.

        """
        # Clear the general stats, the daily stats will be deleted by cascading
        # effect
        _, count_per_model = self.stats_model.objects.all().delete()
        return count_per_model

    def update_stats(self, report_counter, up_to, starting_from=None):
        """Update the statistics of the general and daily stats entries.

        The algorithm works as follow:
        1. The reports are filtered considering a specific period of time to
            allow for comparable results between subclasses. The lower bound
            should be omitted for the first update but always set for later
            calls. The upper bound must be specified to avoid race conditions.
        2. The report counter requirements are applied to the reports.
        3. The reports are grouped per day and per version, a counter is
            generated.
        4. Each report group count is used to update specific daily stats,
            while the sum of them per version updates the general stats.

        Args:
            report_counter (_ReportCounterEngine): The report counter to
                update the stats with.
            up_to (datetime): The maximum timestamp to consider (inclusive).
            starting_from (datetime, optional): The minimum timestamp to
                consider (exclusive).
        Returns:
            dict(str, dict(str, int)): The number of added entries and the
                number of updated entries bundled in a dict, respectively
                hashed with the keys 'created' and 'updated', per model name.

        """
        counts_per_model = {
            self.stats_model: {"created": 0, "updated": 0},
            self.daily_stats_model: {"created": 0, "updated": 0},
        }

        query_objects = self._valid_objects(report_counter.model.objects.all())
        # Only include reports from the interesting period of time
        query_objects = self._objects_within_period(
            query_objects, up_to, starting_from
        )
        # Apply the report counter requirements
        query_objects = report_counter.filter(query_objects)
        # Chain our own filters
        query_objects = self._unique_objects_per_day(query_objects)

        # Explicitly use the iterator() method to avoid caching as we will
        # not re-use the QuerySet
        for query_object in query_objects.iterator():
            report_day = query_object["_report_day"]
            # Use a dict to be able to dereference the field name
            stats, created = self.stats_model.objects.get_or_create(
                **{
                    self.version_field_name: query_object[
                        self.version_field_name
                    ],
                    "defaults": {
                        "first_seen_on": report_day,
                        "released_on": report_day,
                    },
                }
            )
            counts_per_model[self.stats_model][
                ("created" if created else "updated")
            ] += 1

            # Reports are coming in an unordered manner, a late report can
            # be older (device time wise). Make sure that the current reports
            # creation date is taken into account in the version history.
            if not created and stats.first_seen_on > report_day:
                # Avoid changing the released_on field if it is different than
                # the default value (i.e. equals to the value of first_seen_on)
                # since it indicates that it was manually changed.
                if stats.released_on == stats.first_seen_on:
                    stats.released_on = report_day
                stats.first_seen_on = report_day

            daily_stats, created = self.daily_stats_model.objects.get_or_create(
                version=stats, date=report_day
            )
            counts_per_model[self.daily_stats_model][
                ("created" if created else "updated")
            ] += 1

            setattr(
                stats,
                report_counter.field_name,
                F(report_counter.field_name) + query_object["count"],
            )
            setattr(
                daily_stats,
                report_counter.field_name,
                F(report_counter.field_name) + query_object["count"],
            )

            stats.save()
            daily_stats.save()

        return counts_per_model


class VersionStatsEngine(_StatsModelsEngine):
    """Version stats engine.

    An engine to update a counter of general stats (Version) and their daily
    counterparts (VersionDaily).
    """

    def __init__(self):
        """Initialise the engine."""
        super(VersionStatsEngine, self).__init__(
            stats_model=Version,
            daily_stats_model=VersionDaily,
            version_field_name="build_fingerprint",
        )


class RadioVersionStatsEngine(_StatsModelsEngine):
    """Radio version stats engine.

    An engine to update a counter of general stats (RadioVersion) and their
    daily counterparts (RadioVersionDaily).
    """

    def __init__(self):
        """Initialise the engine."""
        super(RadioVersionStatsEngine, self).__init__(
            stats_model=RadioVersion,
            daily_stats_model=RadioVersionDaily,
            version_field_name="radio_version",
        )

    def _valid_objects(self, query_objects):
        # For legacy reasons, the version field might be null
        return query_objects.filter(radio_version__isnull=False)


class Command(BaseCommand):
    """Management command to compute Hiccup statistics."""

    _STATS_MODELS_ENGINES = [VersionStatsEngine(), RadioVersionStatsEngine()]

    # All the report counters that are listed in the stats models
    _REPORT_COUNTER_FILTERS = [
        HeartBeatCounterFilter(),
        CrashreportCounterFilter(
            name="crashes",
            field_name="prob_crashes",
            include_boot_reasons=Crashreport.CRASH_BOOT_REASONS,
        ),
        CrashreportCounterFilter(
            name="smpl",
            field_name="smpl",
            include_boot_reasons=Crashreport.SMPL_BOOT_REASONS,
        ),
        CrashreportCounterFilter(
            name="other",
            field_name="other",
            exclude_boot_reasons=(
                Crashreport.SMPL_BOOT_REASONS + Crashreport.CRASH_BOOT_REASONS
            ),
        ),
    ]

    help = __doc__

    def add_arguments(self, parser):
        """Add custom arguments to the command."""
        parser.add_argument("action", choices=["reset", "update"])

    def handle(self, *args, **options):
        """Carry out the command executive logic."""
        # pylint: disable=attribute-defined-outside-init
        # self.debug is only ever read through calls of handle().
        self.debug = int(options["verbosity"]) >= 2

        if options["action"] == "reset":
            self.delete_all_stats()
            self.update_all_stats()
        elif options["action"] == "update":
            self.update_all_stats()

    def _success(self, msg, *args, **kwargs):
        # pylint: disable=no-member
        # Members of Style are generated and cannot be statically inferred.
        self.stdout.write(self.style.SUCCESS(msg), *args, **kwargs)

    def delete_all_stats(self):
        """Delete the statistics from all stats models."""
        with transaction.atomic():
            for engine in self._STATS_MODELS_ENGINES:
                counts_per_model = engine.delete_stats()
                if self.debug:
                    # Default the count of deleted models to 0 if missing
                    if not counts_per_model:
                        counts_per_model = {
                            engine.stats_model._meta.label: 0,
                            engine.daily_stats_model._meta.label: 0,
                        }
                    for model, count in counts_per_model.items():
                        name = model.split(".")[-1]
                        self._success("{} {} deleted".format(count, name))

            # Reset the metadata
            count, _ = StatsMetadata.objects.all().delete()
            if self.debug:
                self._success("{} StatsMetadata deleted".format(count))

    def update_all_stats(self):
        """Update the statistics from all stats models."""
        try:
            previous_update = StatsMetadata.objects.latest("updated_at")
            starting_from = previous_update.updated_at
        except StatsMetadata.DoesNotExist:
            starting_from = None
        # Fix the upper limit to avoid race conditions with new reports sent
        # while we are updating the different statistics
        up_to = datetime.datetime.now(tz=pytz.utc)

        for engine in self._STATS_MODELS_ENGINES:
            with transaction.atomic():
                for filter_ in self._REPORT_COUNTER_FILTERS:
                    counts_per_model = engine.update_stats(
                        filter_, up_to, starting_from
                    )
                    if self.debug:
                        for model, counts in counts_per_model.items():
                            for action, count in counts.items():
                                msg = "{} {} {} for counter {}".format(
                                    count, model.__name__, action, filter_.name
                                )
                                self._success(msg)

        StatsMetadata(updated_at=up_to).save()
