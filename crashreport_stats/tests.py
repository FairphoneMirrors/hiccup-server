"""Test crashreport_stats models and the 'stats' command."""
from datetime import datetime, date
import pytz

from django.urls import reverse
from django.utils.http import urlencode

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from crashreport_stats.models import (
    Version, VersionDaily, RadioVersion, RadioVersionDaily
)

from crashreports.models import User, Device


class Dummy():
    """Class for creating dummy instances for testing."""

    # Valid unique entries
    BUILD_FINGERPRINTS = [(
        'Fairphone/FP2/FP2:5.1/FP2/r4275.1_FP2_gms76_1.13.0:user/release-keys'
    ), (
        'Fairphone/FP2/FP2:5.1.1/FP2-gms75.1.13.0/FP2-gms75.1.13.0'
        ':user/release-keys'
    ), (
        'Fairphone/FP2/FP2:6.0.1/FP2-gms-18.04.1/FP2-gms-18.04.1'
        ':user/release-keys'
    ), (
        'Fairphone/FP2/FP2:7.1.2/18.07.2/gms-7480c31d'
        ':user/release-keys'
    )]
    RADIO_VERSIONS = ['4437.1-FP2-0-07', '4437.1-FP2-0-08',
                      '4437.1-FP2-0-09', '4437.1-FP2-0-10']

    DATES = [date(2018, 3, 19), date(2018, 3, 26), date(2018, 5, 1)]

    DEFAULT_DUMMY_VERSION_VALUES = {
        'build_fingerprint': BUILD_FINGERPRINTS[0],
        'first_seen_on': DATES[1],
        'released_on': DATES[0]
    }

    DEFAULT_DUMMY_VERSION_DAILY_VALUES = {
        'date': DATES[1]
    }

    DEFAULT_DUMMY_RADIO_VERSION_VALUES = {
        'radio_version': RADIO_VERSIONS[0],
        'first_seen_on': DATES[1],
        'released_on': DATES[0]
    }

    DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES = {
        'date': DATES[1]
    }

    DEFAULT_DUMMY_DEVICE_VALUES = {
        'board_date': datetime(2015, 12, 15, 1, 23, 45, tzinfo=pytz.utc),
        'chipset': 'Qualcomm MSM8974PRO-AA',
        'token': '64111c62d521fb4724454ca6dea27e18f93ef56e'
    }

    DEFAULT_DUMMY_USER_VALUES = {
        'username': 'testuser'
    }

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
        entity = User(**Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_USER_VALUES, kwargs))
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
        entity = Device(user=user, **Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_DEVICE_VALUES, kwargs))
        entity.save()
        return entity

    @staticmethod
    def create_dummy_version(**kwargs):
        """Create a dummy version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created version instance.

        """
        entity = Version(**Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_VERSION_VALUES, kwargs))
        entity.save()
        return entity

    @staticmethod
    def create_dummy_radio_version(**kwargs):
        """Create a dummy radio version instance.

        The dummy instance is created and saved to the database.
        Args:
            **kwargs:
                Optional arguments to extend/overwrite the default values.

        Returns: The created radio version instance.

        """
        entity = RadioVersion(**Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_RADIO_VERSION_VALUES, kwargs))
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
        entity = VersionDaily(version=version, **Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_VERSION_DAILY_VALUES, kwargs))
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
        entity = RadioVersionDaily(version=version, **Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_RADIO_VERSION_DAILY_VALUES, kwargs))
        entity.save()
        return entity


