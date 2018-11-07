"""Tests for the crashreports REST API."""
from django.urls import reverse
from rest_framework import status

from crashreports.tests.utils import Dummy
from crashreports.tests.test_rest_api_heartbeats import HeartbeatsTestCase


class CrashreportsTestCase(HeartbeatsTestCase):
    """Test cases for crash reports."""

    # pylint: disable=too-many-ancestors

    LIST_CREATE_URL = "api_v1_crashreports"
    RETRIEVE_URL = "api_v1_crashreport"
    LIST_CREATE_BY_UUID_URL = "api_v1_crashreports_by_uuid"
    RETRIEVE_BY_UUID_URL = "api_v1_crashreport_by_uuid"

    @staticmethod
    def _create_dummy_data(**kwargs):
        return Dummy.crashreport_data(**kwargs)

    @staticmethod
    def _create_alternative_dummy_data(**kwargs):
        return Dummy.alternative_crashreport_data(**kwargs)

    def test_create_duplicate(self):
        """Test creation of a duplicate crashreport."""
        # Create a first crashreport
        report_data = self._create_dummy_data(uuid=self.uuid)
        response_first = self.user.post(
            reverse(self.LIST_CREATE_URL), report_data
        )
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)

        # Create a second crashreport for the same day and the same time
        response_second = self.user.post(
            reverse(self.LIST_CREATE_URL), report_data
        )
        self.assertEqual(response_second.status_code, status.HTTP_201_CREATED)

        # Assert that only one crashreport instance was created
        url = reverse(self.LIST_CREATE_BY_UUID_URL, args=[self.uuid])
        response = self.fp_staff_client.get(url)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_with_datetime(self):
        """Override to just pass because crashreports always use datetime."""
        pass
