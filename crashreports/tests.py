from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import datetime

# Create your tests here.


class DeviceTestCase(APITestCase):

    def setUp(self):
        pass

    def test(self):
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.assertTrue("token" in request.data)
        self.assertTrue("uuid" in request.data)
        self.assertEqual(request.status_code, 200)

# Create your tests here.


class ListDevicesTestCase(APITestCase):

    def setUp(self):
        self.password = "test"
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        self.client.post("/hiccup/api/v1/devices/register/", {})
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid_to_retrieve = request.data['uuid']
        self.token_to_retrieve = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid_to_delete = request.data['uuid']
        self.token_to_delete = request.data['token']

    def test_device_list(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.get("/hiccup/api/v1/devices/", {})
        self.assertTrue("uuid" in request.data[1])
        self.assertTrue(len(request.data) >= 3)
        self.assertEqual(request.status_code, 200)
        client.logout()

    def test_device_list_unauth(self):
        client = APIClient()
        request = client.get("/hiccup/api/v1/devices/", {})
        self.assertEqual(request.status_code, 401)

    def test_retrieve_device_auth(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.get(
            "/hiccup/api/v1/devices/{}/".format(self.uuid_to_retrieve), {})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['uuid'],  str(self.uuid_to_retrieve))
        self.assertEqual(request.data['token'],  self.token_to_retrieve)
        client.logout()

    def test_retrieve_device_unauth(self):
        client = APIClient()
        request = client.get(
            "/hiccup/api/v1/devices/{}/".format(self.uuid_to_retrieve), {})
        self.assertEqual(request.status_code, 401)

    def test_delete_device_auth(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        url = "/hiccup/api/v1/devices/{}/".format(self.uuid_to_delete)
        request = client.delete(
            url.format(self.uuid_to_delete), {})
        self.assertEqual(request.status_code, 204)
        request = client.delete(
            url.format(self.uuid_to_delete), {})
        self.assertEqual(request.status_code, 404)
        client.logout()


class HeartbeatListTestCase(APITestCase):

    def setUp(self):
        self.setup_users()
        self.data = self.create_dummy_data(self.uuid)
        self.url = "/hiccup/api/v1/heartbeats/"
        self.url_by_uuid = "/hiccup/api/v1/devices/{}/heartbeats/"

    def setup_users(self):
        self.password = "test"
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
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
            'date': str(datetime.datetime(year=2016, month=1, day=1))
        }

    def test_create_no_auth(self):
        request = self.noauth_client.post(self.url, self.data)
        self.assertEqual(request.status_code, 401)

    def test_create_as_admin(self):
        request = self.admin.post(self.url, self.data)
        self.assertEqual(request.status_code, 201)
        self.assertTrue(request.data['id'] > 0)

    def test_create_as_admin_not_existing_device(self):
        request = self.admin.post(self.url,
                                  self.create_dummy_data())
        self.assertEqual(request.status_code, 404)

    def test_create_as_uuid_owner(self):
        request = self.user.post(self.url,
                                 self.create_dummy_data(self.uuid))
        self.assertEqual(request.status_code, 201)
        self.assertTrue(request.data['id'] == -1)

    def test_create_as_uuid_not_owner(self):
        request = self.user.post(self.url,
                                 self.create_dummy_data(self.other_uuid))
        self.assertEqual(request.status_code, 403)

    def post_multiple(self, client, data, count=5):
        for i in range(count):
            client.post(self.url, data)

    def test_list(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.admin.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(request.data) == count)

    def test_retrieve_single(self, user=None, expected_result=200):
        count = 5
        if user is None:
            user = self.admin
        self.post_multiple(self.user, self.data, count)
        url = "{}1/".format(self.url)
        request = user.get(url)
        self.assertEqual(request.status_code, expected_result)

    def test_retrieve_single_noauth(self):
        self.test_retrieve_single(user=self.user, expected_result=403)

    def test_retrieve_single_device_owner(self):
        self.test_retrieve_single(self.noauth_client, 401)

    def test_list_by_uuid(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        self.post_multiple(self.admin, self.create_dummy_data(self.other_uuid),
                           count)
        url = self.url_by_uuid.format(self.uuid)
        request = self.admin.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(request.data) == count)

    def test_list_noauth(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.noauth_client.get(self.url)
        self.assertEqual(request.status_code, 401)

    def test_list_device_owner(self):
        count = 5
        self.post_multiple(self.user, self.data, count)
        request = self.user.get(self.url)
        self.assertEqual(request.status_code, 403)


def create_crashreport(uuid="not set"):
    return {
        'uuid': uuid,
        'is_fake_report': 0,
        'app_version': 2,
        'uptime': "2 Hours",
        'build_fingerprint': "models.CharField(max_length=200)",
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
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
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

    def test_Logfile_upload_as_admin(self):
        pass
