"""Utility functions shared by all crashreports tests."""

import os
from typing import Optional

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from crashreports.models import Crashreport

DEFAULT_DUMMY_LOG_FILE_DIRECTORY = os.path.join("resources", "test")


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

    DEFAULT_DUMMY_DEVICE_REGISTER_VALUES = {
        "board_date": "2015-12-15T01:23:45Z",
        "chipset": "Qualcomm MSM8974PRO-AA",
    }

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        "uuid": None,
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": (
            "Fairphone/FP2/FP2:6.0.1/FP2-gms-18.03.1/FP2-gms-18.03.1:user/"
            "release-keys"
        ),
        "radio_version": "4437.1-FP2-0-08",
        "date": "2018-03-19T09:58:30.386Z",
    }

    DEFAULT_DUMMY_CRASHREPORTS_VALUES = DEFAULT_DUMMY_HEARTBEAT_VALUES.copy()
    DEFAULT_DUMMY_CRASHREPORTS_VALUES.update(
        {
            "is_fake_report": 0,
            "boot_reason": "why?",
            "power_on_reason": "it was powered on",
            "power_off_reason": "something happened and it went off",
        }
    )

    CRASH_TYPE_TO_BOOT_REASON_MAP = {
        "crash": Crashreport.BOOT_REASON_KEYBOARD_POWER_ON,
        "smpl": Crashreport.BOOT_REASON_RTC_ALARM,
        "other": "whatever",
    }

    DEFAULT_DUMMY_LOG_FILE_PATH = os.path.join(
        DEFAULT_DUMMY_LOG_FILE_DIRECTORY, "test_logfile.zip"
    )

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
        from `Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES`.
        """
        return Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_DEVICE_REGISTER_VALUES, kwargs
        )

    @staticmethod
    def heartbeat_data(**kwargs):
        """Return the data required to create a heartbeat.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES`.
        """
        return Dummy._update_copy(Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES, kwargs)

    @staticmethod
    def crashreport_data(report_type: Optional[str] = None, **kwargs):
        """Return the data required to create a crashreport.

        Use the values passed as keyword arguments or default to the ones
        from `Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES`.

        Args:
            report_type: A valid value from
                `Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.keys()` that will
                define the boot reason if not explicitly defined in the
                keyword arguments already.
        """
        data = Dummy._update_copy(
            Dummy.DEFAULT_DUMMY_CRASHREPORTS_VALUES, kwargs
        )
        if report_type and "boot_reason" not in kwargs:
            if report_type not in Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP:
                raise InvalidCrashTypeError(report_type)
            data["boot_reason"] = Dummy.CRASH_TYPE_TO_BOOT_REASON_MAP.get(
                report_type
            )
        return data


class HiccupCrashreportsAPITestCase(APITestCase):
    """Base class that offers a device registration method."""

    REGISTER_DEVICE_URL = "api_v1_register_device"

    def setUp(self):
        """Create an admin user for accessing the API.

        The APIClient that can be used to make authenticated requests to the
        server is stored in self.admin.
        """
        admin_user = User.objects.create_superuser(
            "somebody", "somebody@example.com", "thepassword"
        )
        self.admin = APIClient()
        self.admin.force_authenticate(admin_user)

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
