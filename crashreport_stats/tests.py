"""Test crashreport_stats models and the 'stats' command."""

# pylint: disable=too-many-lines,too-many-public-methods

from io import StringIO
from datetime import datetime, date, timedelta
import operator
import os
import unittest
import zipfile

import pytz

from django.contrib.auth.models import Group
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

from crashreports.models import Crashreport, Device, HeartBeat, LogFile, User
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


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

    USERNAMES = ["testuser1", "testuser2"]

    DATES = [date(2018, 3, 19), date(2018, 3, 26), date(2018, 5, 1)]

    DEFAULT_DUMMY_VERSION_VALUES = {
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "first_seen_on": DATES[1],
        "released_on": DATES[0],
        "is_beta_release": False,
        "is_official_release": True,
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

    DEFAULT_DUMMY_USER_VALUES = {"username": USERNAMES[0]}

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "radio_version": RADIO_VERSIONS[0],
        "date": datetime(2018, 3, 19, 12, 0, 0, tzinfo=pytz.utc),
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

    DEFAULT_DUMMY_LOG_FILE_VALUES = {
        "logfile_type": "last_kmsg",
        "logfile": os.path.join("resources", "test", "test_logfile.zip"),
    }

    DEFAULT_DUMMY_LOG_FILE_NAME = "dmesg.log"

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
    def create_dummy_log_file(crashreport, **kwargs):
        """Create a dummy log file instance.

        The dummy instance is created and saved to the database.

        Args:
            crashreport: The crashreport that the log file belongs to.
            **kwargs: Optional arguments to extend/overwrite the default values.

        Returns: The created log file instance.

        """
        entity = LogFile(
            crashreport=crashreport,
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_LOG_FILE_VALUES, kwargs)
        )

        entity.save()
        return entity

    @staticmethod
    def read_logfile_contents(path_to_zipfile, logfile_name):
        """Read bytes of a zipped logfile."""
        archive = zipfile.ZipFile(path_to_zipfile, "r")
        return archive.read(logfile_name)

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


