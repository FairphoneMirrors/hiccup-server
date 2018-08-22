"""Test the API for crashreports, devices, heartbeats and logfiles."""
import os
import tempfile
from typing import Optional

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from crashreports.models import Crashreport


class InvalidCrashTypeError(BaseException):
    """Invalid crash type encountered.

    The valid crash type values (strings) are:
      - 'crash';
      - 'smpl';
      - 'other'.

    Args:
      - crash_type: The invalid crash type.
    """

    def __init__(self, crash_type):
        """Initialise the exception using the crash type to build a message.

        Args:
            crash_type: The invalid crash type.
        """
        super(InvalidCrashTypeError, self).__init__(
            "{} is not a valid crash type".format(crash_type)
        )


class Dummy:
    """Dummy values for devices, heartbeats and crashreports."""

    DEFAULT_DUMMY_DEVICE_REGISTER_VALUES = {
        "board_date": "2015-12-15T01:23:45Z",
        "chipset": "Qualcomm MSM8974PRO-AA",
    }

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        "uuid": None,
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": (
            "Fairphone/FP2/FP2:6.0.1/FP2-gms-18.03.1/FP2-gms-18.03.1:user/"
            "release-keys"
        ),
        "radio_version": "4437.1-FP2-0-08",
        "date": "2018-03-19T09:58:30.386Z",
    }

    DEFAULT_DUMMY_CRASHREPORTS_VALUES = DEFAULT_DUMMY_HEARTBEAT_VALUES.copy()
    DEFAULT_DUMMY_CRASHREPORTS_VALUES.update(
        {
            "is_fake_report": 0,
            "boot_reason": "why?",
            "power_on_reason": "it was powered on",
            "power_off_reason": "something happened and it went off",
        }
    )

    CRASH_TYPE_TO_BOOT_REASON_MAP = {
        "crash": Crashreport.BOOT_REASON_KEYBOARD_POWER_ON,
        "smpl": Crashreport.BOOT_REASON_RTC_ALARM,
        "other": "whatever",
    }

    @staticmethod
    def _update_copy(original, update):
        """Merge fields of update into a copy of original."""
        data = original.copy()
        data.update(update)
        return data

    @staticmethod
    def device_register_data(**kwargs):
        """Return the data required to register a device.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES`.
        """
        return Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES, kwargs
        )

    @staticmethod
    def heartbeat_data(**kwargs):
        """Return the data required to create a heartbeat.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES`.
        """
        return Dummy._update_copy(Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES, kwargs)

    @staticmethod
    def crashreport_data(report_type: Optional[str] = None, **kwargs):
        """Return the data required to create a crashreport.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES`.

        Args:
            report_type: A valid value from
                `Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.keys()` that will
                define the boot reason if not explicitly defined in the
                keyword arguments already.
        """
        data = Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES, kwargs
        )
        if report_type and "boot_reason" not in kwargs:
            if report_type not in Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP:
                raise InvalidCrashTypeError(report_type)
            data["boot_reason"] = Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.get(
                report_type
            )
        return data


class DeviceRegisterAPITestCase(APITestCase):
    """Base class that offers a device registration method."""

    REGISTER_DEVICE_URL = "api_v1_register_device"

    def setUp(self):
        """Create an admin user for accessing the API.

        The APIClient that can be used to make authenticated requests to the
        server is stored in self.admin.
        """
        admin_user = User.objects.create_superuser(
            "somebody", "somebody@example.com", "thepassword"
        )
        self.admin = APIClient()
        self.admin.force_authenticate(admin_user)

    def _register_device(self, **kwargs):
        """Register a new device.

        Arguments:
            **kwargs: The data to pass the dummy data creation
                method `Dummy.device_register_data`.
        Returns:
            (UUID, APIClient, str): The uuid of the new device as well as an
            authentication token and the associated user with credentials.

        """
        data = Dummy.device_register_data(**kwargs)
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uuid = response.data["uuid"]
        token = response.data["token"]
        user = APIClient()
        user.credentials(HTTP_AUTHORIZATION="Token " + token)

        return uuid, user, token


