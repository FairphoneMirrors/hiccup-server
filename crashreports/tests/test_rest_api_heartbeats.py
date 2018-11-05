"""Tests for the heartbeats REST API."""

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from crashreports.tests.utils import HiccupCrashreportsAPITestCase, Dummy


class HeartbeatsTestCase(HiccupCrashreportsAPITestCase):
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
        response = self._post_multiple(self.fp_staff_client, self.data, count)
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

    def test_create_as_fp_staff(self):
        """Test creation as Fairphone staff."""
        response = self.fp_staff_client.post(
            reverse(self.LIST_CREATE_URL), self.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["id"] > 0)

    def test_create_as_fp_staff_not_existing_device(self):
        """Test creation of heartbeat on non-existing device."""
        response = self.fp_staff_client.post(
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
        response = self.fp_staff_client.get(reverse(self.LIST_CREATE_URL))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), count)

    def test_retrieve_single_fp_staff(self):
        """Test retrieval as Fairphone staff."""
        self.assertEqual(
            self._retrieve_single(self.fp_staff_client), status.HTTP_200_OK
        )

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

    def test_retrieve_single_by_device_fp_staff(self):
        """Test retrieval by device as Fairphone staff."""
        self.assertEqual(
            self._retrieve_single_by_device(self.fp_staff_client),
            status.HTTP_200_OK,
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
            self.fp_staff_client, self._create_dummy_data(uuid=uuid), count
        )
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.fp_staff_client.get(url)
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
        response = self.fp_staff_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNone(response.data["results"][0]["radio_version"])

    def test_radio_version_field(self):
        """Test retrieval of radio version field."""
        response = self.user.post(reverse(self.LIST_CREATE_URL), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.fp_staff_client.get(url)
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
