"""Utility functions shared by all crashreport stats tests."""

from datetime import datetime

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

from crashreports.models import User
from crashreports.tests.utils import Dummy as CrashreportsDummy
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


class Dummy(CrashreportsDummy):
    """Class for creating dummy instances for testing."""

    DEFAULT_VERSION_VALUES = {
        "build_fingerprint": CrashreportsDummy.BUILD_FINGERPRINTS[0],
        "first_seen_on": CrashreportsDummy.DATES[1],
        "released_on": CrashreportsDummy.DATES[0],
        "is_beta_release": False,
        "is_official_release": True,
    }

    DEFAULT_VERSION_DAILY_VALUES = {"date": CrashreportsDummy.DATES[1]}

    DEFAULT_RADIO_VERSION_VALUES = {
        "radio_version": CrashreportsDummy.RADIO_VERSIONS[0],
        "first_seen_on": CrashreportsDummy.DATES[1],
        "released_on": CrashreportsDummy.DATES[0],
    }

    DEFAULT_RADIO_VERSION_DAILY_VALUES = {"date": CrashreportsDummy.DATES[1]}

    DEFAULT_STATSMETADATA_VALUES = {
        "updated_at": datetime(2018, 6, 15, 2, 12, 24, tzinfo=pytz.utc)
    }

    @staticmethod
    def create_version(version_type=Version, **kwargs):
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
                **Dummy._update_copy(Dummy.DEFAULT_VERSION_VALUES, kwargs)
            )
        elif version_type == RadioVersion:
            entity = RadioVersion(
                **Dummy._update_copy(Dummy.DEFAULT_RADIO_VERSION_VALUES, kwargs)
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
    def create_daily_version(version, **kwargs):
        """Create a dummy daily version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily version instance.

        """
        entity = VersionDaily(
            version=version,
            **Dummy._update_copy(Dummy.DEFAULT_VERSION_DAILY_VALUES, kwargs)
        )
        entity.save()
        return entity

    @staticmethod
    def create_daily_radio_version(version, **kwargs):
        """Create a dummy daily radio version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created daily radio version instance.

        """
        entity = RadioVersionDaily(
            version=version,
            **Dummy._update_copy(
                Dummy.DEFAULT_RADIO_VERSION_DAILY_VALUES, kwargs
            )
        )
        entity.save()
        return entity

    @staticmethod
    def create_stats_metadata(**kwargs):
        """Create a dummy stats metadata instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created stats metadata instance.

        """
        entity = StatsMetadata(
            **Dummy._update_copy(Dummy.DEFAULT_STATSMETADATA_VALUES, kwargs)
        )
        entity.save()
        return entity


class HiccupStatsAPITestCase(APITestCase):
    """Abstract class for Hiccup stats REST API test cases to inherit from."""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Create client users for accessing the API.

        The APIClient that can be used to make authenticated requests as
        Fairphone staff user is stored in self.fp_staff_client. Additionally, a
        client which is related to a device owner user is stored in
        self.device_owner_client.
        """
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
        cls.device_owner_device = Dummy.create_device(
            user=cls.device_owner_user
        )
        cls.device_owner_client = APIClient()
        cls.device_owner_client.credentials(
            HTTP_AUTHORIZATION="Token " + cls.device_owner_user.auth_token.key
        )

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
