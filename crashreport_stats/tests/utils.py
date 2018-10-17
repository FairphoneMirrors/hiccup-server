"""Utility functions shared by all crashreport stats tests."""

from datetime import datetime, date
import zipfile

import pytz
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from crashreport_stats.models import (
    Version,
    VersionDaily,
    RadioVersion,
    RadioVersionDaily,
    StatsMetadata,
)

from crashreports.models import Crashreport, Device, HeartBeat, LogFile, User
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


class Dummy:
    """Class for creating dummy instances for testing."""

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

    USERNAMES = ["testuser1", "testuser2", "testuser3"]

    DATES = [date(2018, 3, 19), date(2018, 3, 26), date(2018, 5, 1)]

    DEFAULT_DUMMY_VERSION_VALUES = {
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "first_seen_on": DATES[1],
        "released_on": DATES[0],
        "is_beta_release": False,
        "is_official_release": True,
    }

    DEFAULT_DUMMY_VERSION_DAILY_VALUES = {"date": DATES[1]}

    DEFAULT_DUMMY_RADIO_VERSION_VALUES = {
        "radio_version": RADIO_VERSIONS[0],
        "first_seen_on": DATES[1],
        "released_on": DATES[0],
    }

    DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES = {"date": DATES[1]}

    DEFAULT_DUMMY_STATSMETADATA_VALUES = {
        "updated_at": datetime(2018, 6, 15, 2, 12, 24, tzinfo=pytz.utc)
    }

    DEFAULT_DUMMY_DEVICE_VALUES = {
        "board_date": datetime(2015, 12, 15, 1, 23, 45, tzinfo=pytz.utc),
        "chipset": "Qualcomm MSM8974PRO-AA",
        "token": "64111c62d521fb4724454ca6dea27e18f93ef56e",
    }

    DEFAULT_DUMMY_USER_VALUES = {"username": USERNAMES[0]}

    DEFAULT_DUMMY_HEARTBEAT_VALUES = {
        "app_version": 10100,
        "uptime": (
            "up time: 16 days, 21:49:56, idle time: 5 days, 20:55:04, "
            "sleep time: 10 days, 20:46:27"
        ),
        "build_fingerprint": BUILD_FINGERPRINTS[0],
        "radio_version": RADIO_VERSIONS[0],
        "date": datetime(2018, 3, 19, 12, 0, 0, tzinfo=pytz.utc),
    }

    DEFAULT_DUMMY_CRASHREPORT_VALUES = DEFAULT_DUMMY_HEARTBEAT_VALUES.copy()
    DEFAULT_DUMMY_CRASHREPORT_VALUES.update(
        {
            "is_fake_report": 0,
            "boot_reason": Crashreport.BOOT_REASON_UNKOWN,
            "power_on_reason": "it was powered on",
            "power_off_reason": "something happened and it went off",
        }
    )

    DEFAULT_DUMMY_LOG_FILE_VALUES = {
        "logfile_type": "last_kmsg",
        "logfile": "test_logfile.zip",
    }

    DEFAULT_DUMMY_LOG_FILE_NAME = "dmesg.log"

    @staticmethod
    def update_copy(original, update):
        """Merge fields of update into a copy of original."""
        data = original.copy()
        data.update(update)
        return data

    @staticmethod
    def create_dummy_user(**kwargs):
        """Create a dummy user instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created user instance.

        """
        entity = User(
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_USER_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_device(user, **kwargs):
        """Create a dummy device instance.

        The dummy instance is created and saved to the database.
        Args:
            user: The user instance that the device should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created device instance.

        """
        entity = Device(
            user=user,
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_DEVICE_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_report(report_type, device, **kwargs):
        """Create a dummy report instance of the given report class type.

        The dummy instance is created and saved to the database.
        Args:
            report_type: The class of the report type to be created.
            user: The device instance that the heartbeat should relate to
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created report instance.

        """
        if report_type == HeartBeat:
            entity = HeartBeat(
                device=device,
                **Dummy.update_copy(
                    Dummy.DEFAULT_DUMMY_HEARTBEAT_VALUES, kwargs
                )
            )
        elif report_type == Crashreport:
            entity = Crashreport(
                device=device,
                **Dummy.update_copy(
                    Dummy.DEFAULT_DUMMY_CRASHREPORT_VALUES, kwargs
                )
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
    def create_dummy_log_file(crashreport, **kwargs):
        """Create a dummy log file instance.

        The dummy instance is created and saved to the database.

        Args:
            crashreport: The crashreport that the log file belongs to.
            **kwargs: Optional arguments to extend/overwrite the default values.

        Returns: The created log file instance.

        """
        entity = LogFile(
            crashreport=crashreport,
            **Dummy.update_copy(Dummy.DEFAULT_DUMMY_LOG_FILE_VALUES, kwargs)
        )

        entity.save()
        return entity

    @staticmethod
    def read_logfile_contents(path_to_zipfile, logfile_name):
        """Read bytes of a zipped logfile."""
        archive = zipfile.ZipFile(path_to_zipfile, "r")
        return archive.read(logfile_name)

    @staticmethod
    def create_dummy_version(version_type=Version, **kwargs):
        """Create a dummy version instance.

        The dummy instance is created and saved to the database.
        Args:
            version_type: The class of the version type to be created.
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created version instance.

        Raises:
            ValueError: If version_type is not a valid version class type.

        """
        if version_type == Version:
            entity = Version(
                **Dummy.update_copy(Dummy.DEFAULT_DUMMY_VERSION_VALUES, kwargs)
            )
        elif version_type == RadioVersion:
            entity = RadioVersion(
                **Dummy.update_copy(
                    Dummy.DEFAULT_DUMMY_RADIO_VERSION_VALUES, kwargs
                )
            )
        else:
            raise ValueError(
                "No dummy version instance can be created for {}".format(
                    version_type.__name__
                )
            )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_daily_version(version, **kwargs):
        """Create a dummy daily version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily version instance.

        """
        entity = VersionDaily(
            version=version,
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_VERSION_DAILY_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_daily_radio_version(version, **kwargs):
        """Create a dummy daily radio version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily radio version instance.

        """
        entity = RadioVersionDaily(
            version=version,
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_dummy_stats_metadata(**kwargs):
        """Create a dummy stats metadata instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created stats metadata instance.

        """
        entity = StatsMetadata(
            **Dummy.update_copy(
                Dummy.DEFAULT_DUMMY_STATSMETADATA_VALUES, kwargs
            )
        )
        entity.save()
        return entity


class HiccupStatsAPITestCase(APITestCase):
    """Abstract class for Hiccup stats REST API test cases to inherit from."""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Create an admin and two client users for accessing the API.

        The APIClient that can be used to make authenticated requests as
        admin user is stored in self.admin. A client which is related to a
        user that is part of the Fairphone staff group is stored in
        self.fp_staff_client. A client which is related to a device owner
        user is stored in self.device_owner_client.
        """
        admin_user = User.objects.create_superuser(
            "somebody", "somebody@example.com", "thepassword"
        )
        cls.admin = APIClient()
        cls.admin.force_login(admin_user)

        fp_staff_group = Group.objects.get(name=FP_STAFF_GROUP_NAME)
        fp_staff_user = User.objects.create_user(
            "fp_staff", "somebody@fairphone.com", "thepassword"
        )
        fp_staff_user.groups.add(fp_staff_group)
        cls.fp_staff_client = APIClient()
        cls.fp_staff_client.force_login(fp_staff_user)

        cls.device_owner_user = User.objects.create_user(
            "device_owner", "somebody@somemail.com", "thepassword"
        )
        Token.objects.create(user=cls.device_owner_user)
        cls.device_owner_device = Dummy.create_dummy_device(
            user=cls.device_owner_user
        )
        cls.device_owner_client = APIClient()
        cls.device_owner_client.credentials(
            HTTP_AUTHORIZATION="Token " + cls.device_owner_user.auth_token.key
        )

    def _assert_get_as_admin_user_succeeds(
        self, url, expected_status=status.HTTP_200_OK
    ):
        response = self.admin.get(url)
        self.assertEqual(response.status_code, expected_status)

    def _assert_get_as_fp_staff_succeeds(
        self, url, expected_status=status.HTTP_200_OK
    ):
        response = self.fp_staff_client.get(url)
        self.assertEqual(response.status_code, expected_status)

    def _assert_get_without_authentication_fails(
        self, url, expected_status=status.HTTP_401_UNAUTHORIZED
    ):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status)

    def _assert_get_as_device_owner_fails(
        self, url, expected_status=status.HTTP_403_FORBIDDEN
    ):
        response = self.device_owner_client.get(url)
        self.assertEqual(response.status_code, expected_status)
