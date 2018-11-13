"""Tests for the heartbeats REST API."""
from datetime import timedelta, datetime

import pytz
from django.db import connection
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from crashreports.tests.utils import (
    Dummy,
    RaceConditionsTestCase,
    HiccupCrashreportsAPITestCase,
)
from crashreports.models import HeartBeat


class HeartbeatsTestCase(HiccupCrashreportsAPITestCase):
    """Test cases for heartbeats."""

    # pylint: disable=too-many-public-methods,too-many-ancestors

    LIST_CREATE_URL = "api_v1_heartbeats"
    RETRIEVE_URL = "api_v1_heartbeat"
    LIST_CREATE_BY_UUID_URL = "api_v1_heartbeats_by_uuid"
    RETRIEVE_BY_UUID_URL = "api_v1_heartbeat_by_uuid"

    @staticmethod
    def _create_dummy_data(**kwargs):
        return Dummy.heartbeat_data(**kwargs)

    @staticmethod
    def _create_alternative_dummy_data(**kwargs):
        return Dummy.alternative_heartbeat_data(**kwargs)

    def _post_multiple(self, client, data, count):
        """Send multiple POST requests to create reports.

        Note that the date of the data will be adapted for each POST request
        so that no duplicate reports are being created. However, the given
        `data` parameter value will not be modified.

        Args:
            client: The client used for sending the requests
            data: The data that is sent each request
            count: The number of requests that should be made

        Returns: A list of HTTP response objects

        """
        results = []
        data_to_send = data.copy()
        for i in range(count):
            data_to_send["date"] += timedelta(days=i)
            results.append(
                client.post(reverse(self.LIST_CREATE_URL), data_to_send)
            )

        return results

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
            reverse(self.LIST_CREATE_URL),
            self._create_dummy_data(uuid=Dummy.UUIDs[0]),
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

    def test_create_duplicate(self):
        """Test creation of a duplicate Heartbeat."""
        # Create a first Heartbeat
        report_data = self._create_dummy_data(uuid=self.uuid)
        response_first = self.user.post(
            reverse(self.LIST_CREATE_URL), report_data
        )
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)

        # Create a second heartbeat for the same day
        response_second = self.user.post(
            reverse(self.LIST_CREATE_URL), report_data
        )
        self.assertEqual(response_second.status_code, status.HTTP_201_CREATED)

        # Assert that only one heartbeat instance was created
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.fp_staff_client.get(url)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_duplicate_different_values(self):
        """Test creation of a duplicate Heartbeat with different values."""
        # Create a first Heartbeat
        report_1_data = self._create_dummy_data(uuid=self.uuid)
        response_first = self.user.post(
            reverse(self.LIST_CREATE_URL), report_1_data
        )
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)

        # Create a second heartbeat for the same day with all different
        # values except for the date and UUID
        report_2_data = self._create_alternative_dummy_data(uuid=self.uuid)
        response_second = self.user.post(
            reverse(self.LIST_CREATE_URL), report_2_data
        )
        self.assertEqual(response_second.status_code, status.HTTP_201_CREATED)

        # Assert that only one heartbeat instance was created
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.fp_staff_client.get(url)
        self.assertEqual(len(response.data["results"]), 1)

        # Assert that the values are all the same as of the first heartbeat, as
        # we are dropping all incoming duplicates (we need to ignore the `id`
        # because its value is set to -1 in the response for creating reports)
        self.assertTrue(
            {k: v for k, v in response.data["results"][0].items() if k != "id"}
            == {k: v for k, v in response_first.data.items() if k != "id"}
        )

    def test_create_with_datetime(self):
        """Test creation of heartbeats with datetime instead of date value.

        Initially, the 'date' field of the HeartBeat model was a datetime
        field but now has been changed to a date field. However, Hiccup clients
        are still sending datetime values which also need to be accepted and
        processed by the server.
        """
        data = self._create_dummy_data(uuid=self.uuid)
        data["date"] = datetime(2018, 3, 19, 12, 0, 0, tzinfo=pytz.utc)

        response = self.user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["date"], str(data["date"].date()))


class HeartBeatRaceConditionsTestCase(RaceConditionsTestCase):
    """Test cases for heartbeat race conditions."""

    LIST_CREATE_URL = "api_v1_heartbeats"

    def test_create_multiple_heartbeats(self):
        """Test that no race condition occurs when creating heartbeats."""
        uuid, user, _ = self._register_device()

        def upload_report(client, data):
            response = client.post(reverse(self.LIST_CREATE_URL), data)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)
            connection.close()

        data = Dummy.heartbeat_data(uuid=uuid)
        argslist = [
            [user, dict(data, date=data["date"] + timedelta(days=i))]
            for i in range(10)
        ]

        self._test_create_multiple(
            HeartBeat, upload_report, argslist, "device_local_id"
        )
