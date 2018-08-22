"""The stats models."""
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
)


class _VersionStats(Model):
    """The base class for all-time stats of a version.

    Sub-classes should be created to gather stats about a versioned
    end-product such as a software build.

    Attributes:
        is_official_release:
            If this version is an official release. Defaults to False.
        is_beta_release: If this version is a beta release. Defaults to False.
        first_seen_on:
            Day this version has been seen for the first time as reported by
            devices (not by the server). Defaults to the current date.
        released_on:
            Day this version has been released on. Defaults to the current date.
        heartbeats: The total heartbeats counted for this version.
        prob_crashes: The total probable crash reports counted for this version.
        smpl: The total SMPL reports counted for this version.
        other: The total of other reports counted for this version.

    """

    is_official_release = BooleanField(default=False)
    is_beta_release = BooleanField(default=False)
    first_seen_on = DateField()
    released_on = DateField()
    heartbeats = IntegerField(default=0)
    prob_crashes = IntegerField(default=0)
    smpl = IntegerField(default=0)
    other = IntegerField(default=0)

    class Meta:
        abstract = True


class _DailyVersionStats(Model):
    """The base class for daily stats of a version.

    Sub-classes MUST define the foreign key `version` pointing back to the
    `_VersionStats` implementation they are gathering stats for.

    Attributes:
        date: Day considered for the stats.
        heartbeats:
            The total heartbeats counted for this version on the day `date`.
        prob_crashes:
            The total probable crash reports counted for this version on the
            day `date`.
        smpl: The total SMPL reports counted for this version on the day `date`.
        other:
            The total of other reports counted for this version on the day
            `date`.

    """

    date = DateField()
    heartbeats = IntegerField(default=0)
    prob_crashes = IntegerField(default=0)
    smpl = IntegerField(default=0)
    other = IntegerField(default=0)

    class Meta:
        abstract = True


class Version(_VersionStats):
    """The all-time stats of a software version.

    Attributes:
        build_fingerprint:
            The software build fingerprint uniquely identifying this version.

    """

    build_fingerprint = CharField(max_length=200, unique=True)

    def __str__(self):  # noqa: D105
        return self.build_fingerprint


class VersionDaily(_DailyVersionStats):
    """The daily stats of a software version.

    Attributes:
        version:
            The software version object (`Version`) these daily stats are about.

    """

    version = ForeignKey(
        Version, db_index=True, related_name="daily_stats", on_delete=CASCADE
    )


class RadioVersion(_VersionStats):
    """The all-time stats of a radio version.

    Attributes:
        radio_version:
            The radio version number uniquely identifying this version.

    """

    radio_version = CharField(max_length=200, unique=True)

    def __str__(self):  # noqa: D105
        return self.radio_version


class RadioVersionDaily(_DailyVersionStats):
    """The daily stats of a radio version.

    Attributes:
        version:
            The radio version object (`RadioVersion`) these daily stats are
            about.

    """

    version = ForeignKey(
        RadioVersion,
        db_index=True,
        related_name="daily_stats",
        on_delete=CASCADE,
    )


class StatsMetadata(Model):
    """The stats metadata.

    Attributes:
        updated_at: The last time the stats were updated.

    """

    updated_at = DateTimeField()
