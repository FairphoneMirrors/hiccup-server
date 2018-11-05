"""Tests for the devices REST API."""

from django.urls import reverse

from rest_framework import status

from crashreports.tests.utils import HiccupCrashreportsAPITestCase, Dummy


class DeviceTestCase(HiccupCrashreportsAPITestCase):
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


class ListDevicesTestCase(HiccupCrashreportsAPITestCase):
    """Test cases for listing and deleting devices."""

    LIST_CREATE_URL = "api_v1_list_devices"
    RETRIEVE_URL = "api_v1_retrieve_device"

    def test_device_list(self):
        """Test registration of 2 devices."""
        number_of_devices = 2
        uuids = [
            str(self._register_device()[0]) for _ in range(number_of_devices)
        ]

        response = self.fp_staff_client.get(reverse(self.LIST_CREATE_URL), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), number_of_devices)
        for result in response.data["results"]:
            self.assertIn(result["uuid"], uuids)

    def test_device_list_unauth(self):
        """Test listing devices without authentication."""
        response = self.client.get(reverse(self.LIST_CREATE_URL), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_device_auth(self):
        """Test retrieval of devices as Fairphone staff user."""
        uuid, _, token = self._register_device()
        response = self.fp_staff_client.get(
            reverse(self.RETRIEVE_URL, args=[uuid]), {}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(uuid))
        self.assertEqual(response.data["token"], token)

    def test_retrieve_device_unauth(self):
        """Test retrieval of devices without authentication."""
        uuid, _, _ = self._register_device()
        response = self.client.get(reverse(self.RETRIEVE_URL, args=[uuid]), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_device_auth(self):
        """Test deletion of devices as Fairphone staff user."""
        uuid, _, _ = self._register_device()
        url = reverse(self.RETRIEVE_URL, args=[uuid])
        response = self.fp_staff_client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.fp_staff_client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
