from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
import datetime
import tempfile

# Create your tests here.


class DeviceTestCase(APITestCase):

    def setUp(self):
        self.url = "/hiccup/api/v1/devices/register/"

    def test(self):
        request = self.client.post(self.url, device_register_data)
        self.assertTrue("token" in request.data)
        self.assertTrue("uuid" in request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_missing_fields(self):
        request = self.client.post(self.url)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_board_date(self):
        request = self.client.post(self.url, {
            "board_date": device_register_data["board_date"]
        })
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_chipset(self):
        request = self.client.post(self.url, {
            "chipset": device_register_data["chipset"]
        })
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_board_date(self):
        request = self.client.post(self.url, {
            "board_date": "not_a_valid_date"
        })
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_non_existent_time_board_date(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "forward".
        """
        data = device_register_data.copy()
        # In 2017, the Netherlands changed from CET to CEST on March, 26 at 02:00
        data['board_date'] = '2017-03-26 02:34:56'
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_ambiguous_time_board_date(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "backward".
        """
        data = device_register_data.copy()
        # In 2017, the Netherlands changed from CEST to CET on October, 29 at 03:00
        data['board_date'] = '2017-10-29 02:34:56'
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


# Create your tests here.

device_register_data = {
 "board_date": str(datetime.datetime(year=2016, month=1, day=1)),
 "chipset": "chipset"

}
class ListDevicesTestCase(APITestCase):

    def setUp(self):
        self.password = "test"
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.uuid_to_retrieve = request.data['uuid']
        self.token_to_retrieve = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.uuid_to_delete = request.data['uuid']
        self.token_to_delete = request.data['token']

    def test_device_list(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.get("/hiccup/api/v1/devices/", {})
        self.assertTrue(request.data['results'][1]['uuid'] is not '')
        self.assertTrue(len(request.data['results']) >= 3)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        client.logout()

    def test_device_list_unauth(self):
        client = APIClient()
        request = client.get("/hiccup/api/v1/devices/", {})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_device_auth(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.get(
            "/hiccup/api/v1/devices/{}/".format(self.uuid_to_retrieve), {})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['uuid'],  str(self.uuid_to_retrieve))
        self.assertEqual(request.data['token'],  self.token_to_retrieve)
        client.logout()

    def test_retrieve_device_unauth(self):
        client = APIClient()
        request = client.get(
            "/hiccup/api/v1/devices/{}/".format(self.uuid_to_retrieve), {})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_device_auth(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        url = "/hiccup/api/v1/devices/{}/".format(self.uuid_to_delete)
        request = client.delete(
            url.format(self.uuid_to_delete), {})
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        request = client.delete(
            url.format(self.uuid_to_delete), {})
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        client.logout()


class HeartbeatListTestCase(APITestCase):

    def setUp(self):
        self.setup_users()
        self.data = self.create_dummy_data(self.uuid)
        self.url = "/hiccup/api/v1/heartbeats/"
        self.url_by_uuid = "/hiccup/api/v1/devices/{}/heartbeats/"

    def setup_users(self):
        self.password = "test"
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.other_uuid = request.data['uuid']
        self.other_token = request.data['token']
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        self.admin = APIClient()
        self.admin.login(username='myuser', password='test')
        self.user = APIClient()
        self.other_user = APIClient()
        self.user.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.other_user.credentials(HTTP_AUTHORIZATION='Token '
                                    + self.other_token)
        self.noauth_client = APIClient()

    def create_dummy_data(self, uuid="not set"):
        return {
            'uuid': uuid,
            'app_version': 2,
            'uptime': "2 Hours",
            'build_fingerprint': "models.CharField(max_length=200)",
            'radio_version': 'XXXX.X-FP2-X-XX',
            'date': str(datetime.datetime(year=2016, month=1, day=1))
        }

    def test_create_no_auth(self):
        request = self.noauth_client.post(self.url, self.data)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_as_admin(self):
        request = self.admin.post(self.url, self.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertTrue(request.data['id'] > 0)

    def test_create_as_admin_not_existing_device(self):
        request = self.admin.post(self.url,
                                  self.create_dummy_data())
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_as_uuid_owner(self):
        request = self.user.post(self.url,
                                 self.create_dummy_data(self.uuid))
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertTrue(request.data['id'] == -1)

    def test_create_as_uuid_not_owner(self):
        request = self.user.post(self.url,
                                 self.create_dummy_data(self.other_uuid))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def post_multiple(self, client, data, count=5):
        for i in range(count):
            client.post(self.url, data)

    def test_list(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.admin.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertTrue(len(request.data['results']) == count)

    def retrieve_single(self, user):
        count = 5
        self.post_multiple(self.user, self.data, count)
        url = "{}1/".format(self.url)
        request = user.get(url)
        return request.status_code

    def test_retrieve_single_admin(self):
        self.assertEqual(
            self.retrieve_single(self.admin),
            status.HTTP_200_OK)

    def test_retrieve_single_noauth(self):
        self.assertEqual(
            self.retrieve_single(self.user),
            status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_device_owner(self):
        self.assertEqual(
            self.retrieve_single(self.noauth_client),
            status.HTTP_401_UNAUTHORIZED)

    def retrieve_single_by_device(self, user):
        count = 5
        self.post_multiple(self.user, self.data, count)
        url = "{}1/".format(self.url_by_uuid.format(self.uuid))
        request = user.get(url)
        return request.status_code

    def test_retreive_single_by_device_admin(self):
        self.assertEqual(
            self.retrieve_single_by_device(self.admin),
            status.HTTP_200_OK)

    def test_retrieve_single_by_device_noauth(self):
        self.assertEqual(
            self.retrieve_single_by_device(self.user),
            status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_by_device_device_owner(self):
        self.assertEqual(
            self.retrieve_single_by_device(self.noauth_client),
            status.HTTP_401_UNAUTHORIZED)

    def test_list_by_uuid(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        self.post_multiple(self.admin, self.create_dummy_data(self.other_uuid),
                           count)
        url = self.url_by_uuid.format(self.uuid)
        request = self.admin.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertTrue(len(request.data['results']) == count)

    def test_list_noauth(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.noauth_client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_device_owner(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.user.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_radio_version(self):
        data = self.data.copy()
        data.pop('radio_version')
        self.post_multiple(self.user, data, 1)
        url = self.url_by_uuid.format(self.uuid)
        request = self.admin.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data['results']), 1)
        self.assertIsNone(request.data['results'][0]['radio_version'])

    def test_radio_version_field(self):
        self.post_multiple(self.user, self.data, 1)
        url = self.url_by_uuid.format(self.uuid)
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
        data = self.data.copy()
        # In 2017, the Netherlands changed from CET to CEST on March, 26 at 02:00
        data['date'] = '2017-03-26 02:34:56'
        request = self.user.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_send_ambiguous_time(self):
        """
        Test the resolution of a naive date-time in which the Europe/Amsterdam daylight saving
        time transition moved the time "backward".
        """
        data = self.data.copy()
        # In 2017, the Netherlands changed from CEST to CET on October, 29 at 03:00
        data['date'] = '2017-10-29 02:34:56'
        request = self.user.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


def create_crashreport(uuid="not set"):
    return {
        'uuid': uuid,
        'is_fake_report': 0,
        'app_version': 2,
        'uptime': "2 Hours",
        'build_fingerprint': "models.CharField(max_length=200)",
        'radio_version': 'XXXX.X-FP2-X-XX',
        'boot_reason': "models.CharField(max_length=200)",
        'power_on_reason': "models.CharField(max_length=200)",
        'power_off_reason': "models.CharField(max_length=200)",
        'date': str(datetime.datetime(year=2016, month=1, day=1))
    }


class CrashreportListTestCase(HeartbeatListTestCase):

    def setUp(self):
        self.setup_users()
        self.data = self.create_dummy_data(self.uuid)
        self.url = "/hiccup/api/v1/crashreports/"
        self.url_by_uuid = "/hiccup/api/v1/devices/{}/crashreports/"

    def create_dummy_data(self, uuid="not set"):
        return create_crashreport(uuid)


class LogfileUploadTest(APITestCase):
    def setUp(self):
        self.setup_users()
        # we need a device
        self.user.post("/hiccup/api/v1/crashreports/",
                       create_crashreport(self.uuid))
        self.user.post("/hiccup/api/v1/crashreports/",
                       create_crashreport(self.uuid))
        self.user.post("/hiccup/api/v1/crashreports/",
                       create_crashreport(self.other_uuid))
        self.user.post("/hiccup/api/v1/crashreports/",
                       create_crashreport(self.other_uuid))

    def setup_users(self):
        self.password = "test"
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", device_register_data)
        self.other_uuid = request.data['uuid']
        self.other_token = request.data['token']
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        self.user = APIClient()
        self.other_user = APIClient()
        self.user.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.other_user.credentials(HTTP_AUTHORIZATION='Token '
                                    + self.other_token)

    def get_url(self, uuid, report_id, filename):
        return ("/hiccup/api/v1/devices/{}/crashreports/{}/logfile_put/{}/".
                format(uuid, report_id, "test.log"))

    def test_Logfile_upload_as_admin(self):
        self.client.force_authenticate(self.admin)
        f = tempfile.NamedTemporaryFile('w+', suffix=".log", delete=True)
        f.write(u"blihblahblub")
        request = self.client.post(
            self.get_url(self.uuid, 1, f.name),
            {'file': f}, format="multipart")
        self.assertEqual(status.HTTP_201_CREATED, request.status_code)
