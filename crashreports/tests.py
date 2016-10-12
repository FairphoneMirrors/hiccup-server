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
        self.password = "test"
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        # we need a device
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.other_uuid = request.data['uuid']
        self.other_token = request.data['token']
        self.data = self.create_dummy_data(self.uuid)
        self.url = "/hiccup/api/v1/heartbeats/"

    def create_dummy_data(self, uuid="not set"):
        return {
            'uuid': uuid,
            'app_version': 2,
            'uptime': "2 Hours",
            'build_fingerprint': "models.CharField(max_length=200)",
            'date': str(datetime.datetime(year=2016, month=1, day=1))
        }

    def test_create_no_auth(self):
        client = APIClient()
        request = client.post(self.url, self.data)
        self.assertEqual(request.status_code, 401)

    def test_create_as_admin(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.post(self.url, self.data)
        self.assertEqual(request.status_code, 201)
        client.logout()

    def test_create_as_admin_not_existing_device(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.post(self.url,
                              self.create_dummy_data())
        self.assertEqual(request.status_code, 404)
        client.logout()

    def test_create_as_uuid_owner(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        request = client.post(self.url,
                              self.create_dummy_data(self.uuid))
        self.assertEqual(request.status_code, 201)
        client.credentials()

    def test_create_as_uuid_not_owner(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        request = client.post(self.url,
                              self.create_dummy_data(self.other_uuid))
        self.assertEqual(request.status_code, 403)
        client.credentials()

    def post_heartbeats(self, client, heartbeat, count=5):
        for i in range(count):
            client.post(self.url, heartbeat)

    def test_list(self):
        count = 5
        client = APIClient()
        client.login(username='myuser', password='test')
        self.post_heartbeats(client, self.data, count)
        request = client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(request.data) >= count)
        client.logout()

    def test_list_noauth(self):
        count = 5
        client = APIClient()
        client.login(username='myuser', password='test')
        self.post_heartbeats(client, self.data, count)
        client.logout()
        request = client.get(self.url)
        self.assertEqual(request.status_code, 401)

    def test_list_device_owner(self):
        count = 5
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.post_heartbeats(client, self.data, count)
        request = client.get(self.url)
        client.logout()
        self.assertEqual(request.status_code, 403)


class CrashreportListTestCase(HeartbeatListTestCase):

    def setUp(self):
        self.password = "test"
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)
        # we need a device
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.uuid = request.data['uuid']
        self.token = request.data['token']
        request = self.client.post("/hiccup/api/v1/devices/register/", {})
        self.other_uuid = request.data['uuid']
        self.other_token = request.data['token']
        self.data = self.create_dummy_data(self.uuid)
        self.url = "/hiccup/api/v1/crashreports/"

    def create_dummy_data(self, uuid="not set"):
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
