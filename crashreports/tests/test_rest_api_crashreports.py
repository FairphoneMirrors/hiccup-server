"""Tests for the crashreports REST API."""

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
