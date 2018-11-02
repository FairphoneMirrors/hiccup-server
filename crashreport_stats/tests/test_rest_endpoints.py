"""Tests for the rest_endpoints module."""
import operator
from datetime import datetime, timedelta
import unittest

import pytz
from django.test import override_settings

from django.urls import reverse
from django.utils.http import urlencode

from rest_framework import status

from crashreport_stats.models import RadioVersion
from crashreport_stats.tests.utils import Dummy, HiccupStatsAPITestCase

from crashreports.models import Crashreport, HeartBeat, LogFile
from crashreports.tests.utils import DEFAULT_DUMMY_LOG_FILE_DIRECTORY

# pylint: disable=too-many-public-methods


class StatusTestCase(HiccupStatsAPITestCase):
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

    def test_status_url_as_admin(self):
        """Test that admin users can access the status URL."""
        self._assert_get_as_admin_user_succeeds(self.status_url)

    def test_status_url_as_fp_staff(self):
        """Test that Fairphone staff users can access the status URL."""
        self._assert_get_as_fp_staff_succeeds(self.status_url)

    def test_status_url_as_device_owner(self):
        """Test that device owner users can not access the status URL."""
        self._assert_get_as_device_owner_fails(self.status_url)

    def test_status_url_no_auth(self):
        """Test that non-authenticated users can not access the status URL."""
        self._assert_get_without_authentication_fails(self.status_url)

    def test_get_status_empty_database(self):
        """Get the status when the database is empty."""
        response = self.fp_staff_client.get(self.status_url)

        # Assert that only the device that was created by the setUpTestData()
        # method is found.
        self._assert_status_response_is(response, 1, 0, 0)

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

        # Assert that the status includes the appropriate numbers (a third
        # device was created by the setUpTestData() method)
        response = self.fp_staff_client.get(self.status_url)
        self._assert_status_response_is(
            response, num_devices=3, num_crashreports=1, num_heartbeats=1
        )


class _VersionTestCase(HiccupStatsAPITestCase):
    """Abstract class for version-related test cases to inherit from."""

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

    def _assert_filter_result_matches(
        self, endpoint_url, unique_entry_name, filter_params, expected_result
    ):
        # List entities with filter
        response = self._get_with_params(endpoint_url, filter_params)

        # Expect only the single matching result to be returned
        self._assert_result_length_is(response, 1)
        self.assertEqual(
            response.data["results"][0][unique_entry_name],
            getattr(expected_result, unique_entry_name),
        )


class VersionTestCase(_VersionTestCase):
    """Test the Version and REST endpoint."""

    # pylint: disable=too-many-ancestors

    # The attribute name characterising the unicity of a stats entry (the
    # named identifier)
    unique_entry_name = "build_fingerprint"
    # The collection of unique entries to post
    unique_entries = Dummy.BUILD_FINGERPRINTS
    # The URL to retrieve the stats entries from
    endpoint_url = reverse("hiccup_stats_api_v1_versions")

    def _create_version_entities(self):
        versions = [
            self._create_dummy_version(**{self.unique_entry_name: unique_entry})
            for unique_entry in self.unique_entries
        ]
        return versions

    def test_endpoint_url_as_admin(self):
        """Test that admin users can access the endpoint URL."""
        self._assert_get_as_admin_user_succeeds(self.endpoint_url)

    def test_endpoint_url_as_fp_staff(self):
        """Test that Fairphone staff users can access the endpoint URL."""
        self._assert_get_as_fp_staff_succeeds(self.endpoint_url)

    def test_endpoint_url_as_device_owner(self):
        """Test that device owner users can not access the endpoint URL."""
        self._assert_get_as_device_owner_fails(self.endpoint_url)

    def test_endpoint_url_no_auth(self):
        """Test that non-authenticated users can not access the endpoint URL."""
        self._assert_get_without_authentication_fails(self.endpoint_url)

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
            self.endpoint_url,
            self.unique_entry_name,
            filter_params,
            expected_result=versions[0],
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
                self.endpoint_url,
                self.unique_entry_name,
                filter_params,
                expected_result=version,
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
            self.endpoint_url,
            self.unique_entry_name,
            filter_params,
            expected_result=versions[0],
        )


# pylint: disable=too-many-ancestors
class RadioVersionTestCase(VersionTestCase):
    """Test the RadioVersion REST endpoint."""

    unique_entry_name = "radio_version"
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse("hiccup_stats_api_v1_radio_versions")

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_version(RadioVersion, **kwargs)