class _HiccupAPITestCase(APITestCase):
    """Abstract class for Hiccup REST API test cases to inherit from."""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Create an admin and client user for accessing the API.

        The APIClient that can be used to make authenticated requests as
        admin user is stored in self.admin. Another client (which is
        related to a user that is part of the Fairphone software team group)
        is stored in self.fp_staff_client.
        """
        admin_user = User.objects.create_superuser(
            "somebody", "somebody@example.com", "thepassword"
        )
        cls.admin = APIClient()
        cls.admin.force_authenticate(admin_user)

        fp_software_team_group = Group(name=FP_STAFF_GROUP_NAME)
        fp_software_team_group.save()
        fp_software_team_user = User.objects.create_user(
            "fp_staff", "somebody@fairphone.com", "thepassword"
        )
        fp_software_team_user.groups.add(fp_software_team_group)
        cls.fp_staff_client = APIClient()
        cls.fp_staff_client.login(username="fp_staff", password="thepassword")


class StatusTestCase(_HiccupAPITestCase):
    """Test the status endpoint."""

    status_url = reverse("hiccup_stats_api_v1_status")

    def _assert_status_response_is(
        self, response, num_devices, num_crashreports, num_heartbeats
    ):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("devices", response.data)
        self.assertIn("crashreports", response.data)
        self.assertIn("heartbeats", response.data)
        self.assertEqual(response.data["devices"], num_devices)
        self.assertEqual(response.data["crashreports"], num_crashreports)
        self.assertEqual(response.data["heartbeats"], num_heartbeats)

    def test_get_status_empty_database(self):
        """Get the status when the database is empty."""
        response = self.fp_staff_client.get(self.status_url)
        self._assert_status_response_is(response, 0, 0, 0)

    def test_get_status(self):
        """Get the status after some reports have been created."""
        # Create a device with a heartbeat and a crash report
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        Dummy.create_dummy_report(HeartBeat, device)
        Dummy.create_dummy_report(Crashreport, device)

        # Create a second device without any reports
        Dummy.create_dummy_device(
            Dummy.create_dummy_user(username=Dummy.USERNAMES[1])
        )

        # Assert that the status includes the appropriate numbers
        response = self.fp_staff_client.get(self.status_url)
        self._assert_status_response_is(
            response, num_devices=2, num_crashreports=1, num_heartbeats=1
        )


class _VersionTestCase(_HiccupAPITestCase):
    """Abstract class for version-related test cases to inherit from."""

    # The attribute name characterising the unicity of a stats entry (the
    # named identifier)
    unique_entry_name = "build_fingerprint"
    # The collection of unique entries to post
    unique_entries = Dummy.BUILD_FINGERPRINTS
    # The URL to retrieve the stats entries from
    endpoint_url = reverse("hiccup_stats_api_v1_versions")

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

    # pylint: disable=too-many-ancestors

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

    def _assert_reports_with_same_timestamp_are_counted(
        self, report_type, counter_attribute_name, **kwargs
    ):
        """Validate that reports with the same timestamp are counted.

        Reports from different devices but the same timestamp should be
        counted as independent reports.
        """
        # Create a report
        device1 = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        report1 = Dummy.create_dummy_report(
            report_type, device=device1, **kwargs
        )

        # Create a second report with the same timestamp but from another device
        device2 = Dummy.create_dummy_device(
            user=Dummy.create_dummy_user(username=Dummy.USERNAMES[1])
        )
        Dummy.create_dummy_report(
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

    @unittest.skip(
        "Duplicates are dropped based on their timestamp at the moment. This is"
        "to be adapted so that they are dropped taking into account the device"
        "UUID as well."
    )
    def test_heartbeats_with_same_timestamp_are_counted(self):
        """Validate that heartbeats with same timestamp are counted."""
        counter_attribute_name = "heartbeats"
        self._assert_reports_with_same_timestamp_are_counted(
            HeartBeat, counter_attribute_name
        )

    @unittest.skip(
        "Duplicates are dropped based on their timestamp at the moment. This is"
        "to be adapted so that they are dropped taking into account the device"
        "UUID as well."
    )
    def test_crash_reports_with_same_timestamp_are_counted(self):
        """Validate that crash report duplicates are ignored."""
        counter_attribute_name = "prob_crashes"
        for unique_entry, boot_reason in zip(
            self.unique_entries, Crashreport.CRASH_BOOT_REASONS
        ):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: unique_entry,
            }
            self._assert_reports_with_same_timestamp_are_counted(
                Crashreport, counter_attribute_name, **params
            )

    @unittest.skip(
        "Duplicates are dropped based on their timestamp at the moment. This is"
        "to be adapted so that they are dropped taking into account the device"
        "UUID as well."
    )
    def test_smpl_reports_with_same_timestamp_are_counted(self):
        """Validate that smpl report duplicates are ignored."""
        counter_attribute_name = "smpl"
        for unique_entry, boot_reason in zip(
            self.unique_entries, Crashreport.SMPL_BOOT_REASONS
        ):
            params = {
                "boot_reason": boot_reason,
                self.unique_entry_name: unique_entry,
            }
            self._assert_reports_with_same_timestamp_are_counted(
                Crashreport, counter_attribute_name, **params
            )

    @unittest.skip(
        "Duplicates are dropped based on their timestamp at the moment. This is"
        "to be adapted so that they are dropped taking into account the device"
        "UUID as well."
    )
    def test_other_reports_with_same_timestamp_are_counted(self):
        """Validate that other report duplicates are ignored."""
        counter_attribute_name = "other"
        params = {"boot_reason": "random boot reason"}
        self._assert_reports_with_same_timestamp_are_counted(
            Crashreport, counter_attribute_name, **params
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

    def _assert_older_reports_update_released_on_date(
        self, report_type, **kwargs
    ):
        """Test updating of the released_on date.

        Validate that the released_on date is updated once an older report is
        sent.
        """
        # Create a report
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        report = Dummy.create_dummy_report(report_type, device=device, **kwargs)

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the first report date
        self.assertEqual(version.released_on, report.date.date())

        # Create a second report with the a timestamp earlier in time
        report_2_date = report.date - timedelta(days=1)
        Dummy.create_dummy_report(
            report_type, device=device, date=report_2_date, **kwargs
        )

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the older report date
        self.assertEqual(version.released_on, report_2_date.date())

    def _assert_newer_reports_do_not_update_released_on_date(
        self, report_type, **kwargs
    ):
        """Test updating of the released_on date.

        Validate that the released_on date is not updated once a newer report is
        sent.
        """
        # Create a report
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        report = Dummy.create_dummy_report(report_type, device=device, **kwargs)
        report_1_date = report.date.date()

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
        Dummy.create_dummy_report(
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
        device = Dummy.create_dummy_device(user=Dummy.create_dummy_user())
        report = Dummy.create_dummy_report(report_type, device=device, **kwargs)

        # Run the command to update the database
        call_command("stats", "update")

        # Get the corresponding version instance from the database
        version = self.version_class.objects.get(
            **{self.unique_entry_name: getattr(report, self.unique_entry_name)}
        )

        # Assert that the released_on date matches the first report date
        self.assertEqual(version.released_on, report.date.date())

        # Create a second report with a timestamp earlier in time
        report_2_date = report.date - timedelta(days=1)
        Dummy.create_dummy_report(
            report_type, device=device, date=report_2_date, **kwargs
        )

        # Manually change the released_on date
        version_release_date = report.date + timedelta(days=1)
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
        self.assertEqual(version.released_on, version_release_date.date())

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
        version = Dummy.create_dummy_version()
        radio_version = Dummy.create_dummy_radio_version()
        Dummy.create_dummy_daily_version(version)
        Dummy.create_dummy_daily_radio_version(radio_version)
        Dummy.create_dummy_stats_metadata()

        # We expect that the model instances get deleted
        self._assert_command_output_matches(
            "reset", 1, ["deleted"], self._ALL_MODELS
        )


class DeviceStatsTestCase(_HiccupAPITestCase):
    """Test the single device stats REST endpoints."""

    def _get_with_params(self, url, params):
        url = reverse(url, kwargs=params)
        return self.fp_staff_client.get(url)

    def _assert_device_stats_response_is(
        self,
        response,
        uuid,
        board_date,
        num_heartbeats,
        num_crashreports,
        num_smpls,
        crashes_per_day,
        smpl_per_day,
        last_active,
    ):
        # pylint: disable=too-many-arguments
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("uuid", response.data)
        self.assertIn("board_date", response.data)
        self.assertIn("heartbeats", response.data)
        self.assertIn("crashreports", response.data)
        self.assertIn("smpls", response.data)
        self.assertIn("crashes_per_day", response.data)
        self.assertIn("smpl_per_day", response.data)
        self.assertIn("last_active", response.data)

        self.assertEqual(response.data["uuid"], uuid)
        self.assertEqual(response.data["board_date"], board_date)
        self.assertEqual(response.data["heartbeats"], num_heartbeats)
        self.assertEqual(response.data["crashreports"], num_crashreports)
        self.assertEqual(response.data["smpls"], num_smpls)
        self.assertEqual(response.data["crashes_per_day"], crashes_per_day)
        self.assertEqual(response.data["smpl_per_day"], smpl_per_day)
        self.assertEqual(response.data["last_active"], last_active)

    @unittest.skip(
        "Fails because there is no fallback for the last_active "
        "date for devices without heartbeats."
    )
    def test_get_device_stats_no_reports(self):
        """Test getting device stats for a device without reports."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=0,
            num_crashreports=0,
            num_smpls=0,
            crashes_per_day=0.0,
            smpl_per_day=0.0,
            last_active=device.board_date,
        )

    def test_get_device_stats_no_crash_reports(self):
        """Test getting device stats for a device without crashreports."""
        # Create a device and a heartbeat
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        heartbeat = Dummy.create_dummy_report(HeartBeat, device)

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=1,
            num_crashreports=0,
            num_smpls=0,
            crashes_per_day=0.0,
            smpl_per_day=0.0,
            last_active=heartbeat.date,
        )

    @unittest.skip(
        "Fails because there is no fallback for the last_active "
        "date for devices without heartbeats."
    )
    def test_get_device_stats_no_heartbeats(self):
        """Test getting device stats for a device without heartbeats."""
        # Create a device and crashreport
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        Dummy.create_dummy_report(Crashreport, device)

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=0,
            num_crashreports=1,
            num_smpls=0,
            crashes_per_day=0.0,
            smpl_per_day=0.0,
            last_active=device.board_date,
        )

    def test_get_device_stats(self):
        """Test getting device stats for a device."""
        # Create a device with a heartbeat and one report of each type
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        heartbeat = Dummy.create_dummy_report(HeartBeat, device)
        for boot_reason in (
            Crashreport.SMPL_BOOT_REASONS
            + Crashreport.CRASH_BOOT_REASONS
            + ["other boot reason"]
        ):
            Dummy.create_dummy_report(
                Crashreport, device, boot_reason=boot_reason
            )

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=1,
            num_crashreports=len(Crashreport.CRASH_BOOT_REASONS),
            num_smpls=len(Crashreport.SMPL_BOOT_REASONS),
            crashes_per_day=len(Crashreport.CRASH_BOOT_REASONS),
            smpl_per_day=len(Crashreport.SMPL_BOOT_REASONS),
            last_active=heartbeat.date,
        )

    def test_get_device_stats_multiple_days(self):
        """Test getting device stats for a device that sent more reports."""
        # Create a device with some heartbeats and reports over time
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        num_days = 100
        for i in range(num_days):
            report_day = datetime.now(tz=pytz.utc) + timedelta(days=i)
            heartbeat = Dummy.create_dummy_report(
                HeartBeat, device, date=report_day
            )
            Dummy.create_dummy_report(Crashreport, device, date=report_day)
            Dummy.create_dummy_report(
                Crashreport,
                device,
                date=report_day,
                boot_reason=Crashreport.SMPL_BOOT_REASONS[0],
            )

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=num_days,
            num_crashreports=num_days,
            num_smpls=num_days,
            crashes_per_day=1,
            smpl_per_day=1,
            last_active=heartbeat.date,
        )

    def test_get_device_stats_multiple_days_missing_heartbeat(self):
        """Test getting device stats for a device with missing heartbeat."""
        # Create a device with some heartbeats and reports over time
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        num_days = 100
        skip_day = round(num_days / 2)
        for i in range(num_days):
            report_day = datetime.now(tz=pytz.utc) + timedelta(days=i)
            # Skip creation of heartbeat at one day
            if i != skip_day:
                heartbeat = Dummy.create_dummy_report(
                    HeartBeat, device, date=report_day
                )
            Dummy.create_dummy_report(Crashreport, device, date=report_day)

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=num_days - 1,
            num_crashreports=num_days,
            num_smpls=0,
            crashes_per_day=num_days / (num_days - 1),
            smpl_per_day=0,
            last_active=heartbeat.date,
        )

    @unittest.skip("Duplicate heartbeats are currently not dropped.")
    def test_get_device_stats_multiple_days_duplicate_heartbeat(self):
        """Test getting device stats for a device with duplicate heartbeat.

        Duplicate heartbeats are dropped and thus should not influence the
        statistics.
        """
        # Create a device with some heartbeats and reports over time
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        num_days = 100
        duplicate_day = round(num_days / 2)
        first_report_day = Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES["date"]
        for i in range(num_days):
            report_day = first_report_day + timedelta(days=i)
            heartbeat = Dummy.create_dummy_report(
                HeartBeat, device, date=report_day
            )
            # Create a second at the duplicate day (with 1 hour delay)
            if i == duplicate_day:
                Dummy.create_dummy_report(
                    HeartBeat, device, date=report_day + timedelta(hours=1)
                )
            Dummy.create_dummy_report(Crashreport, device, date=report_day)

        # Get the device statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_overview", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self._assert_device_stats_response_is(
            response=response,
            uuid=str(device.uuid),
            board_date=device.board_date,
            num_heartbeats=num_days,
            num_crashreports=num_days,
            num_smpls=0,
            crashes_per_day=1,
            smpl_per_day=0,
            last_active=heartbeat.date,
        )

    def test_get_device_report_history_no_reports(self):
        """Test getting report history stats for a device without reports."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the device report history statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_report_history", {"uuid": device.uuid}
        )

        # Assert that the report history is empty
        self.assertEqual([], response.data)

    @unittest.skip("Broken raw query. Heartbeats are not counted correctly.")
    def test_get_device_report_history(self):
        """Test getting report history stats for a device."""
        # Create a device with a heartbeat and one report of each type
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        heartbeat = Dummy.create_dummy_report(HeartBeat, device)
        for boot_reason in (
            Crashreport.SMPL_BOOT_REASONS
            + Crashreport.CRASH_BOOT_REASONS
            + ["other boot reason"]
        ):
            Dummy.create_dummy_report(
                Crashreport, device, boot_reason=boot_reason
            )

        # Get the device report history statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_report_history", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        report_history = [
            {
                "date": heartbeat.date.date(),
                "heartbeats": 1,
                "smpl": len(Crashreport.SMPL_BOOT_REASONS),
                "prob_crashes": len(Crashreport.CRASH_BOOT_REASONS),
                "other": 1,
            }
        ]
        self.assertEqual(report_history, response.data)

    def test_get_device_update_history_no_reports(self):
        """Test getting update history stats for a device without reports."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the device report history statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_update_history", {"uuid": device.uuid}
        )

        # Assert that the update history is empty
        self.assertEqual([], response.data)

    def test_get_device_update_history(self):
        """Test getting update history stats for a device."""
        # Create a device with a heartbeat and one report of each type
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        heartbeat = Dummy.create_dummy_report(HeartBeat, device)
        for boot_reason in (
            Crashreport.SMPL_BOOT_REASONS
            + Crashreport.CRASH_BOOT_REASONS
            + ["other boot reason"]
        ):
            params = {"boot_reason": boot_reason}
            Dummy.create_dummy_report(Crashreport, device, **params)

        # Get the device update history statistics
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_update_history", {"uuid": device.uuid}
        )

        # Assert that the statistics match
        update_history = [
            {
                "build_fingerprint": heartbeat.build_fingerprint,
                "heartbeats": 1,
                "max": device.id,
                "other": 1,
                "prob_crashes": len(Crashreport.CRASH_BOOT_REASONS),
                "smpl": len(Crashreport.SMPL_BOOT_REASONS),
                "update_date": heartbeat.date,
            }
        ]
        self.assertEqual(update_history, response.data)

    def test_get_device_update_history_multiple_updates(self):
        """Test getting update history stats with multiple updates."""
        # Create a device with a heartbeats and crashreport for each build
        # fingerprint in the dummy values
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        expected_update_history = []
        for i, build_fingerprint in enumerate(Dummy.BUILD_FINGERPRINTS):
            report_day = datetime.now(tz=pytz.utc) + timedelta(days=i)
            Dummy.create_dummy_report(
                HeartBeat,
                device,
                date=report_day,
                build_fingerprint=build_fingerprint,
            )
            Dummy.create_dummy_report(
                Crashreport,
                device,
                date=report_day,
                build_fingerprint=build_fingerprint,
            )

            # Create the expected update history object
            expected_update_history.append(
                {
                    "update_date": report_day,
                    "build_fingerprint": build_fingerprint,
                    "max": device.id,
                    "prob_crashes": 1,
                    "smpl": 0,
                    "other": 0,
                    "heartbeats": 1,
                }
            )
        # Sort the expected values by build fingerprint
        expected_update_history.sort(
            key=operator.itemgetter("build_fingerprint")
        )

        # Get the device update history statistics and sort it
        response = self._get_with_params(
            "hiccup_stats_api_v1_device_update_history", {"uuid": device.uuid}
        )
        response.data.sort(key=operator.itemgetter("build_fingerprint"))

        # Assert that the statistics match
        self.assertEqual(expected_update_history, response.data)

    def test_download_non_existing_logfile(self):
        """Test download of a non existing log file."""
        # Try to get a log file
        response = self._get_with_params(
            "hiccup_stats_api_v1_logfile_download", {"id_logfile": 0}
        )

        # Assert that the log file was not found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_download_logfile(self):
        """Test download of log files."""
        # Create a device with a crash report along with log file
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        crashreport = Dummy.create_dummy_report(Crashreport, device)
        logfile = Dummy.create_dummy_log_file(crashreport)

        # Get the log file
        response = self._get_with_params(
            "hiccup_stats_api_v1_logfile_download", {"id_logfile": logfile.id}
        )

        # Assert that the log file contents are in the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(Dummy.DEFAULT_DUMMY_LOG_FILE_NAME, response.data)
        expected_logfile_content = Dummy.read_logfile_contents(
            logfile.logfile.path, Dummy.DEFAULT_DUMMY_LOG_FILE_NAME
        )
        self.assertEqual(
            response.data[Dummy.DEFAULT_DUMMY_LOG_FILE_NAME],
            expected_logfile_content,
        )


