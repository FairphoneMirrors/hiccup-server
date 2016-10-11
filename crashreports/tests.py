from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate

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
        request = client.delete(url, {})
        # self.assertEqual(request.status_code, 204)
        # request = client.delete("/hiccup/api/v1/devices/{}/".format(self.uuid_to_delete),{})
        # self.assertEqual(request.status_code, 404)
        client.logout()

import datetime


def create_dummy_crash_report(uuid="not set"):
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

from crashreports.models import Crashreport

class CreateCrashreportTestCase(APITestCase):

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
        self.crashreport = create_dummy_crash_report(self.uuid)

    def test_create_crashreport_no_auth(self):
        client = APIClient()
        request = client.post("/hiccup/api/v1/crashreports/", self.crashreport)
        self.assertEqual(request.status_code, 401)

    def test_create_crashreport_as_admin(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.post("/hiccup/api/v1/crashreports/", self.crashreport)
        self.assertEqual(request.status_code, 201)
        client.logout()

    def test_create_crashreport_as_admin_not_existing_device(self):
        client = APIClient()
        client.login(username='myuser', password='test')
        request = client.post("/hiccup/api/v1/crashreports/", create_dummy_crash_report())
        self.assertEqual(request.status_code, 404)
        client.logout()
        
    def test_create_crashreport_as_uuid_owner(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        request = client.post("/hiccup/api/v1/crashreports/",  create_dummy_crash_report(self.uuid))
        self.assertEqual(request.status_code, 201)
        client.credentials()
    
    def test_create_crashreport_as_uuid_not_owner(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        request = client.post("/hiccup/api/v1/crashreports/",  create_dummy_crash_report(self.other_uuid))
        self.assertEqual(request.status_code, 403) 
        client.credentials()
