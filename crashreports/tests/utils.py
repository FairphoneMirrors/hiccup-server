"""Utility functions shared by all crashreports tests."""

import os
import shutil
import threading
import zipfile
from datetime import date, datetime
from typing import Optional

import pytz
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from crashreports.models import (
    Crashreport,
    Device,
    HeartBeat,
    LogFile,
    crashreport_file_name,
)
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


class InvalidCrashTypeError(BaseException):
    """Invalid crash type encountered.

    The valid crash type values (strings) are:
      - 'crash';
      - 'smpl';
      - 'other'.

    Args:
      - crash_type: The invalid crash type.
    """

    def __init__(self, crash_type):
        """Initialise the exception using the crash type to build a message.

        Args:
            crash_type: The invalid crash type.
        """
        super(InvalidCrashTypeError, self).__init__(
            "{} is not a valid crash type".format(crash_type)
        )


class Dummy:
    """Dummy values for devices, heartbeats and crashreports."""

    # Valid unique entries
    BUILD_FINGERPRINTS = [
        (
            "Fairphone/FP2/FP2:5.1/FP2/r4275.1_FP2_gms76_1.13.0"
            ":user/release-keys"
        ),
        (
            "Fairphone/FP2/FP2:5.1.1/FP2-gms75.1.13.0/FP2-gms75.1.13.0"
            ":user/release-keys"
        ),
        (
            "Fairphone/FP2/FP2:6.0.1/FP2-gms-18.04.1/FP2-gms-18.04.1"
            ":user/release-keys"
        ),
        ("Fairphone/FP2/FP2:7.1.2/18.07.2/gms-7480c31d:user/release-keys"),
    ]
    RADIO_VERSIONS = [
        "4437.1-FP2-0-07",
        "4437.1-FP2-0-08",
        "4437.1-FP2-0-09",
        "4437.1-FP2-0-10",
    ]
    UUIDs = ["e1c0cc95-ab8d-461a-a768-cb8d9d7fdb04"]

    USERNAMES = ["testuser1", "testuser2", "testuser3", "testuser4"]

    DATES = [date(2018, 3, 19), date(2018, 3, 26), date(2018, 5, 1)]

    DEFAULT_USER_VALUES = {"username": USERNAMES[0]}

    DEFAULT_DEVICE_REGISTER_VALUES = {
        "board_date": datetime(2015, 12, 15, 1, 23, 45, tzinfo=pytz.utc),
        "chipset": "Qualcomm MSM8974PRO-AA",
    }

    DEFAULT_DEVICE_VALUES = DEFAULT_DEVICE_REGISTER_VALUES.copy()
    DEFAULT_DEVICE_VALUES.update(
        {"token": "64111c62d521fb4724454ca6dea27e18f93ef56e"}
    )

    DEFAULT_HEARTBEAT_VALUES = {
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "radio_version": RADIO_VERSIONS[0],
        "date": date(2018, 3, 19),
    }

    ALTERNATIVE_HEARTBEAT_VALUES = {
        "app_version": 10101,
        "uptime": (
            "up time: 2 days, 12:39:13, idle time: 2 days, 11:35:01, "
            "sleep time: 2 days, 11:56:12"
        ),
        "build_fingerprint": BUILD_FINGERPRINTS[1],
        "radio_version": RADIO_VERSIONS[1],
        "date": date(2018, 3, 19),
    }

    DEFAULT_CRASHREPORT_VALUES = DEFAULT_HEARTBEAT_VALUES.copy()
    DEFAULT_CRASHREPORT_VALUES.update(
        {
            "is_fake_report": False,
            "boot_reason": Crashreport.BOOT_REASON_UNKOWN,
            "power_on_reason": "it was powered on",
            "power_off_reason": "something happened and it went off",
            "date": datetime(2018, 3, 19, 12, 0, 0, tzinfo=pytz.utc),
        }
    )

    ALTERNATIVE_CRASHREPORT_VALUES = ALTERNATIVE_HEARTBEAT_VALUES.copy()
    ALTERNATIVE_CRASHREPORT_VALUES.update(
        {
            "is_fake_report": True,
            "boot_reason": Crashreport.BOOT_REASON_KEYBOARD_POWER_ON,
            "power_on_reason": "alternative power on reason",
            "power_off_reason": "alternative power off reason",
            "date": datetime(2018, 3, 19, 12, 0, 0, tzinfo=pytz.utc),
        }
    )

    DEFAULT_LOG_FILE_NAME = "dmesg.log"

    CRASH_TYPE_TO_BOOT_REASON_MAP = {
        "crash": Crashreport.BOOT_REASON_KEYBOARD_POWER_ON,
        "smpl": Crashreport.BOOT_REASON_RTC_ALARM,
        "other": "whatever",
    }

    DEFAULT_LOG_FILE_FILENAMES = ["test_logfile_1.zip", "test_logfile_2.zip"]
    DEFAULT_LOG_FILE_DIRECTORY = os.path.join("resources", "test")

    DEFAULT_LOG_FILE_VALUES = {
        "logfile_type": "last_kmsg",
        "logfile": DEFAULT_LOG_FILE_FILENAMES[0],
    }

    DEFAULT_LOG_FILE_PATHS = [
        os.path.join(DEFAULT_LOG_FILE_DIRECTORY, DEFAULT_LOG_FILE_FILENAMES[0]),
        os.path.join(DEFAULT_LOG_FILE_DIRECTORY, DEFAULT_LOG_FILE_FILENAMES[1]),
    ]

    @staticmethod
    def _update_copy(original, update):
        """Merge fields of update into a copy of original."""
        data = original.copy()
        data.update(update)
        return data

    @staticmethod
    def device_register_data(**kwargs):
        """Return the data required to register a device.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DEVICE_REGISTER_VALUES`.
        """
        return Dummy._update_copy(Dummy.DEFAULT_DEVICE_REGISTER_VALUES, kwargs)

    @staticmethod
    def heartbeat_data(**kwargs):
        """Return the data required to create a heartbeat.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_HEARTBEAT_VALUES`.
        """
        return Dummy._update_copy(Dummy.DEFAULT_HEARTBEAT_VALUES, kwargs)

    @staticmethod
    def alternative_heartbeat_data(**kwargs):
        """Return the alternative data required to create a heartbeat.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.ALTERNATIVE_HEARTBEAT_VALUES`.
        """
        return Dummy._update_copy(Dummy.ALTERNATIVE_HEARTBEAT_VALUES, kwargs)

    @staticmethod
    def crashreport_data(report_type: Optional[str] = None, **kwargs):
        """Return the data required to create a crashreport.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_CRASHREPORTS_VALUES`.

        Args:
            report_type: A valid value from
                `Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.keys()` that will
                define the boot reason if not explicitly defined in the
                keyword arguments already.
        """
        data = Dummy._update_copy(Dummy.DEFAULT_CRASHREPORT_VALUES, kwargs)
        if report_type and "boot_reason" not in kwargs:
            if report_type not in Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP:
                raise InvalidCrashTypeError(report_type)
            data["boot_reason"] = Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.get(
                report_type
            )
        return data

    @staticmethod
    def alternative_crashreport_data(**kwargs):
        """Return the alternative data required to create a crashreport.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.ALTERNATIVE_CRASHREPORT_VALUES`.
        """
        return Dummy._update_copy(Dummy.ALTERNATIVE_CRASHREPORT_VALUES, kwargs)

    @staticmethod
    def create_user(**kwargs):
        """Create a dummy user instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created user instance.

        """
        entity = User(**Dummy._update_copy(Dummy.DEFAULT_USER_VALUES, kwargs))
        entity.save()
        return entity

    @staticmethod
    def create_device(user, **kwargs):
        """Create a dummy device instance.

        The dummy instance is created and saved to the database.
        Args:
            user: The user instance that the device should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created device instance.

        """
        entity = Device(
            user=user, **Dummy._update_copy(Dummy.DEFAULT_DEVICE_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_report(report_type, device, **kwargs):
        """Create a dummy report instance of the given report class type.

        The dummy instance is created and saved to the database.
        Args:
            report_type: The class of the report type to be created.
            user: The device instance that the heartbeat should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created report instance.

        Raises:
            RuntimeError: If report_type is not a report class type.

        """
        if report_type == HeartBeat:
            entity = HeartBeat(
                device=device,
                **Dummy._update_copy(Dummy.DEFAULT_HEARTBEAT_VALUES, kwargs)
            )
        elif report_type == Crashreport:
            entity = Crashreport(
                device=device,
                **Dummy._update_copy(Dummy.DEFAULT_CRASHREPORT_VALUES, kwargs)
            )
        else:
            raise RuntimeError(
                "No dummy report instance can be created for {}".format(
                    report_type.__name__
                )
            )
        entity.save()
        return entity

    @staticmethod
    def create_log_file(crashreport, **kwargs):
        """Create a dummy log file instance.

        The dummy instance is created and saved to the database.

        Args:
            crashreport: The crashreport that the log file belongs to.
            **kwargs: Optional arguments to extend/overwrite the default values.

        Returns: The created log file instance.

        """
        entity = LogFile(
            crashreport=crashreport,
            **Dummy._update_copy(Dummy.DEFAULT_LOG_FILE_VALUES, kwargs)
        )

        entity.save()
        return entity

    @staticmethod
    def create_log_file_with_actual_file(crashreport, **kwargs):
        """Create a dummy log file instance along with a file.

        The dummy instance is created and saved to the database. The log file
        is copied to the respective location in the media directory.

        Args:
            crashreport: The crashreport that the log file belongs to.
            **kwargs: Optional arguments to extend/overwrite the default values.

        Returns: The created log file instance and the path to the copied file.

        """
        logfile = Dummy.create_log_file(crashreport, **kwargs)
        logfile_filename = os.path.basename(logfile.logfile.path)
        test_logfile_path = os.path.join(
            settings.MEDIA_ROOT,
            crashreport_file_name(logfile, logfile_filename),
        )
        logfile.logfile = test_logfile_path
        logfile.save()

        os.makedirs(os.path.dirname(test_logfile_path))
        shutil.copy(
            os.path.join(Dummy.DEFAULT_LOG_FILE_DIRECTORY, logfile_filename),
            test_logfile_path,
        )
        return logfile, test_logfile_path

    @staticmethod
    def read_logfile_contents(path_to_zipfile, logfile_name):
        """Read bytes of a zipped logfile."""
        archive = zipfile.ZipFile(path_to_zipfile, "r")
        return archive.read(logfile_name)


class HiccupCrashreportsTransactionTestCase(TransactionTestCase):
    """Base class that offers a device registration method."""

    REGISTER_DEVICE_URL = "api_v1_register_device"

    def setUp(self):
        """Create a Fairphone staff user for accessing the API.

        The APIClient that can be used to make authenticated requests to the
        server is stored in self.fp_staff_client.
        """
        fp_staff_group = Group.objects.get(name=FP_STAFF_GROUP_NAME)
        fp_staff_user = User.objects.create_user(
            "fp_staff", "somebody@fairphone.com", "thepassword"
        )
        fp_staff_user.groups.add(fp_staff_group)
        self.fp_staff_client = APIClient()
        self.fp_staff_client.force_login(fp_staff_user)

    def _register_device(self, **kwargs):
        """Register a new device.

        Arguments:
            **kwargs: The data to pass the dummy data creation
                method `Dummy.device_register_data`.
        Returns:
            (UUID, APIClient, str): The uuid of the new device as well as an
            authentication token and the associated user with credentials.

        """
        data = Dummy.device_register_data(**kwargs)
        response = self.client.post(reverse(self.REGISTER_DEVICE_URL), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uuid = response.data["uuid"]
        token = response.data["token"]
        user = APIClient()
        user.credentials(HTTP_AUTHORIZATION="Token " + token)

        return uuid, user, token


class HiccupCrashreportsAPITestCase(
    HiccupCrashreportsTransactionTestCase, APITestCase
):
    """Base class combining device registration methods and API test methods."""

    pass


class RaceConditionsTestCase(HiccupCrashreportsTransactionTestCase):
    """Test cases for race conditions."""

    # Make data from migrations available in the test cases
    serialized_rollback = True

    def _test_create_multiple(
        self, report_type, create_function, argslist, local_id_name
    ):
        """Test that no race condition occurs when creating instances."""
        # Create multiple threads which send reports simultaneously
        threads = []
        for args in argslist:
            thread = threading.Thread(target=create_function, args=args)
            threads.append(thread)
            thread.start()

        # Wait until the threads have finished
        for thread in threads:
            thread.join()

        # Assert that no duplicate local IDs have been assigned
        reports = report_type.objects.all()
        self.assertEqual(
            reports.count(), reports.distinct(local_id_name).count()
        )
        self.assertEqual(reports.count(), len(argslist))