class DeviceTestCase(DeviceRegisterAPITestCase):
    """Test cases for registering devices."""

    def test_register(self):
        """Test registration of devices."""
        response = self.client.post(
            reverse(self.REGISTER_DEVICE_URL), Dummy.device_register_data()
        )
        self.assertTrue("token" in response.data)
        self.assertTrue("uuid" in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_missing_fields(self):
        """Test registration with missing fields."""
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_board_date(self):
        """Test registration with missing board date."""
        data = Dummy.device_register_data()
        data.pop("board_date")
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_chipset(self):
        """Test registration with missing chipset."""
        data = Dummy.device_register_data()
        data.pop("chipset")
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_board_date(self):
        """Test registration with invalid board date."""
        data = Dummy.device_register_data()
        data["board_date"] = "not_a_valid_date"
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_non_existent_time_board_date(self):
        """Test registration with non existing time.

        Test the resolution of a naive date-time in which the
        Europe/Amsterdam daylight saving time transition moved the time
        "forward". The server should not crash when receiving a naive
        date-time which does not exist in the server timezone or locale.
        """
        data = Dummy.device_register_data()
        # In 2017, the Netherlands changed from CET to CEST on March,
        # 26 at 02:00
        data["board_date"] = "2017-03-26 02:34:56"
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ambiguous_time_board_date(self):
        """Test registration with ambiguous time.

        Test the resolution of a naive date-time in which the
        Europe/Amsterdam daylight saving time transition moved the time
        "backward". The server should not crash when receiving a naive
        date-time that can belong to multiple timezones.
        """
        data = Dummy.device_register_data()
        # In 2017, the Netherlands changed from CEST to CET on October,
        # 29 at 03:00
        data["board_date"] = "2017-10-29 02:34:56"
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListDevicesTestCase(DeviceRegisterAPITestCase):
    """Test cases for listing and deleting devices."""

    LIST_CREATE_URL = "api_v1_list_devices"
    RETRIEVE_URL = "api_v1_retrieve_device"

    def test_device_list(self):
        """Test registration of 2 devices."""
        number_of_devices = 2
        uuids = [
            str(self._register_device()[0]) for _ in range(number_of_devices)
        ]

        response = self.admin.get(reverse(self.LIST_CREATE_URL), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), number_of_devices)
        for result in response.data["results"]:
            self.assertIn(result["uuid"], uuids)

    def test_device_list_unauth(self):
        """Test listing devices without authentication."""
        response = self.client.get(reverse(self.LIST_CREATE_URL), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_device_auth(self):
        """Test retrieval of devices as admin user."""
        uuid, _, token = self._register_device()
        response = self.admin.get(reverse(self.RETRIEVE_URL, args=[uuid]), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(uuid))
        self.assertEqual(response.data["token"], token)

    def test_retrieve_device_unauth(self):
        """Test retrieval of devices without authentication."""
        uuid, _, _ = self._register_device()
        response = self.client.get(reverse(self.RETRIEVE_URL, args=[uuid]), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_device_auth(self):
        """Test deletion of devices as admin user."""
        uuid, _, _ = self._register_device()
        url = reverse(self.RETRIEVE_URL, args=[uuid])
        response = self.admin.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.admin.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HeartbeatListTestCase(DeviceRegisterAPITestCase):
    """Test cases for heartbeats."""

    LIST_CREATE_URL = "api_v1_heartbeats"
    RETRIEVE_URL = "api_v1_heartbeat"
    LIST_CREATE_BY_UUID_URL = "api_v1_heartbeats_by_uuid"
    RETRIEVE_BY_UUID_URL = "api_v1_heartbeat_by_uuid"

    @staticmethod
    def _create_dummy_data(**kwargs):
        return Dummy.heartbeat_data(**kwargs)

    def _post_multiple(self, client, data, count):
        return [
            client.post(reverse(self.LIST_CREATE_URL), data)
            for _ in range(count)
        ]

    def _retrieve_single(self, user):
        count = 5
        response = self._post_multiple(self.admin, self.data, count)
        self.assertEqual(len(response), count)
        self.assertEqual(response[0].status_code, status.HTTP_201_CREATED)
        url = reverse(self.RETRIEVE_URL, args=[response[0].data["id"]])
        request = user.get(url)
        return request.status_code

    def _retrieve_single_by_device(self, user):
        count = 5
        response = self._post_multiple(self.user, self.data, count)
        self.assertEqual(len(response), count)
        self.assertEqual(response[0].status_code, status.HTTP_201_CREATED)
        url = reverse(
            self.RETRIEVE_BY_UUID_URL,
            args=[self.uuid, response[0].data["device_local_id"]],
        )
        request = user.get(url)
        return request.status_code

    def setUp(self):
        """Set up a device and some data."""
        super().setUp()
        self.uuid, self.user, self.token = self._register_device()
        self.data = self._create_dummy_data(uuid=self.uuid)

    def test_create_no_auth(self):
        """Test creation without authentication."""
        noauth_client = APIClient()
        response = noauth_client.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_as_admin(self):
        """Test creation as admin."""
        response = self.admin.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["id"] > 0)

    def test_create_as_admin_not_existing_device(self):
        """Test creation of heartbeat on non-existing device."""
        response = self.admin.post(
            reverse(self.LIST_CREATE_URL), self._create_dummy_data()
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_as_uuid_owner(self):
        """Test creation as owner."""
        response = self.user.post(
            reverse(self.LIST_CREATE_URL),
            self._create_dummy_data(uuid=self.uuid),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], -1)

    def test_create_as_uuid_not_owner(self):
        """Test creation as non-owner."""
        uuid, _, _ = self._register_device()
        response = self.user.post(
            reverse(self.LIST_CREATE_URL), self._create_dummy_data(uuid=uuid)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        """Test listing of heartbeats."""
        count = 5
        self._post_multiple(self.user, self.data, count)
        response = self.admin.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), count)

    def test_retrieve_single_admin(self):
        """Test retrieval as admin."""
        self.assertEqual(self._retrieve_single(self.admin), status.HTTP_200_OK)

    def test_retrieve_single_device_owner(self):
        """Test retrieval as device owner."""
        self.assertEqual(
            self._retrieve_single(self.user), status.HTTP_403_FORBIDDEN
        )

    def test_retrieve_single_noauth(self):
        """Test retrieval without authentication."""
        noauth_client = APIClient()
        self.assertEqual(
            self._retrieve_single(noauth_client), status.HTTP_401_UNAUTHORIZED
        )

    def test_retrieve_single_by_device_admin(self):
        """Test retrieval by device as admin."""
        self.assertEqual(
            self._retrieve_single_by_device(self.admin), status.HTTP_200_OK
        )

    def test_retrieve_single_by_device_device_owner(self):
        """Test retrieval by device as owner."""
        self.assertEqual(
            self._retrieve_single_by_device(self.user),
            status.HTTP_403_FORBIDDEN,
        )

    def test_retrieve_single_by_device_noauth(self):
        """Test retrieval by device without authentication."""
        noauth_client = APIClient()
        self.assertEqual(
            self._retrieve_single_by_device(noauth_client),
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_by_uuid(self):
        """Test listing of devices by UUID."""
        count = 5
        uuid, _, _ = self._register_device()
        self._post_multiple(self.user, self.data, count)
        self._post_multiple(
            self.admin, self._create_dummy_data(uuid=uuid), count
        )
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), count)

    def test_list_noauth(self):
        """Test listing of devices without authentication."""
        count = 5
        noauth_client = APIClient()
        self._post_multiple(self.user, self.data, count)
        response = noauth_client.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_device_owner(self):
        """Test listing as device owner."""
        count = 5
        self._post_multiple(self.user, self.data, count)
        response = self.user.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_radio_version(self):
        """Test creation and retrieval without radio version."""
        data = self._create_dummy_data(uuid=self.uuid)
        data.pop("radio_version")
        response = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNone(response.data["results"][0]["radio_version"])

    def test_radio_version_field(self):
        """Test retrieval of radio version field."""
        response = self.user.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["radio_version"],
            self.data["radio_version"],
        )

    def test_send_non_existent_time(self):
        """Test sending of heartbeat with non existent time.

        Test the resolution of a naive date-time in which the
        Europe/Amsterdam daylight saving time transition moved the time
        "forward".
        """
        data = self._create_dummy_data(uuid=self.uuid)
        # In 2017, the Netherlands changed from CET to CEST on March,
        # 26 at 02:00
        data["date"] = "2017-03-26 02:34:56"
        response = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_ambiguous_time(self):
        """Test sending of heartbeat with ambiguous time.

        Test the resolution of a naive date-time in which the
        Europe/Amsterdam daylight saving time transition moved the time
        "backward".
        """
        data = self._create_dummy_data(uuid=self.uuid)
        # In 2017, the Netherlands changed from CEST to CET on October,
        # 29 at 03:00
        data["date"] = "2017-10-29 02:34:56"
        response = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# pylint: disable=too-many-ancestors
