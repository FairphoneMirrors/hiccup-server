import os
import tempfile

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from crashreports.models import Crashreport


class InvalidCrashTypeError(BaseException):
    """Invalid crash type encountered

    The valid crash type values (strings) are:
      - 'crash';
      - 'smpl';
      - 'other'.

    Args:
      - crash_type: The invalid crash type.
    """

    def __init__(self, crash_type):
        super(InvalidCrashTypeError, self).__init__(
            '{} is not a valid crash type'.format(crash_type))


class Dummy(object):
    DEFAULT_DUMMY_DEVICE_REGISTER_VALUES = {
        'board_date': '2015-12-15T01:23:45Z',
        'chipset': 'Qualcomm MSM8974PRO-AA',
    }

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        'uuid': None,
        'app_version': 10100,
        'uptime': (
            'up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, '
            'sleep time: 10 days, 20:46:27'),
        'build_fingerprint': (
            'Fairphone/FP2/FP2:6.0.1/FP2-gms-18.03.1/FP2-gms-18.03.1:user/'
            'release-keys'),
        'radio_version': '4437.1-FP2-0-08',
        'date': '2018-03-19T09:58:30.386Z',
    }

    DEFAULT_DUMMY_CRASHREPORTS_VALUES = DEFAULT_DUMMY_HEARTBEAT_VALUES.copy()
    DEFAULT_DUMMY_CRASHREPORTS_VALUES.update({
        'is_fake_report': 0,
        'boot_reason': 'why?',
        'power_on_reason': 'it was powered on',
        'power_off_reason': 'something happened and it went off',
    })

    CRASH_TYPE_TO_BOOT_REASON_MAP = {
        'crash': Crashreport.BOOT_REASON_KEYBOARD_POWER_ON,
        'smpl': Crashreport.BOOT_REASON_RTC_ALARM,
        'other': 'whatever',
    }

    @staticmethod
    def _update_copy(original, update):
        """Merge fields of update into a copy of original"""
        data = original.copy()
        data.update(update)
        return data

    @staticmethod
    def device_register_data(**kwargs):
        """
            Return the data required to register a device.

            Use the values passed as keyword arguments or default to
            the ones from `Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES`.
        """
        return Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES, kwargs)

    @staticmethod
    def heartbeat_data(**kwargs):
        """
            Return the data required to create a heartbeat.

            Use the values passed as keyword arguments or default to
            the ones from `Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES`.
        """
        return Dummy._update_copy(Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES, kwargs)

    @staticmethod
    def crashreport_data(report_type=None, **kwargs):
        """
            Return the data required to create a crashreport.

            Use the values passed as keyword arguments or default to
            the ones from `Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES`.

            Args:
                report_type (str, optional): A valid value from
                    `Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.keys()` that will
                    define the boot reason if not explicitly defined in the
                    keyword arguments already.
        """
        data = Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES, kwargs)
        if report_type and 'boot_reason' not in kwargs:
            if report_type not in Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP:
                raise InvalidCrashTypeError(report_type)
            data['boot_reason'] = Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.get(
                report_type)
        return data


class DeviceTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("api_v1_register_device")

    def test(self):
        request = self.client.post(self.url, Dummy.device_register_data())
        self.assertTrue("token" in request.data)
        self.assertTrue("uuid" in request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_missing_fields(self):
        request = self.client.post(self.url)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_board_date(self):
        data = Dummy.device_register_data()
        data.pop('board_date')
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_chipset(self):
        data = Dummy.device_register_data()
        data.pop('chipset')
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_board_date(self):
        data = Dummy.device_register_data()
        data['board_date'] = 'not_a_valid_date'
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_non_existent_time_board_date(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "forward".
        """
        data = Dummy.device_register_data()
        # In 2017, the Netherlands changed from CET to CEST on March, 26 at 02:00
        data['board_date'] = '2017-03-26 02:34:56'
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_ambiguous_time_board_date(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "backward".
        """
        data = Dummy.device_register_data()
        # In 2017, the Netherlands changed from CEST to CET on October, 29 at 03:00
        data['board_date'] = '2017-10-29 02:34:56'
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class DeviceRegisterAPITestCase(APITestCase):
    """Base class that offers device registration as well as base users

    Attributes:
        number_of_devices_created (int): The number of devices created in the
            database.
    """

    REGISTER_DEVICE_URL = "api_v1_register_device"

    def setUp(self):
        self.number_of_devices_created = 0

        _, response_data = self._register_device()
        self.uuid = response_data['uuid']
        self.token = response_data['token']
        self.user = APIClient()
        self.user.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        _, response_data = self._register_device()
        self.other_uuid = response_data['uuid']
        self.other_token = response_data['token']
        self.other_user = APIClient()
        self.other_user.credentials(
            HTTP_AUTHORIZATION='Token ' + self.other_token)

        self.noauth_client = APIClient()

        self.admin_user = User.objects.create_superuser(
            'somebody', 'somebody@example.com', 'thepassword')
        self.admin = APIClient()
        self.admin.force_authenticate(self.admin_user)

    def _register_device(self, **kwargs):
        """Register a new device

        Arguments:
            **kwargs: The data to pass the dummy data creation
                method `Dummy.device_register_data`.
        Returns:
            (dict(str, str), dict(str, str)): The tuple composed of the device
            data that was used for the registration and the data returned by
            the server in return.
        """
        data = Dummy.device_register_data(**kwargs)
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.number_of_devices_created += 1

        return (data, response.data)


class ListDevicesTestCase(DeviceRegisterAPITestCase):

    LIST_CREATE_URL = "api_v1_list_devices"
    RETRIEVE_URL = "api_v1_retrieve_device"

    def test_device_list(self):
        request = self.admin.get(reverse(self.LIST_CREATE_URL), {})
        self.assertIsNot(request.data['results'][1]['uuid'], '')
        self.assertEqual(
            len(request.data['results']), self.number_of_devices_created)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_device_list_unauth(self):
        request = self.client.get(reverse(self.LIST_CREATE_URL), {})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_device_auth(self):
        request = self.admin.get(
            reverse(self.RETRIEVE_URL, args=[self.uuid]), {})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['uuid'], str(self.uuid))
        self.assertEqual(request.data['token'], self.token)

    def test_retrieve_device_unauth(self):
        request = self.client.get(
            reverse(self.RETRIEVE_URL, args=[self.uuid]), {})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_device_auth(self):
        url = reverse(self.RETRIEVE_URL, args=[self.other_uuid])
        request = self.admin.delete(url, {})
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        request = self.admin.delete(url, {})
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


class HeartbeatListTestCase(DeviceRegisterAPITestCase):

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
            for _ in range(count)]

    def _retrieve_single(self, user):
        count = 5
        requests = self._post_multiple(self.admin, self.data, count)
        self.assertEqual(len(requests), count)
        self.assertEqual(requests[0].status_code, status.HTTP_201_CREATED)
        url = reverse(self.RETRIEVE_URL, args=[requests[0].data['id']])
        request = user.get(url)
        return request.status_code

    def _retrieve_single_by_device(self, user):
        count = 5
        requests = self._post_multiple(self.user, self.data, count)
        self.assertEqual(len(requests), count)
        self.assertEqual(requests[0].status_code, status.HTTP_201_CREATED)
        url = reverse(self.RETRIEVE_BY_UUID_URL, args=[
            self.uuid, requests[0].data['device_local_id']])
        request = user.get(url)
        return request.status_code

    def setUp(self):
        super(HeartbeatListTestCase, self).setUp()
        self.data = self._create_dummy_data(uuid=self.uuid)

    def test_create_no_auth(self):
        request = self.noauth_client.post(
            reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_as_admin(self):
        request = self.admin.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertTrue(request.data['id'] > 0)

    def test_create_as_admin_not_existing_device(self):
        request = self.admin.post(
            reverse(self.LIST_CREATE_URL), self._create_dummy_data())
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_as_uuid_owner(self):
        request = self.user.post(
            reverse(self.LIST_CREATE_URL),
            self._create_dummy_data(uuid=self.uuid))
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['id'], -1)

    def test_create_as_uuid_not_owner(self):
        request = self.user.post(
            reverse(self.LIST_CREATE_URL),
            self._create_dummy_data(uuid=self.other_uuid))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        count = 5
        self._post_multiple(self.user, self.data, count)
        request = self.admin.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data['results']), count)

    def test_retrieve_single_admin(self):
        self.assertEqual(
            self._retrieve_single(self.admin), status.HTTP_200_OK)

    def test_retrieve_single_device_owner(self):
        self.assertEqual(
            self._retrieve_single(self.user), status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_noauth(self):
        self.assertEqual(
            self._retrieve_single(self.noauth_client),
            status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_single_by_device_admin(self):
        self.assertEqual(
            self._retrieve_single_by_device(self.admin), status.HTTP_200_OK)

    def test_retrieve_single_by_device_device_owner(self):
        self.assertEqual(
            self._retrieve_single_by_device(self.user),
            status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_by_device_noauth(self):
        self.assertEqual(
            self._retrieve_single_by_device(self.noauth_client),
            status.HTTP_401_UNAUTHORIZED)

    def test_list_by_uuid(self):
        count = 5
        self._post_multiple(self.user, self.data, count)
        self._post_multiple(
            self.admin, self._create_dummy_data(uuid=self.other_uuid), count)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        request = self.admin.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data['results']), count)

    def test_list_noauth(self):
        count = 5
        self._post_multiple(self.user, self.data, count)
        request = self.noauth_client.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_device_owner(self):
        count = 5
        self._post_multiple(self.user, self.data, count)
        request = self.user.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_radio_version(self):
        data = self._create_dummy_data(uuid=self.uuid)
        data.pop('radio_version')
        request = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        request = self.admin.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data['results']), 1)
        self.assertIsNone(request.data['results'][0]['radio_version'])

    def test_radio_version_field(self):
        request = self.user.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        request = self.admin.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data['results']), 1)
        self.assertEqual(request.data['results'][0]['radio_version'],
                self.data['radio_version'])

    def test_send_non_existent_time(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "forward".
        """
        data = self._create_dummy_data(uuid=self.uuid)
        # In 2017, the Netherlands changed from CET to CEST on March, 26 at 02:00
        data['date'] = '2017-03-26 02:34:56'
        request = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_send_ambiguous_time(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "backward".
        """
        data = self._create_dummy_data(uuid=self.uuid)
        # In 2017, the Netherlands changed from CEST to CET on October, 29 at 03:00
        data['date'] = '2017-10-29 02:34:56'
        request = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class CrashreportListTestCase(HeartbeatListTestCase):

    LIST_CREATE_URL = "api_v1_crashreports"
    RETRIEVE_URL = "api_v1_crashreport"
    LIST_CREATE_BY_UUID_URL = "api_v1_crashreports_by_uuid"
    RETRIEVE_BY_UUID_URL = "api_v1_crashreport_by_uuid"

    @staticmethod
    def _create_dummy_data(**kwargs):
        return Dummy.crashreport_data(**kwargs)


class LogfileUploadTest(DeviceRegisterAPITestCase):

    LIST_CREATE_URL = "api_v1_crashreports"
    PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"

    def setUp(self):
        super(LogfileUploadTest, self).setUp()

        url = reverse(self.LIST_CREATE_URL)
        for uuid in [self.uuid, self.other_uuid]:
            data = Dummy.crashreport_data(uuid=uuid)
            for _ in range(2):
                self.user.post(url, data)

    def test_Logfile_upload_as_admin(self):
        f = tempfile.NamedTemporaryFile('w+', suffix=".log", delete=True)
        f.write(u"blihblahblub")
        request = self.admin.post(
            reverse(self.PUT_LOGFILE_URL, args=[
                self.uuid, 1, os.path.basename(f.name)
            ]),
            {'file': f}, format="multipart")
        self.assertEqual(status.HTTP_201_CREATED, request.status_code)
