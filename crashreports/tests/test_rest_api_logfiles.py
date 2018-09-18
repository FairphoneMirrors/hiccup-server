"""Tests for the logfiles REST API."""

import os
import tempfile

from django.urls import reverse

from rest_framework import status

from crashreports.tests.utils import HiccupCrashreportsAPITestCase, Dummy


class LogfileUploadTest(HiccupCrashreportsAPITestCase):
    """Test cases for upload of log files."""

    LIST_CREATE_URL = "api_v1_crashreports"
    PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"

    def _upload_crashreport(self, user, uuid):
        """
        Upload dummy crashreport data.

        Args:
            user: The user which should be used for uploading the report
            uuid: The uuid of the device to which the report should be uploaded

        Returns: The local id of the device for which the report was uploaded.

        """
        data = Dummy.crashreport_data(uuid=uuid)
        response = user.post(reverse(self.LIST_CREATE_URL), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue("device_local_id" in response.data)
        device_local_id = response.data["device_local_id"]

        return device_local_id

    def _test_logfile_upload(self, user, uuid):
        # Upload crashreport
        device_local_id = self._upload_crashreport(user, uuid)

        # Upload a logfile for the crashreport
        logfile = tempfile.NamedTemporaryFile("w+", suffix=".log", delete=True)
        logfile.write(u"blihblahblub")
        response = user.post(
            reverse(
                self.PUT_LOGFILE_URL,
                args=[uuid, device_local_id, os.path.basename(logfile.name)],
            ),
            {"file": logfile},
            format="multipart",
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_logfile_upload_as_user(self):
        """Test upload of logfiles as device owner."""
        uuid, user, _ = self._register_device()
        self._test_logfile_upload(user, uuid)

    def test_logfile_upload_as_admin(self):
        """Test upload of logfiles as admin user."""
        uuid, _, _ = self._register_device()
        self._test_logfile_upload(self.admin, uuid)