class ViewsTestCase(_HiccupAPITestCase):
    """Test cases for the statistics views."""

    home_url = reverse("device")
    device_url = reverse("hiccup_stats_device")
    versions_url = reverse("hiccup_stats_versions")
    versions_all_url = reverse("hiccup_stats_versions_all")

    @staticmethod
    def _url_with_params(url, params):
        return "{}?{}".format(url, urlencode(params))

    def _get_with_params(self, url, params):
        return self.fp_staff_client.get(self._url_with_params(url, params))

    def test_get_home_view(self):
        """Test getting the home view with device search form."""
        response = self.fp_staff_client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(response.context["devices"], None)

    def test_home_view_filter_devices_by_uuid(self):
        """Test filtering devices by UUID."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Filter devices by UUID of the created device
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device.uuid)}
        )

        # Assert that the the client is redirected to the device page
        self.assertRedirects(
            response,
            self._url_with_params(self.device_url, {"uuid": device.uuid}),
        )

    def test_home_view_filter_devices_by_uuid_part(self):
        """Test filtering devices by start of UUID."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Filter devices with start of the created device's UUID
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device.uuid)[:4]}
        )

        # Assert that the the client is redirected to the device page
        self.assertRedirects(
            response,
            self._url_with_params(self.device_url, {"uuid": device.uuid}),
        )

    def test_home_view_filter_devices_by_uuid_part_ambiguous_result(self):
        """Test filtering devices with common start of UUIDs."""
        # Create two devices
        device1 = Dummy.create_dummy_device(Dummy.create_dummy_user())
        device2 = Dummy.create_dummy_device(
            Dummy.create_dummy_user(username=Dummy.USERNAMES[1])
        )

        # Adapt the devices' UUID so that they start with the same characters
        device1.uuid = "4060fd90-6de1-4b03-a380-4277c703e913"
        device1.save()
        device2.uuid = "4061c59b-823d-4ec6-a463-8ac0c1cea67d"
        device2.save()

        # Filter devices with first three (common) characters of the UUID
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device1.uuid)[:3]}
        )

        # Assert that both devices are part of the result
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(set(response.context["devices"]), {device1, device2})

    def test_home_view_filter_devices_empty_database(self):
        """Test filtering devices on an empty database."""
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": "TestUUID"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

    def test_home_view_filter_devices_no_uuid(self):
        """Test filtering devices without specifying UUID."""
        response = self.fp_staff_client.post(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(response.context["devices"], None)

    def test_get_device_view_empty_database(self):
        """Test getting device view on an empty database."""
        response = self.fp_staff_client.get(self.device_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_device_view(self):
        """Test getting device view."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the corresponding device view
        response = self._get_with_params(self.device_url, {"uuid": device.uuid})

        # Assert that the view is constructed from the correct templates and
        # the response context contains the device UUID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/device.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/device_overview.html", count=1
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_update_history.html",
            count=1,
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_report_history.html",
            count=1,
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_crashreport_table.html",
            count=1,
        )
        self.assertEqual(response.context["uuid"], str(device.uuid))

    def _assert_versions_view_templates_are_used(self, response):
        self.assertTemplateUsed(
            response, "crashreport_stats/versions.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_table.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_pie_chart.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_bar_chart.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_area_chart.html", count=1
        )

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_view_empty_database(self):
        """Test getting versions view on an empty database."""
        response = self.fp_staff_client.get(self.versions_url)

        # Assert that the correct templates are used and the response context
        # contains the correct value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context["is_official_release"], True)

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_view(self):
        """Test getting versions view."""
        # Create a version
        Dummy.create_dummy_version()

        # Get the versions view
        response = self.fp_staff_client.get(self.versions_url)

        # Assert that the correct templates are used and the response context
        # contains the correct value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context["is_official_release"], True)

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_all_view_no_versions(self):
        """Test getting versions all view on an empty database."""
        response = self.fp_staff_client.get(self.versions_all_url)

        # Assert that the correct templates are used and the response context
        # contains an empty value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context.get("is_official_release", ""), "")

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_all_view(self):
        """Test getting versions view."""
        # Create a version
        Dummy.create_dummy_version()

        # Get the versions view
        response = self.fp_staff_client.get(self.versions_all_url)

        # Assert that the correct templates are used and the response context
        # contains the an empty value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context.get("is_official_release", ""), "")
