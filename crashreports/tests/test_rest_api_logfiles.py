"""Tests for the logfiles REST API."""

import os
import shutil
import tempfile
import zipfile

from django.conf import settings
from django.core.files.storage import default_storage
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from crashreports.models import crashreport_file_name, Device
from crashreports.tests.utils import HiccupCrashreportsAPITestCase, Dummy


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(".hiccup-tests"))
class LogfileUploadTest(HiccupCrashreportsAPITestCase):
    """Test cases for upload of log files."""

    LIST_CREATE_URL = "api_v1_crashreports"
    PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"

    def setUp(self):
        """Call the super setup method and register a device."""
        super().setUp()
        self.device_uuid, self.user, _ = self._register_device()

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

    def _assert_zip_file_contents_equal(self, file1, file2):
        """Assert that the files within two zip files are equal."""
        zip_file_1 = zipfile.ZipFile(file1)
        zip_file_2 = zipfile.ZipFile(file2)
        for file_name_1, file_name_2 in zip(
            zip_file_1.filelist, zip_file_2.filelist
        ):
            file_1 = zip_file_1.open(file_name_1)
            file_2 = zip_file_2.open(file_name_2)

            self.assertEqual(file_1.read(), file_2.read())

    def _test_logfile_upload(self, user, uuid):
        # Upload crashreport
        device_local_id = self._upload_crashreport(user, uuid)

        # Upload a logfile for the crashreport
        logfile = open(Dummy.DEFAULT_DUMMY_LOG_FILE_PATH, "rb")

        logfile_name = os.path.basename(logfile.name)
        response = user.post(
            reverse(
                self.PUT_LOGFILE_URL, args=[uuid, device_local_id, logfile_name]
            ),
            {"file": logfile},
            format="multipart",
        )
        logfile.close()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        logfile_instance = (
            Device.objects.get(uuid=uuid)
            .crashreports.get(device_local_id=device_local_id)
            .logfiles.last()
        )
        uploaded_logfile_path = crashreport_file_name(
            logfile_instance, logfile_name
        )

        self.assertTrue(default_storage.exists(uploaded_logfile_path))
        # The files are not 100% equal, because the server adds some extra
        # bytes. However, we mainly care that the contents are equal:
        self._assert_zip_file_contents_equal(
            default_storage.path(uploaded_logfile_path),
            Dummy.DEFAULT_DUMMY_LOG_FILE_PATH,
        )

    def test_logfile_upload_as_user(self):
        """Test upload of logfiles as device owner."""
        self._test_logfile_upload(self.user, self.device_uuid)

    def test_logfile_upload_as_fp_staff(self):
        """Test upload of logfiles as Fairphone staff user."""
        self._test_logfile_upload(self.fp_staff_client, self.device_uuid)

    def tearDown(self):
        """Remove the file and directories that were created for the test."""
        shutil.rmtree(settings.MEDIA_ROOT)