class _VersionTestCase(APITestCase):
    """Abstract class for version-related test cases to inherit from."""

    # The attribute name characterising the unicity of a stats entry (the
    # named identifier)
    unique_entry_name = 'build_fingerprint'
    # The collection of unique entries to post
    unique_entries = Dummy.BUILD_FINGERPRINTS
    # The URL to retrieve the stats entries from
    endpoint_url = reverse('hiccup_stats_api_v1_versions')

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Create an admin user for accessing the API.

        The APIClient that can be used to make authenticated requests to the
        server is stored in self.admin.
        """
        admin_user = User.objects.create_superuser(
            'somebody', 'somebody@example.com', 'thepassword')
        cls.admin = APIClient()
        cls.admin.force_authenticate(admin_user)

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_version(**kwargs)

    def _get_with_params(self, url, params):
        return self.admin.get('{}?{}'.format(url, urlencode(params)))

    def _assert_result_length_is(self, response, count):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], count)
        self.assertEqual(len(response.data['results']), count)

    def _assert_device_owner_has_no_get_access(self, entries_url):
        # Create a user and device
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user=user)

        # Create authenticated client
        user = APIClient()
        user.credentials(HTTP_AUTHORIZATION='Token ' + device.token)

        # Try getting entries using the client
        response = user.get(entries_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _assert_filter_result_matches(self, filter_params, expected_result):
        # List entities with filter
        response = self._get_with_params(self.endpoint_url, filter_params)

        # Expect only the single matching result to be returned
        self._assert_result_length_is(response, 1)
        self.assertEqual(response.data['results'][0][self.unique_entry_name],
                         getattr(expected_result, self.unique_entry_name))


class VersionTestCase(_VersionTestCase):
    """Test the Version and REST endpoint."""

    def _create_version_entities(self):
        versions = [
            self._create_dummy_version(
                **{self.unique_entry_name: unique_entry}
            )
            for unique_entry in self.unique_entries
        ]
        return versions

    def test_list_versions_without_authentication(self):
        """Test listing of versions without authentication."""
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_versions_as_device_owner(self):
        """Test listing of versions as device owner."""
        self._assert_device_owner_has_no_get_access(self.endpoint_url)

    def test_list_versions_empty_database(self):
        """Test listing of versions on an empty database."""
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, 0)

    def test_list_versions(self):
        """Test listing versions."""
        versions = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

    def test_filter_versions_by_unique_entry_name(self):
        """Test filtering versions by their unique entry name."""
        versions = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)

        # Listing all entities should return the correct result length
        self._assert_result_length_is(response, len(versions))

        # List entities with filter
        filter_params = {
            self.unique_entry_name: getattr(versions[0],
                                            self.unique_entry_name)
        }
        self._assert_filter_result_matches(filter_params,
                                           expected_result=versions[0])

    def test_filter_versions_by_release_type(self):
        """Test filtering versions by release type."""
        # Create versions for all combinations of release types
        versions = []
        i = 0
        for is_official_release in True, False:
            for is_beta_release in True, False:
                versions.append(self._create_dummy_version(**{
                    'is_official_release': is_official_release,
                    'is_beta_release': is_beta_release,
                    self.unique_entry_name: self.unique_entries[i]
                }))
                i += 1

        # # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # List each of the entities with the matching filter params
        for version in versions:
            filter_params = {
                'is_official_release': version.is_official_release,
                'is_beta_release': version.is_beta_release
            }
            self._assert_filter_result_matches(filter_params,
                                               expected_result=version)

    def test_filter_versions_by_first_seen_date(self):
        """Test filtering versions by first seen date."""
        versions = self._create_version_entities()

        # Set the first seen date of an entity
        versions[0].first_seen_on = Dummy.DATES[2]
        versions[0].save()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # Expect the single matching result to be returned
        filter_params = {'first_seen_after': Dummy.DATES[2]}
        self._assert_filter_result_matches(filter_params,
                                           expected_result=versions[0])


# pylint: disable=too-many-ancestors
class RadioVersionTestCase(VersionTestCase):
    """Test the RadioVersion REST endpoint."""

    unique_entry_name = 'radio_version'
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse('hiccup_stats_api_v1_radio_versions')

    @staticmethod
    def _create_dummy_version(**kwargs):
        return Dummy.create_dummy_radio_version(**kwargs)


class VersionDailyTestCase(_VersionTestCase):
    """Test the VersionDaily REST endpoint."""

    endpoint_url = reverse('hiccup_stats_api_v1_version_daily')

    @staticmethod
    def _create_dummy_daily_version(version, **kwargs):
        return Dummy.create_dummy_daily_version(version, **kwargs)

    def _create_version_entities(self):
        versions = [
            self._create_dummy_version(
                **{self.unique_entry_name: unique_entry}
            )
            for unique_entry in self.unique_entries
        ]
        versions_daily = [
            self._create_dummy_daily_version(version=version)
            for version in versions
        ]
        return versions_daily

    def test_list_daily_versions_without_authentication(self):
        """Test listing of daily versions without authentication."""
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_daily_versions_as_device_owner(self):
        """Test listing of daily versions as device owner."""
        self._assert_device_owner_has_no_get_access(self.endpoint_url)

    def test_list_daily_versions_empty_database(self):
        """Test listing of daily versions on an empty database."""
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, 0)

    def test_list_daily_versions(self):
        """Test listing daily versions."""
        versions_daily = self._create_version_entities()
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions_daily))

    def test_filter_daily_versions_by_version(self):
        """Test filtering versions by the version they relate to."""
        # Create VersionDaily entities
        versions = self._create_version_entities()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # List entities with filter
        param_name = 'version__' + self.unique_entry_name
        filter_params = {
            param_name: getattr(versions[0].version, self.unique_entry_name)
        }
        self._assert_filter_result_matches(filter_params,
                                           expected_result=versions[0].version)

    def test_filter_daily_versions_by_date(self):
        """Test filtering daily versions by date."""
        # Create Version and VersionDaily entities
        versions = self._create_version_entities()

        # Update the date
        versions[0].date = Dummy.DATES[2]
        versions[0].save()

        # Listing all entities should return the correct result length
        response = self.admin.get(self.endpoint_url)
        self._assert_result_length_is(response, len(versions))

        # Expect the single matching result to be returned
        filter_params = {'date': versions[0].date}
        self._assert_filter_result_matches(filter_params,
                                           expected_result=versions[0].version)


class RadioVersionDailyTestCase(VersionDailyTestCase):
    """Test the RadioVersionDaily REST endpoint."""

    unique_entry_name = 'radio_version'
    unique_entries = Dummy.RADIO_VERSIONS
    endpoint_url = reverse('hiccup_stats_api_v1_radio_version_daily')

    @staticmethod
    def _create_dummy_version(**kwargs):
        entity = RadioVersion(**Dummy.update_copy(
            Dummy.DEFAULT_DUMMY_RADIO_VERSION_VALUES, kwargs))
        entity.save()
        return entity

    @staticmethod
    def _create_dummy_daily_version(version, **kwargs):
        return Dummy.create_dummy_daily_radio_version(version, **kwargs)