class VersionDailyTestCase(_VersionTestCase):
    """Test the VersionDaily REST endpoint."""

    unique_entry_name = "build_fingerprint"
    unique_entries = Dummy.BUILD_FINGERPRINTS
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

    def test_endpoint_url_as_admin(self):
        """Test that admin users can access the endpoint URL."""
        self._assert_get_as_admin_user_succeeds(self.endpoint_url)

    def test_endpoint_url_as_fp_staff(self):
        """Test that Fairphone staff users can access the endpoint URL."""
        self._assert_get_as_fp_staff_succeeds(self.endpoint_url)

    def test_endpoint_url_as_device_owner(self):
        """Test that device owner users can not access the endpoint URL."""
        self._assert_get_as_device_owner_fails(self.endpoint_url)

    def test_endpoint_url_no_auth(self):
        """Test that non-authenticated users can not access the endpoint URL."""
        self._assert_get_without_authentication_fails(self.endpoint_url)

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
            self.endpoint_url,
            self.unique_entry_name,
            filter_params,
            expected_result=versions[0].version,
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
            self.endpoint_url,
            self.unique_entry_name,
            filter_params,
            expected_result=versions[0].version,
        )


class RadioVersionDailyTestCase(VersionDailyTestCase):
    """Test the RadioVersionDaily REST endpoint."""

    unique_entry_name = "radio_version"
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse("hiccup_stats_api_v1_radio_version_daily")

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_version(RadioVersion, **kwargs)

    @staticmethod
    def _create_dummy_daily_version(version, **kwargs):
        return Dummy.create_dummy_daily_radio_version(version, **kwargs)


