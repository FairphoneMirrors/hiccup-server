"""Test crashreport_stats models and the 'stats' command."""
from io import StringIO
from datetime import datetime, date, timedelta
import pytz

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from crashreport_stats.models import (
    Version,
    VersionDaily,
    RadioVersion,
    RadioVersionDaily,
    StatsMetadata,
)

from crashreports.models import User, Device, Crashreport, HeartBeat


class Dummy:
    """Class for creating dummy instances for testing."""

    # Valid unique entries
    BUILD_FINGERPRINTS = [
        (
            "Fairphone/FP2/FP2:5.1/FP2/r4275.1_FP2_gms76_1.13.0"
            ":user/release-keys"
        ),
        (
            "Fairphone/FP2/FP2:5.1.1/FP2-gms75.1.13.0/FP2-gms75.1.13.0"
            ":user/release-keys"
        ),
        (
            "Fairphone/FP2/FP2:6.0.1/FP2-gms-18.04.1/FP2-gms-18.04.1"
            ":user/release-keys"
        ),
        ("Fairphone/FP2/FP2:7.1.2/18.07.2/gms-7480c31d:user/release-keys"),
    ]
    RADIO_VERSIONS = [
        "4437.1-FP2-0-07",
        "4437.1-FP2-0-08",
        "4437.1-FP2-0-09",
        "4437.1-FP2-0-10",
    ]

    DATES = [date(2018, 3, 19), date(2018, 3, 26), date(2018, 5, 1)]

    DEFAULT_DUMMY_VERSION_VALUES = {
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "first_seen_on": DATES[1],
        "released_on": DATES[0],
    }

    DEFAULT_DUMMY_VERSION_DAILY_VALUES = {"date": DATES[1]}

    DEFAULT_DUMMY_RADIO_VERSION_VALUES = {
        "radio_version": RADIO_VERSIONS[0],
        "first_seen_on": DATES[1],
        "released_on": DATES[0],
    }

    DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES = {"date": DATES[1]}

    DEFAULT_DUMMY_STATSMETADATA_VALUES = {
        "updated_at": datetime(2018, 6, 15, 2, 12, 24, tzinfo=pytz.utc)
    }

    DEFAULT_DUMMY_DEVICE_VALUES = {
        "board_date": datetime(2015, 12, 15, 1, 23, 45, tzinfo=pytz.utc),
        "chipset": "Qualcomm MSM8974PRO-AA",
        "token": "64111c62d521fb4724454ca6dea27e18f93ef56e",
    }

    DEFAULT_DUMMY_USER_VALUES = {"username": "testuser"}

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "radio_version": RADIO_VERSIONS[0],
        "date": datetime(2018, 3, 19, tzinfo=pytz.utc),
    }

    DEFAULT_DUMMY_CRASHREPORT_VALUES = DEFAULT_DUMMY_HEARTBEAT_VALUES.copy()
    DEFAULT_DUMMY_CRASHREPORT_VALUES.update(
        {
            "is_fake_report": 0,
            "boot_reason": Crashreport.BOOT_REASON_UNKOWN,
            "power_on_reason": "it was powered on",
            "power_off_reason": "something happened and it went off",
        }
    )

    @staticmethod
    def update_copy(original, update):
        """Merge fields of update into a copy of original."""
        data = original.copy()
        data.update(update)
        return data

    @staticmethod
    def create_dummy_user(**kwargs):
        """Create a dummy user instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created user instance.

        """
        entity = User(
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_USER_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_device(user, **kwargs):
        """Create a dummy device instance.

        The dummy instance is created and saved to the database.
        Args:
            user: The user instance that the device should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created device instance.

        """
        entity = Device(
            user=user,
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_DEVICE_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_report(report_type, device, **kwargs):
        """Create a dummy report instance of the given report class type.

        The dummy instance is created and saved to the database.
        Args:
            report_type: The class of the report type to be created.
            user: The device instance that the heartbeat should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created report instance.

        """
        if report_type == HeartBeat:
            entity = HeartBeat(
                device=device,
                **Dummy.update_copy(
                    Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES, kwargs
                )
            )
        elif report_type == Crashreport:
            entity = Crashreport(
                device=device,
                **Dummy.update_copy(
                    Dummy.DEFAULT_DUMMY_CRASHREPORT_VALUES, kwargs
                )
            )
        else:
            raise RuntimeError(
                "No dummy report instance can be created for {}".format(
                    report_type.__name__
                )
            )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_version(**kwargs):
        """Create a dummy version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created version instance.

        """
        entity = Version(
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_VERSION_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_radio_version(**kwargs):
        """Create a dummy radio version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created radio version instance.

        """
        entity = RadioVersion(
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_RADIO_VERSION_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_daily_version(version, **kwargs):
        """Create a dummy daily version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily version instance.

        """
        entity = VersionDaily(
            version=version,
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_VERSION_DAILY_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_daily_radio_version(version, **kwargs):
        """Create a dummy daily radio version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily radio version instance.

        """
        entity = RadioVersionDaily(
            version=version,
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_stats_metadata(**kwargs):
        """Create a dummy stats metadata instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created stats metadata instance.

        """
        entity = StatsMetadata(
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_STATSMETADATA_VALUES, kwargs
            )
        )
        entity.save()
        return entity


class _VersionTestCase(APITestCase):
    """Abstract class for version-related test cases to inherit from."""

    # The attribute name characterising the unicity of a stats entry (the
    # named identifier)
    unique_entry_name = "build_fingerprint"
    # The collection of unique entries to post
    unique_entries = Dummy.BUILD_FINGERPRINTS
    # The URL to retrieve the stats entries from
    endpoint_url = reverse("hiccup_stats_api_v1_versions")

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Create an admin user for accessing the API.

        The APIClient that can be used to make authenticated requests to the
        server is stored in self.admin.
        """
        admin_user = User.objects.create_superuser(
            "somebody", "somebody@example.com", "thepassword"
        )
        cls.admin = APIClient()
        cls.admin.force_authenticate(admin_user)

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_version(**kwargs)

    def _get_with_params(self, url, params):
        return self.admin.get("{}?{}".format(url, urlencode(params)))

    def _assert_result_length_is(self, response, count):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], count)
        self.assertEqual(len(response.data["results"]), count)

    def _assert_device_owner_has_no_get_access(self, entries_url):
        # Create a user and device
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)

        # Create authenticated client
        user = APIClient()
        user.credentials(HTTP_AUTHORIZATION="Token " + device.token)

        # Try getting entries using the client
        response = user.get(entries_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _assert_filter_result_matches(self, filter_params, expected_result):
        # List entities with filter
        response = self._get_with_params(self.endpoint_url, filter_params)

        # Expect only the single matching result to be returned
        self._assert_result_length_is(response, 1)
        self.assertEqual(
            response.data["results"][0][self.unique_entry_name],
            getattr(expected_result, self.unique_entry_name),
        )


class VersionTestCase(_VersionTestCase):
    """Test the Version and REST endpoint."""

    def _create_version_entities(self):
        versions = [
            self._create_dummy_version(**{self.unique_entry_name: unique_entry})
            for unique_entry in self.unique_entries
        ]
        return versions

    def test_list_versions_without_authentication(self):
        """Test listing of versions without authentication."""
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_versions_as_device_owner(self):
        """Test listing of versions as device owner."""
        self._assert_device_owner_has_no_get_access(self.endpoint_url)

    def test_list_versions_empty_database(self):
        """Test listing of versions on an empty database."""
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, 0)

    def test_list_versions(self):
        """Test listing versions."""
        versions = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

    def test_filter_versions_by_unique_entry_name(self):
        """Test filtering versions by their unique entry name."""
        versions = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)

        # Listing all entities should return the correct result length
        self._assert_result_length_is(response, len(versions))

        # List entities with filter
        filter_params = {
            self.unique_entry_name: getattr(versions[0], self.unique_entry_name)
        }
        self._assert_filter_result_matches(
            filter_params, expected_result=versions[0]
        )

    def test_filter_versions_by_release_type(self):
        """Test filtering versions by release type."""
        # Create versions for all combinations of release types
        versions = []
        i = 0
        for is_official_release in True, False:
            for is_beta_release in True, False:
                versions.append(
                    self._create_dummy_version(
                        **{
                            "is_official_release": is_official_release,
                            "is_beta_release": is_beta_release,
                            self.unique_entry_name: self.unique_entries[i],
                        }
                    )
                )
                i += 1

        # # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # List each of the entities with the matching filter params
        for version in versions:
            filter_params = {
                "is_official_release": version.is_official_release,
                "is_beta_release": version.is_beta_release,
            }
            self._assert_filter_result_matches(
                filter_params, expected_result=version
            )

    def test_filter_versions_by_first_seen_date(self):
        """Test filtering versions by first seen date."""
        versions = self._create_version_entities()

        # Set the first seen date of an entity
        versions[0].first_seen_on = Dummy.DATES[2]
        versions[0].save()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # Expect the single matching result to be returned
        filter_params = {"first_seen_after": Dummy.DATES[2]}
        self._assert_filter_result_matches(
            filter_params, expected_result=versions[0]
        )


# pylint: disable=too-many-ancestors
class RadioVersionTestCase(VersionTestCase):
    """Test the RadioVersion REST endpoint."""

    unique_entry_name = "radio_version"
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse("hiccup_stats_api_v1_radio_versions")

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_radio_version(**kwargs)


class VersionDailyTestCase(_VersionTestCase):
    """Test the VersionDaily REST endpoint."""

    endpoint_url = reverse("hiccup_stats_api_v1_version_daily")

    @staticmethod
    def _create_dummy_daily_version(version, **kwargs):
        return Dummy.create_dummy_daily_version(version, **kwargs)

    def _create_version_entities(self):
        versions = [
            self._create_dummy_version(**{self.unique_entry_name: unique_entry})
            for unique_entry in self.unique_entries
        ]
        versions_daily = [
            self._create_dummy_daily_version(version=version)
            for version in versions
        ]
        return versions_daily

    def test_list_daily_versions_without_authentication(self):
        """Test listing of daily versions without authentication."""
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_daily_versions_as_device_owner(self):
        """Test listing of daily versions as device owner."""
        self._assert_device_owner_has_no_get_access(self.endpoint_url)

    def test_list_daily_versions_empty_database(self):
        """Test listing of daily versions on an empty database."""
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, 0)

    def test_list_daily_versions(self):
        """Test listing daily versions."""
        versions_daily = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions_daily))

    def test_filter_daily_versions_by_version(self):
        """Test filtering versions by the version they relate to."""
        # Create VersionDaily entities
        versions = self._create_version_entities()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # List entities with filter
        param_name = "version__" + self.unique_entry_name
        filter_params = {
            param_name: getattr(versions[0].version, self.unique_entry_name)
        }
        self._assert_filter_result_matches(
            filter_params, expected_result=versions[0].version
        )

    def test_filter_daily_versions_by_date(self):
        """Test filtering daily versions by date."""
        # Create Version and VersionDaily entities
        versions = self._create_version_entities()

        # Update the date
        versions[0].date = Dummy.DATES[2]
        versions[0].save()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # Expect the single matching result to be returned
        filter_params = {"date": versions[0].date}
        self._assert_filter_result_matches(
            filter_params, expected_result=versions[0].version
        )


class RadioVersionDailyTestCase(VersionDailyTestCase):
    """Test the RadioVersionDaily REST endpoint."""

    unique_entry_name = "radio_version"
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse("hiccup_stats_api_v1_radio_version_daily")

    @staticmethod
    def _create_dummy_version(**kwargs):
        entity = RadioVersion(
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_RADIO_VERSION_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def _create_dummy_daily_version(version, **kwargs):
        return Dummy.create_dummy_daily_radio_version(version, **kwargs)


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
        now = datetime.now(pytz.utc)
        for i in range(number):
            report_date = now - timedelta(milliseconds=i)
            report_attributes = {
                self.unique_entry_name: unique_entry_name,
                "device": device,
                "date": report_date,
            }
            report_attributes.update(**kwargs)
            Dummy.create_dummy_report(report_type, **report_attributes)

    def test_stats_calculation(self):
        """Test generation of a Version instance."""
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)
        heartbeat = Dummy.create_dummy_report(HeartBeat, device=device)

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
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)
        report = Dummy.create_dummy_report(report_type, device=device)

        # Run the command to update the database
        call_command("stats", "update")

        get_params = {
            self.unique_entry_name: getattr(report, self.unique_entry_name)
        }
        version = self.version_class.objects.get(**get_params)

        self.assertEqual(report.date.date(), version.first_seen_on)

        # Create a new report from an earlier point in time
        report_time_2 = report.date - timedelta(weeks=1)
        Dummy.create_dummy_report(
            report_type, device=device, date=report_time_2
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the same version object from before
        version = self.version_class.objects.get(**get_params)

        # Validate that the date matches the report recently sent
        self.assertEqual(report_time_2.date(), version.first_seen_on)

    def test_older_heartbeat_updates_version_date(self):
        """Validate updating version date with older heartbeats."""
        self._assert_older_report_updates_version_date(HeartBeat)

    def test_older_crash_report_updates_version_date(self):
        """Validate updating version date with older crash reports."""
        self._assert_older_report_updates_version_date(Crashreport)

    def test_entries_are_unique(self):
        """Validate the entries' unicity and value."""
        # Create some reports
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)
        for unique_entry in self.unique_entries:
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
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)
        for unique_entry, num in zip(self.unique_entries, numbers):
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

    def _assert_duplicates_are_ignored(
        self, report_type, device, counter_attribute_name, **kwargs
    ):
        """Validate that reports with duplicate timestamps are ignored."""
        # Create a report
        report = Dummy.create_dummy_report(report_type, device=device, **kwargs)

        # Create a second report with the same timestamp
        Dummy.create_dummy_report(
            report_type, device=device, date=report.date, **kwargs
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        get_params = {
            self.unique_entry_name: getattr(report, self.unique_entry_name)
        }
        version = self.version_class.objects.get(**get_params)

        # Assert that the report with the duplicate timestamp is not
        # counted, i.e. only 1 report is counted.
        self.assertEqual(getattr(version, counter_attribute_name), 1)

    def test_heartbeat_duplicates_are_ignored(self):
        """Validate that heartbeat duplicates are ignored."""
        counter_attribute_name = "heartbeats"
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        self._assert_duplicates_are_ignored(
            HeartBeat, device, counter_attribute_name
        )

    def test_crash_report_duplicates_are_ignored(self):
        """Validate that crash report duplicates are ignored."""
        counter_attribute_name = "prob_crashes"
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        for i, boot_reason in enumerate(Crashreport.CRASH_BOOT_REASONS):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: self.unique_entries[i],
            }
            self._assert_duplicates_are_ignored(
                Crashreport, device, counter_attribute_name, **params
            )

    def test_smpl_report_duplicates_are_ignored(self):
        """Validate that smpl report duplicates are ignored."""
        counter_attribute_name = "smpl"
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        for i, boot_reason in enumerate(Crashreport.SMPL_BOOT_REASONS):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: self.unique_entries[i],
            }
            self._assert_duplicates_are_ignored(
                Crashreport, device, counter_attribute_name, **params
            )

    def test_other_report_duplicates_are_ignored(self):
        """Validate that other report duplicates are ignored."""
        counter_attribute_name = "other"
        params = {"boot_reason": "random boot reason"}
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        self._assert_duplicates_are_ignored(
            Crashreport, device, counter_attribute_name, **params
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
        version = Dummy.create_dummy_version()
        radio_version = Dummy.create_dummy_radio_version()
        Dummy.create_dummy_daily_version(version)
        Dummy.create_dummy_daily_radio_version(radio_version)
        Dummy.create_dummy_stats_metadata()

        # We expect that the model instances get deleted
        self._assert_command_output_matches(
            "reset", 1, ["deleted"], self._ALL_MODELS
        )