class CrashreportListTestCase(HeartbeatListTestCase):
    """Test cases for crash reports."""

    LIST_CREATE_URL = "api_v1_crashreports"
    RETRIEVE_URL = "api_v1_crashreport"
    LIST_CREATE_BY_UUID_URL = "api_v1_crashreports_by_uuid"
    RETRIEVE_BY_UUID_URL = "api_v1_crashreport_by_uuid"

    @staticmethod
    def _create_dummy_data(**kwargs):
        return Dummy.crashreport_data(**kwargs)


class LogfileUploadTest(DeviceRegisterAPITestCase):
    """Test cases for upload of log files."""

    LIST_CREATE_URL = "api_v1_crashreports"
    PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"

    def _upload_crashreport(self, user, uuid):
        """
        Upload dummy crashreport data.

        Args:
            user: The user which should be used for uploading the report
            uuid: The uuid of the device to which the report should be uploaded

        Returns: The local id of the device for which the report was uploaded.

        """
        data = Dummy.crashreport_data(uuid=uuid)
        response = user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue("device_local_id" in response.data)
        device_local_id = response.data["device_local_id"]

        return device_local_id

    def _test_logfile_upload(self, user, uuid):
        # Upload crashreport
        device_local_id = self._upload_crashreport(user, uuid)

        # Upload a logfile for the crashreport
        logfile = tempfile.NamedTemporaryFile("w+", suffix=".log", delete=True)
        logfile.write(u"blihblahblub")
        response = user.post(
            reverse(
                self.PUT_LOGFILE_URL,
                args=[uuid, device_local_id, os.path.basename(logfile.name)],
            ),
            {"file": logfile},
            format="multipart",
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_logfile_upload_as_user(self):
        """Test upload of logfiles as device owner."""
        uuid, user, _ = self._register_device()
        self._test_logfile_upload(user, uuid)

    def test_logfile_upload_as_admin(self):
        """Test upload of logfiles as admin user."""
        uuid, _, _ = self._register_device()
        self._test_logfile_upload(self.admin, uuid)