@override_settings(MEDIA_ROOT=DEFAULT_DUMMY_LOG_FILE_DIRECTORY)
class DeviceStatsTestCase(HiccupStatsAPITestCase):
    """Test the single device stats REST endpoints."""

    device_overview_url = "hiccup_stats_api_v1_device_overview"
    device_report_history_url = "hiccup_stats_api_v1_device_report_history"
    device_update_history_url = "hiccup_stats_api_v1_device_update_history"
    device_logfile_download_url = "hiccup_stats_api_v1_logfile_download"

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

    def test_device_overview_url_as_admin(self):
        """Test that admin users can access the URL."""
        self._assert_get_as_admin_user_succeeds(
            reverse(
                self.device_overview_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_overview_url_as_fp_staff(self):
        """Test that Fairphone staff users can access the URL."""
        self._assert_get_as_fp_staff_succeeds(
            reverse(
                self.device_overview_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_overview_url_as_device_owner(self):
        """Test that device owner users can not access the URL."""
        self._assert_get_as_device_owner_fails(
            reverse(
                self.device_overview_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_overview_url_no_auth(self):
        """Test that non-authenticated users can not access the URL."""
        self._assert_get_without_authentication_fails(
            reverse(
                self.device_overview_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_report_history_url_as_admin(self):
        """Test that admin users can access device report history URL."""
        self._assert_get_as_admin_user_succeeds(
            reverse(
                self.device_report_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_report_history_url_as_fp_staff(self):
        """Test that FP staff can access device report history URL."""
        self._assert_get_as_fp_staff_succeeds(
            reverse(
                self.device_report_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_report_history_url_as_device_owner(self):
        """Test that device owners can't access device report history URL."""
        self._assert_get_as_device_owner_fails(
            reverse(
                self.device_report_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_report_history_url_no_auth(self):
        """Test that device report history is not accessible without auth."""
        self._assert_get_without_authentication_fails(
            reverse(
                self.device_report_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_update_history_url_as_admin(self):
        """Test that admin users can access device update history URL."""
        self._assert_get_as_admin_user_succeeds(
            reverse(
                self.device_update_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_update_history_url_as_fp_staff(self):
        """Test that FP staff can access device update history URL."""
        self._assert_get_as_fp_staff_succeeds(
            reverse(
                self.device_update_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_update_history_url_as_device_owner(self):
        """Test that device owners can't access device update history URL."""
        self._assert_get_as_device_owner_fails(
            reverse(
                self.device_update_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_device_update_history_url_no_auth(self):
        """Test that device update history is not accessible without auth."""
        self._assert_get_without_authentication_fails(
            reverse(
                self.device_update_history_url,
                kwargs={"uuid": self.device_owner_device.uuid},
            )
        )

    def test_logfile_download_url_as_admin(self):
        """Test that admin users can access the logfile download URL."""
        non_existent_logfile_id = 0
        self.assertFalse(
            LogFile.objects.filter(id=non_existent_logfile_id).exists()
        )
        self._assert_get_as_admin_user_succeeds(
            reverse(
                self.device_logfile_download_url,
                kwargs={"id_logfile": non_existent_logfile_id},
            ),
            expected_status=status.HTTP_404_NOT_FOUND,
        )

    def tes_logfile_download_url_as_fp_staff(self):
        """Test that FP staff can access the logfile download URL."""
        non_existent_logfile_id = 0
        self.assertFalse(
            LogFile.objects.filter(id=non_existent_logfile_id).exists()
        )
        self._assert_get_as_fp_staff_succeeds(
            reverse(
                self.device_logfile_download_url,
                kwargs={"id_logfile": non_existent_logfile_id},
            ),
            expected_status=status.HTTP_404_NOT_FOUND,
        )

    def test_logfile_download_url_as_device_owner(self):
        """Test that device owners can't access the logfile download URL."""
        non_existent_logfile_id = 0
        self.assertFalse(
            LogFile.objects.filter(id=non_existent_logfile_id).exists()
        )
        self._assert_get_as_device_owner_fails(
            reverse(
                self.device_logfile_download_url,
                kwargs={"id_logfile": non_existent_logfile_id},
            )
        )

    def test_logfile_download_url_no_auth(self):
        """Test that the logfile download URL is not accessible without auth."""
        non_existent_logfile_id = 0
        self.assertFalse(
            LogFile.objects.filter(id=non_existent_logfile_id).exists()
        )
        self._assert_get_without_authentication_fails(
            reverse(
                self.device_logfile_download_url,
                kwargs={"id_logfile": non_existent_logfile_id},
            )
        )

    def test_get_device_stats_no_reports(self):
        """Test getting device stats for a device without reports."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the device statistics
        response = self._get_with_params(
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_overview_url, {"uuid": device.uuid}
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

    def test_get_device_stats_no_heartbeats(self):
        """Test getting device stats for a device without heartbeats."""
        # Create a device and crashreport
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        Dummy.create_dummy_report(Crashreport, device)

        # Get the device statistics
        response = self._get_with_params(
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_overview_url, {"uuid": device.uuid}
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
            self.device_report_history_url, {"uuid": device.uuid}
        )

        # Assert that the report history is empty
        self.assertEqual([], response.data)

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
            self.device_report_history_url, {"uuid": device.uuid}
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

    def test_get_device_report_history_multiple_days(self):
        """Test getting report history stats for a device for multiple days."""
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        expected_report_history = []

        # Create a device with a heartbeat and one report of each type for 10
        # days
        report_date = Dummy.DEFAULT_DUMMY_CRASHREPORT_VALUES["date"]
        for _ in range(10):
            report_date = report_date + timedelta(days=1)

            Dummy.create_dummy_report(HeartBeat, device, date=report_date)
            for boot_reason in (
                Crashreport.SMPL_BOOT_REASONS
                + Crashreport.CRASH_BOOT_REASONS
                + ["other boot reason"]
            ):
                Dummy.create_dummy_report(
                    Crashreport,
                    device,
                    boot_reason=boot_reason,
                    date=report_date,
                )

            # Create the expected report history object
            expected_report_history.append(
                {
                    "date": report_date.date(),
                    "heartbeats": 1,
                    "smpl": len(Crashreport.SMPL_BOOT_REASONS),
                    "prob_crashes": len(Crashreport.CRASH_BOOT_REASONS),
                    "other": 1,
                }
            )

        # Sort the expected values by date
        expected_report_history.sort(key=operator.itemgetter("date"))

        # Get the device report history statistics
        response = self._get_with_params(
            self.device_report_history_url, {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self.assertEqual(expected_report_history, response.data)

    def test_get_device_update_history_no_reports(self):
        """Test getting update history stats for a device without reports."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the device report history statistics
        response = self._get_with_params(
            self.device_update_history_url, {"uuid": device.uuid}
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
            self.device_update_history_url, {"uuid": device.uuid}
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
        # Sort the expected values by update date
        expected_update_history.sort(key=operator.itemgetter("update_date"))

        # Get the device update history statistics
        response = self._get_with_params(
            self.device_update_history_url, {"uuid": device.uuid}
        )

        # Assert that the statistics match
        self.assertEqual(expected_update_history, response.data)

    def test_download_non_existing_logfile(self):
        """Test download of a non existing log file."""
        # Try to get a log file
        response = self._get_with_params(
            self.device_logfile_download_url, {"id_logfile": 0}
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
            self.device_logfile_download_url, {"id_logfile": logfile.id}
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
