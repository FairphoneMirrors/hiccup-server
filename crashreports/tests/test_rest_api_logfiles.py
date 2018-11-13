"""Tests for the logfiles REST API."""

import os
import shutil
import tempfile
import zipfile

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import connection
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from crashreports.models import (
    crashreport_file_name,
    Device,
    Crashreport,
    LogFile,
)
from crashreports.tests.utils import (
    Dummy,
    RaceConditionsTestCase,
    HiccupCrashreportsAPITestCase,
)

LIST_CREATE_URL = "api_v1_crashreports"
PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(".hiccup-tests"))
class LogfileUploadTest(HiccupCrashreportsAPITestCase):
    """Test cases for upload of log files."""

    # pylint: disable=too-many-ancestors

    LIST_CREATE_URL = "api_v1_crashreports"
    PUT_LOGFILE_URL = "api_v1_putlogfile_for_device_id"
    POST_LOGFILE_URL = "api_v1_logfiles_by_id"

    def setUp(self):
        """Call the super setup method and register a device."""
        super().setUp()
        self.device_uuid, self.user, _ = self._register_device()

    def upload_crashreport(self, user, uuid):
        """
        Upload dummy crashreport data.

        Args:
            user: The user which should be used for uploading the report
            uuid: The uuid of the device to which the report should be uploaded

        Returns: The local id of the device for which the report was uploaded.

        """
        data = Dummy.crashreport_data(uuid=uuid)
        response = user.post(reverse(LIST_CREATE_URL), data)
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

    def upload_logfile(self, client, uuid, device_local_id):
        """Upload a log file and assert that it was created."""
        logfile = open(Dummy.DEFAULT_DUMMY_LOG_FILE_PATHS[0], "rb")
        logfile_name = os.path.basename(logfile.name)
        response = client.post(
            reverse(
                PUT_LOGFILE_URL, args=[uuid, device_local_id, logfile_name]
            ),
            {"file": logfile},
            format="multipart",
        )
        logfile.close()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        return response

    def _test_logfile_upload(self, user, uuid):
        # Upload crashreport
        device_local_id = self.upload_crashreport(user, uuid)

        # Upload a logfile for the crashreport
        self.upload_logfile(user, uuid, device_local_id)

        logfile_instance = (
            Device.objects.get(uuid=uuid)
            .crashreports.get(device_local_id=device_local_id)
            .logfiles.last()
        )
        uploaded_logfile_path = crashreport_file_name(
            logfile_instance,
            os.path.basename(Dummy.DEFAULT_DUMMY_LOG_FILE_PATHS[0]),
        )

        self.assertTrue(default_storage.exists(uploaded_logfile_path))
        # The files are not 100% equal, because the server adds some extra
        # bytes. However, we mainly care that the contents are equal:
        self._assert_zip_file_contents_equal(
            default_storage.path(uploaded_logfile_path),
            Dummy.DEFAULT_DUMMY_LOG_FILE_PATHS[0],
        )

    def test_logfile_upload_as_user(self):
        """Test upload of logfiles as device owner."""
        self._test_logfile_upload(self.user, self.device_uuid)

    def test_logfile_upload_as_fp_staff(self):
        """Test upload of logfiles as Fairphone staff user."""
        self._test_logfile_upload(self.fp_staff_client, self.device_uuid)

    def test_logfile_deletion(self):
        """Test deletion of logfile instances."""
        # Create a user, device and crashreport with logfile
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())
        crashreport = Dummy.create_dummy_report(Crashreport, device)
        logfile, logfile_path = Dummy.create_dummy_log_file_with_actual_file(
            crashreport
        )

        # Assert that the crashreport and logfile have been created
        self.assertEqual(Crashreport.objects.count(), 1)
        self.assertEqual(LogFile.objects.count(), 1)
        self.assertTrue(os.path.isfile(logfile_path))

        # Delete the logfile
        response = self.fp_staff_client.delete(
            reverse(self.POST_LOGFILE_URL, args=[logfile.id])
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Assert that the logfile has been deleted
        self.assertEqual(LogFile.objects.count(), 0)
        self.assertFalse(os.path.isfile(logfile_path))

    def tearDown(self):
        """Remove the file and directories that were created for the test."""
        shutil.rmtree(settings.MEDIA_ROOT)


class LogfileRaceConditionsTestCase(RaceConditionsTestCase):
    """Test cases for logfile race conditions."""

    def test_create_multiple_logfiles(self):
        """Test that no race condition occurs when creating logfiles."""
        uuid, user, _ = self._register_device()
        device_local_id = LogfileUploadTest.upload_crashreport(self, user, uuid)

        def upload_logfile(client, uuid, device_local_id):
            LogfileUploadTest.upload_logfile(
                self, client, uuid, device_local_id
            )
            connection.close()

        argslist = [[user, uuid, device_local_id] for _ in range(10)]

        self._test_create_multiple(
            LogFile, upload_logfile, argslist, "crashreport_local_id"
        )
