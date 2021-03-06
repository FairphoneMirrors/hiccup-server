"""Tests for the stats management command module."""
from io import StringIO
from datetime import datetime, timedelta

import pytz

from django.core.management import call_command
from django.test import TestCase

from crashreport_stats.models import (
    Version,
    VersionDaily,
    RadioVersion,
    RadioVersionDaily,
    StatsMetadata,
)
from crashreport_stats.tests.utils import Dummy

from crashreports.models import Crashreport, HeartBeat

# pylint: disable=too-many-public-methods


class StatsCommandVersionsTestCase(TestCase):
    """Test the generation of Version stats with the stats command."""

    # The class of the version type to be tested
    version_class = Version
    # The attribute name characterising the unicity of a stats entry (the
    # named identifier)
    unique_entry_name = "build_fingerprint"
    # The collection of unique entries to post
    unique_entries = Dummy.BUILD_FINGERPRINTS

    def _create_reports(
        self, report_type, unique_entry_name, device, number, **kwargs
    ):
        # Create reports with distinct timestamps
        report_date = datetime.now(pytz.utc)
        if report_type == HeartBeat:
            report_date = report_date.date()
        for i in range(number):
            report_attributes = {
                self.unique_entry_name: unique_entry_name,
                "device": device,
                "date": report_date - timedelta(days=i),
            }
            report_attributes.update(**kwargs)
            Dummy.create_report(report_type, **report_attributes)

    def test_stats_calculation(self):
        """Test generation of a Version instance."""
        user = Dummy.create_user()
        device = Dummy.create_device(user=user)
        heartbeat = Dummy.create_report(HeartBeat, device=device)

        # Expect that we do not have the Version before updating the stats
        get_params = {
            self.unique_entry_name: getattr(heartbeat, self.unique_entry_name)
        }
        self.assertRaises(
            self.version_class.DoesNotExist,
            self.version_class.objects.get,
            **get_params
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Assume that a corresponding Version instance has been created
        version = self.version_class.objects.get(**get_params)
        self.assertIsNotNone(version)

    def _assert_older_report_updates_version_date(self, report_type):
        """Validate that older reports sent later affect the version date."""
        user = Dummy.create_user()
        device = Dummy.create_device(user=user)
        report = Dummy.create_report(report_type, device=device)

        # Run the command to update the database
        call_command("stats", "update")

        get_params = {
            self.unique_entry_name: getattr(report, self.unique_entry_name)
        }
        version = self.version_class.objects.get(**get_params)

        report_date = (
            report.date.date() if report_type == Crashreport else report.date
        )
        self.assertEqual(report_date, version.first_seen_on)

        # Create a new report from an earlier point in time
        report_date_2 = report.date - timedelta(weeks=1)
        Dummy.create_report(report_type, device=device, date=report_date_2)

        # Run the command to update the database
        call_command("stats", "update")

        # Get the same version object from before
        version = self.version_class.objects.get(**get_params)

        # Validate that the date matches the report recently sent
        if report_type == Crashreport:
            report_date_2 = report_date_2.date()
        self.assertEqual(report_date_2, version.first_seen_on)

    def test_older_heartbeat_updates_version_date(self):
        """Validate updating version date with older heartbeats."""
        self._assert_older_report_updates_version_date(HeartBeat)

    def test_older_crash_report_updates_version_date(self):
        """Validate updating version date with older crash reports."""
        self._assert_older_report_updates_version_date(Crashreport)

    def test_entries_are_unique(self):
        """Validate the entries' unicity and value."""
        # Create some reports
        for unique_entry, username in zip(self.unique_entries, Dummy.USERNAMES):
            user = Dummy.create_user(username=username)
            device = Dummy.create_device(user=user)
            self._create_reports(HeartBeat, unique_entry, device, 10)

        # Run the command to update the database
        call_command("stats", "update")

        # Check whether the correct amount of distinct versions have been
        # created
        versions = self.version_class.objects.all()
        for version in versions:
            self.assertIn(
                getattr(version, self.unique_entry_name), self.unique_entries
            )
        self.assertEqual(len(versions), len(self.unique_entries))

    def _assert_counter_distribution_is_correct(
        self, report_type, numbers, counter_attribute_name, **kwargs
    ):
        """Validate a counter distribution in the database."""
        if len(numbers) != len(self.unique_entries):
            raise ValueError(
                "The length of the numbers list must match the "
                "length of self.unique_entries in the test class"
                "({} != {})".format(len(numbers), len(self.unique_entries))
            )
        # Create some reports
        for unique_entry, num, username in zip(
            self.unique_entries, numbers, Dummy.USERNAMES
        ):
            user = Dummy.create_user(username=username)
            device = Dummy.create_device(user=user)
            self._create_reports(
                report_type, unique_entry, device, num, **kwargs
            )

        # Run the command to update the database
        call_command("stats", "update")

        # Check whether the numbers of reports match
        for version in self.version_class.objects.all():
            unique_entry_name = getattr(version, self.unique_entry_name)
            num = numbers[self.unique_entries.index(unique_entry_name)]
            self.assertEqual(num, getattr(version, counter_attribute_name))

    def test_heartbeats_counter(self):
        """Test the calculation of the heartbeats counter."""
        numbers = [10, 7, 8, 5]
        counter_attribute_name = "heartbeats"
        self._assert_counter_distribution_is_correct(
            HeartBeat, numbers, counter_attribute_name
        )

    def test_crash_reports_counter(self):
        """Test the calculation of the crashreports counter."""
        numbers = [2, 5, 0, 3]
        counter_attribute_name = "prob_crashes"
        boot_reason_param = {"boot_reason": Crashreport.BOOT_REASON_UNKOWN}
        self._assert_counter_distribution_is_correct(
            Crashreport, numbers, counter_attribute_name, **boot_reason_param
        )

    def test_smpl_reports_counter(self):
        """Test the calculation of the smpl reports counter."""
        numbers = [1, 3, 4, 0]
        counter_attribute_name = "smpl"
        boot_reason_param = {"boot_reason": Crashreport.BOOT_REASON_RTC_ALARM}
        self._assert_counter_distribution_is_correct(
            Crashreport, numbers, counter_attribute_name, **boot_reason_param
        )

    def test_other_reports_counter(self):
        """Test the calculation of the other reports counter."""
        numbers = [0, 2, 1, 2]
        counter_attribute_name = "other"
        boot_reason_param = {"boot_reason": "random boot reason"}
        self._assert_counter_distribution_is_correct(
            Crashreport, numbers, counter_attribute_name, **boot_reason_param
        )

    def _assert_accumulated_counters_are_correct(
        self, report_type, counter_attribute_name, **kwargs
    ):
        """Validate a counter distribution with reports of different devices."""
        # Create some devices and corresponding reports
        devices = [
            Dummy.create_device(Dummy.create_user(username=name))
            for name in Dummy.USERNAMES
        ]
        num_reports = 5
        for device in devices:
            self._create_reports(
                report_type,
                self.unique_entries[0],
                device,
                num_reports,
                **kwargs
            )

        # Run the command to update the database
        call_command("stats", "update")

        # Check whether the numbers of reports match
        version = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[0]}
        )
        self.assertEqual(
            len(Dummy.USERNAMES) * num_reports,
            getattr(version, counter_attribute_name),
        )

    def test_accumulated_heartbeats_counter(self):
        """Test heartbeats counter with reports from different devices."""
        report_type = HeartBeat
        counter_attribute_name = "heartbeats"
        self._assert_accumulated_counters_are_correct(
            report_type, counter_attribute_name
        )

    def test_accumulated_crash_reports_counter(self):
        """Test crash reports counter with reports from different devices."""
        report_type = Crashreport
        counter_attribute_name = "prob_crashes"
        boot_reason_param = {"boot_reason": Crashreport.CRASH_BOOT_REASONS[0]}
        self._assert_accumulated_counters_are_correct(
            report_type, counter_attribute_name, **boot_reason_param
        )

    def test_accumulated_smpl_reports_counter(self):
        """Test smpl reports counter with reports from different devices."""
        report_type = Crashreport
        counter_attribute_name = "smpl"
        boot_reason_param = {"boot_reason": Crashreport.SMPL_BOOT_REASONS[0]}
        self._assert_accumulated_counters_are_correct(
            report_type, counter_attribute_name, **boot_reason_param
        )

    def test_accumulated_other_reports_counter(self):
        """Test other reports counter with reports from different devices."""
        report_type = Crashreport
        counter_attribute_name = "other"
        boot_reason_param = {"boot_reason": "random boot reason"}
        self._assert_accumulated_counters_are_correct(
            report_type, counter_attribute_name, **boot_reason_param
        )

    def test_reset_deletion_of_unrelated_version(self):
        """Test delete functionality of the reset command."""
        # Create a version instance that is not related to any reports
        Dummy.create_version(
            self.version_class,
            **{self.unique_entry_name: self.unique_entries[0]}
        )

        # Run the command to reset the database
        call_command("stats", "reset")

        # Check whether the unrelated version instance has been deleted
        self.assertFalse(
            self.version_class.objects.filter(
                **{self.unique_entry_name: self.unique_entries[0]}
            ).exists()
        )

    def _assert_reset_updates_counter(
        self, report_type, counter_attribute_name, **kwargs
    ):
        # Create a device and corresponding reports
        device = Dummy.create_device(Dummy.create_user())
        num_reports = 5
        self._create_reports(
            report_type, self.unique_entries[0], device, num_reports, **kwargs
        )

        # Create a version instance with wrong numbers
        wrong_num_of_reports = 4
        Dummy.create_version(
            self.version_class,
            **{
                self.unique_entry_name: self.unique_entries[0],
                counter_attribute_name: wrong_num_of_reports,
            }
        )

        # Run the command to reset the database
        call_command("stats", "reset")

        # Check whether the numbers of reports do match
        version = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[0]}
        )
        self.assertEqual(num_reports, getattr(version, counter_attribute_name))

    def test_reset_update_heartbeat_counter(self):
        """Test update of the heartbeat counter using the reset command."""
        self._assert_reset_updates_counter(HeartBeat, "heartbeats")

    def test_reset_update_crash_report_counter(self):
        """Test update of the crash report counter using the reset command."""
        boot_reason_param = {"boot_reason": Crashreport.CRASH_BOOT_REASONS[0]}
        self._assert_reset_updates_counter(
            Crashreport, "prob_crashes", **boot_reason_param
        )

    def test_reset_update_smpl_report_counter(self):
        """Test update of the smpl report counter using the reset command."""
        boot_reason_param = {"boot_reason": Crashreport.SMPL_BOOT_REASONS[0]}
        self._assert_reset_updates_counter(
            Crashreport, "smpl", **boot_reason_param
        )

    def test_reset_update_other_report_counter(self):
        """Test update of the other report counter using the reset command."""
        boot_reason_param = {"boot_reason": "random boot reason"}
        self._assert_reset_updates_counter(
            Crashreport, "other", **boot_reason_param
        )

    def _assert_updating_twice_gives_correct_counters(
        self, report_type, counter_attribute_name, **boot_reason_param
    ):
        # Create a two devices and a corresponding reports for 2 different
        # versions
        device_1 = Dummy.create_device(Dummy.create_user())
        num_reports = 5
        self._create_reports(
            report_type,
            self.unique_entries[0],
            device_1,
            num_reports,
            **boot_reason_param
        )
        device_2 = Dummy.create_device(
            Dummy.create_user(username=Dummy.USERNAMES[1])
        )
        self._create_reports(
            report_type,
            self.unique_entries[1],
            device_2,
            num_reports,
            **boot_reason_param
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Check whether the numbers of reports match for both versions
        version_1 = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[0]}
        )
        self.assertEqual(
            num_reports, getattr(version_1, counter_attribute_name)
        )
        version_2 = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[1]}
        )
        self.assertEqual(
            num_reports, getattr(version_2, counter_attribute_name)
        )

        # Create another report for the first version
        report_new_attributes = {
            self.unique_entry_name: self.unique_entries[0],
            "device": device_1,
            **boot_reason_param,
        }
        Dummy.create_report(report_type, **report_new_attributes)

        # Run the command to update the database again
        call_command("stats", "update")

        # Check whether the numbers of reports match:
        # Assert that the first version's counter is increased by one
        version_1 = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[0]}
        )
        self.assertEqual(
            num_reports + 1, getattr(version_1, counter_attribute_name)
        )
        # Assert that the second versions counter is unchanged
        version_2 = self.version_class.objects.get(
            **{self.unique_entry_name: self.unique_entries[1]}
        )
        self.assertEqual(
            num_reports, getattr(version_2, counter_attribute_name)
        )

    def test_updating_heartbeats_counter_twice(self):
        """Test updating the heartbeats counter twice."""
        self._assert_updating_twice_gives_correct_counters(
            HeartBeat, "heartbeats"
        )

    def test_updating_crash_reports_counter_twice(self):
        """Test updating the crash reports counter twice."""
        boot_reason_param = {"boot_reason": Crashreport.CRASH_BOOT_REASONS[0]}
        self._assert_updating_twice_gives_correct_counters(
            Crashreport, "prob_crashes", **boot_reason_param
        )

    def test_updating_smpl_reports_counter_twice(self):
        """Test updating the smpl reports counter twice."""
        boot_reason_param = {"boot_reason": Crashreport.SMPL_BOOT_REASONS[0]}
        self._assert_updating_twice_gives_correct_counters(
            Crashreport, "smpl", **boot_reason_param
        )

    def test_updating_other_reports_counter_twice(self):
        """Test updating the other reports counter twice."""
        boot_reason_param = {"boot_reason": "random boot reason"}
        self._assert_updating_twice_gives_correct_counters(
            Crashreport, "other", **boot_reason_param
        )

    def _assert_reports_with_same_timestamp_are_counted(
        self,
        report_type,
        counter_attribute_name,
        username_1=Dummy.USERNAMES[0],
        username_2=Dummy.USERNAMES[1],
        **kwargs
    ):
        """Validate that reports with the same timestamp are counted.

        Reports from different devices but the same timestamp should be
        counted as independent reports.
        """
        # Create a report
        device1 = Dummy.create_device(
            user=Dummy.create_user(username=username_1)
        )
        report1 = Dummy.create_report(report_type, device=device1, **kwargs)

        # Create a second report with the same timestamp but from another device
        device2 = Dummy.create_device(
            user=Dummy.create_user(username=username_2)
        )
        Dummy.create_report(
            report_type, device=device2, date=report1.date, **kwargs
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        get_params = {
            self.unique_entry_name: getattr(report1, self.unique_entry_name)
        }
        version = self.version_class.objects.get(**get_params)

        # Assert that both reports are counted
        self.assertEqual(getattr(version, counter_attribute_name), 2)

    def test_heartbeats_with_same_timestamp_are_counted(self):
        """Validate that heartbeats with same timestamp are counted."""
        counter_attribute_name = "heartbeats"
        self._assert_reports_with_same_timestamp_are_counted(
            HeartBeat, counter_attribute_name
        )

    def test_crash_reports_with_same_timestamp_are_counted(self):
        """Validate that crash reports with same timestamp are counted."""
        counter_attribute_name = "prob_crashes"
        for i, (unique_entry, boot_reason) in enumerate(
            zip(self.unique_entries, Crashreport.CRASH_BOOT_REASONS)
        ):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: unique_entry,
            }
            self._assert_reports_with_same_timestamp_are_counted(
                Crashreport,
                counter_attribute_name,
                Dummy.USERNAMES[2 * i],
                Dummy.USERNAMES[2 * i + 1],
                **params
            )

    def test_smpl_reports_with_same_timestamp_are_counted(self):
        """Validate that smpl reports with same timestamp are counted."""
        counter_attribute_name = "smpl"
        for i, (unique_entry, boot_reason) in enumerate(
            zip(self.unique_entries, Crashreport.SMPL_BOOT_REASONS)
        ):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: unique_entry,
            }
            self._assert_reports_with_same_timestamp_are_counted(
                Crashreport,
                counter_attribute_name,
                Dummy.USERNAMES[2 * i],
                Dummy.USERNAMES[2 * i + 1],
                **params
            )

    def test_other_reports_with_same_timestamp_are_counted(self):
        """Validate that other reports with same timestamp are counted."""
        counter_attribute_name = "other"
        params = {"boot_reason": "random boot reason"}
        self._assert_reports_with_same_timestamp_are_counted(
            Crashreport, counter_attribute_name, **params
        )

    def _assert_older_reports_update_released_on_date(
        self, report_type, **kwargs
    ):
        """Test updating of the released_on date.

        Validate that the released_on date is updated once an older report is
        sent.
        """
        # Create a report
        device = Dummy.create_device(user=Dummy.create_user())
        report = Dummy.create_report(report_type, device=device, **kwargs)

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the first report date
        report_date = (
            report.date.date() if report_type == Crashreport else report.date
        )
        self.assertEqual(version.released_on, report_date)

        # Create a second report with the a timestamp earlier in time
        report_2_date = report.date - timedelta(days=1)
        Dummy.create_report(
            report_type, device=device, date=report_2_date, **kwargs
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the older report date
        if report_type == Crashreport:
            report_2_date = report_2_date.date()
        self.assertEqual(version.released_on, report_2_date)

    def _assert_newer_reports_do_not_update_released_on_date(
        self, report_type, **kwargs
    ):
        """Test updating of the released_on date.

        Validate that the released_on date is not updated once a newer report is
        sent.
        """
        # Create a report
        device = Dummy.create_device(user=Dummy.create_user())
        report = Dummy.create_report(report_type, device=device, **kwargs)
        report_1_date = (
            report.date.date() if report_type == Crashreport else report.date
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the first report date
        self.assertEqual(version.released_on, report_1_date)

        # Create a second report with the a timestamp later in time
        report_2_date = report.date + timedelta(days=1)
        Dummy.create_report(
            report_type, device=device, date=report_2_date, **kwargs
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the older report date
        self.assertEqual(version.released_on, report_1_date)

    def test_older_heartbeat_updates_released_on_date(self):
        """Validate that older heartbeats update the release date."""
        self._assert_older_reports_update_released_on_date(HeartBeat)

    def test_older_crash_report_updates_released_on_date(self):
        """Validate that older crash reports update the release date."""
        self._assert_older_reports_update_released_on_date(Crashreport)

    def test_newer_heartbeat_does_not_update_released_on_date(self):
        """Validate that newer heartbeats don't update the release date."""
        self._assert_newer_reports_do_not_update_released_on_date(HeartBeat)

    def test_newer_crash_report_does_not_update_released_on_date(self):
        """Validate that newer crash reports don't update the release date."""
        self._assert_newer_reports_do_not_update_released_on_date(Crashreport)

    def _assert_manually_changed_released_on_date_is_not_updated(
        self, report_type, **kwargs
    ):
        """Test updating of manually changed released_on dates.

        Validate that a manually changed released_on date is not updated when
        new reports are sent.
        """
        # Create a report
        device = Dummy.create_device(user=Dummy.create_user())
        report = Dummy.create_report(report_type, device=device, **kwargs)

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the first report date
        report_date = (
            report.date.date() if report_type == Crashreport else report.date
        )
        self.assertEqual(version.released_on, report_date)

        # Create a second report with a timestamp earlier in time
        report_2_date = report.date - timedelta(days=1)
        Dummy.create_report(
            report_type, device=device, date=report_2_date, **kwargs
        )

        # Manually change the released_on date
        version_release_date = report_date + timedelta(days=1)
        version.released_on = version_release_date
        version.save()

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date still matches the date is was
        # manually changed to
        self.assertEqual(version.released_on, version_release_date)

    def test_manually_changed_released_on_date_is_not_updated_by_heartbeat(
        self
    ):
        """Test update of manually changed released_on date with heartbeat."""
        self._assert_manually_changed_released_on_date_is_not_updated(HeartBeat)

    def test_manually_changed_released_on_date_is_not_updated_by_crash_report(
        self
    ):
        """Test update of manually changed released_on date with crashreport."""
        self._assert_manually_changed_released_on_date_is_not_updated(
            Crashreport
        )


# pylint: disable=too-many-ancestors
class StatsCommandRadioVersionsTestCase(StatsCommandVersionsTestCase):
    """Test the generation of RadioVersion stats with the stats command."""

    version_class = RadioVersion
    unique_entry_name = "radio_version"
    unique_entries = Dummy.RADIO_VERSIONS


class CommandDebugOutputTestCase(TestCase):
    """Test the reset and update commands debug output."""

    # Additional positional arguments to pass to the commands
    _CMD_ARGS = ["--no-color", "-v 2"]

    # The stats models
    _STATS_MODELS = [Version, VersionDaily, RadioVersion, RadioVersionDaily]
    # The models that will generate an output
    _ALL_MODELS = _STATS_MODELS + [StatsMetadata]
    _COUNTER_NAMES = ["heartbeats", "crashes", "smpl", "other"]
    _COUNTER_ACTIONS = ["created", "updated"]

    def _assert_command_output_matches(self, command, number, facts, models):
        """Validate the debug output of a command.

        The debug output is matched against the facts and models given in
        the parameters.
        """
        buffer = StringIO()
        call_command("stats", command, *self._CMD_ARGS, stdout=buffer)
        output = buffer.getvalue().splitlines()

        expected_output = "{number} {model} {fact}"
        for model in models:
            for fact in facts:
                self.assertIn(
                    expected_output.format(
                        number=number, model=model.__name__, fact=fact
                    ),
                    output,
                )

    def test_reset_command_on_empty_db(self):
        """Test the reset command on an empty database.

        The reset command should yield nothing on an empty database.
        """
        self._assert_command_output_matches(
            "reset", 0, ["deleted"], self._ALL_MODELS
        )

    def test_update_command_on_empty_db(self):
        """Test the update command on an empty database.

        The update command should yield nothing on an empty database.
        """
        pattern = "{action} for counter {counter}"
        facts = [
            pattern.format(action=counter_action, counter=counter_name)
            for counter_action in self._COUNTER_ACTIONS
            for counter_name in self._COUNTER_NAMES
        ]
        self._assert_command_output_matches(
            "update", 0, facts, self._STATS_MODELS
        )

    def test_reset_command_deletion_of_instances(self):
        """Test the deletion of stats model instances with the reset command.

        This test validates that model instances get deleted when the
        reset command is called on a database that only contains a single
        model instance for each class.
        """
        # Create dummy version instances
        version = Dummy.create_version()
        radio_version = Dummy.create_version(RadioVersion)
        Dummy.create_daily_version(version)
        Dummy.create_daily_radio_version(radio_version)
        Dummy.create_stats_metadata()

        # We expect that the model instances get deleted
        self._assert_command_output_matches(
            "reset", 1, ["deleted"], self._ALL_MODELS
        )
