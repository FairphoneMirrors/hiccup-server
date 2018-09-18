"""Tests for the views module."""

import unittest
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse

from rest_framework import status

from crashreport_stats.tests.utils import Dummy, HiccupStatsAPITestCase

# pylint: disable=too-many-public-methods


class ViewsTestCase(HiccupStatsAPITestCase):
    """Test cases for the statistics views."""

    home_url = reverse("device")
    device_url = reverse("hiccup_stats_device")
    versions_url = reverse("hiccup_stats_versions")
    versions_all_url = reverse("hiccup_stats_versions_all")

    @staticmethod
    def _url_with_params(url, params):
        # Encode params, but keep slashes because we want to accept URLs as
        # parameter values.
        encoded_params = urlencode(params, safe="/")
        return "{}?{}".format(url, encoded_params)

    def _get_with_params(self, url, params):
        return self.fp_staff_client.get(self._url_with_params(url, params))

    @unittest.skip(
        "Fails because the view is currently not accessible for admin users."
    )
    def test_home_view_as_admin(self):
        """Test that admin users can access the home view."""
        self._assert_get_as_admin_user_succeeds(self.home_url)

    def test_home_view_as_fp_staff(self):
        """Test that Fairphone staff users can access the home view."""
        self._assert_get_as_fp_staff_succeeds(self.home_url)

    def test_home_view_as_device_owner(self):
        """Test that device owner users can not access the home view."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_as_device_owner_fails(
            self.home_url, expected_status=status.HTTP_302_FOUND
        )

    def test_home_view_no_auth(self):
        """Test that one can not access the home view without auth."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_without_authentication_fails(
            self.home_url, expected_status=status.HTTP_302_FOUND
        )

    @unittest.skip(
        "Fails because the view is currently not accessible for admin users."
    )
    def test_device_view_as_admin(self):
        """Test that admin users can access the device view."""
        self._assert_get_as_admin_user_succeeds(
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            )
        )

    def test_device_view_as_fp_staff(self):
        """Test that Fairphone staff users can access the device view."""
        self._assert_get_as_fp_staff_succeeds(
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            )
        )

    def test_device_view_as_device_owner(self):
        """Test that device owner users can not access the device view."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_as_device_owner_fails(
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            ),
            expected_status=status.HTTP_302_FOUND,
        )

    def test_device_view_no_auth(self):
        """Test that non-authenticated users can not access the device view."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_without_authentication_fails(
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            ),
            expected_status=status.HTTP_302_FOUND,
        )

    @unittest.skip(
        "Fails because the view is currently not accessible for admin users."
    )
    def test_versions_view_as_admin(self):
        """Test that admin users can access the versions view."""
        self._assert_get_as_admin_user_succeeds(self.versions_url)

    def test_versions_view_as_fp_staff(self):
        """Test that Fairphone staff users can access the versions view."""
        self._assert_get_as_fp_staff_succeeds(self.versions_url)

    def test_versions_view_as_device_owner(self):
        """Test that device owner users can not access the versions view."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_as_device_owner_fails(
            self.versions_url, expected_status=status.HTTP_302_FOUND
        )

    def test_versions_view_no_auth(self):
        """Test one can not access the versions view without auth."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_without_authentication_fails(
            self.versions_url, expected_status=status.HTTP_302_FOUND
        )

    @unittest.skip(
        "Fails because the view is currently not accessible for admin users."
    )
    def test_versions_all_view_as_admin(self):
        """Test that admin users can access the versions all view."""
        self._assert_get_as_admin_user_succeeds(self.versions_all_url)

    def test_versions_all_view_as_fp_staff(self):
        """Test that Fairphone staff users can access the versions all view."""
        self._assert_get_as_fp_staff_succeeds(self.versions_all_url)

    def test_versions_all_view_as_device_owner(self):
        """Test that device owner users can not access the versions all view."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_as_device_owner_fails(
            self.versions_all_url, expected_status=status.HTTP_302_FOUND
        )

    def test_versions_all_view_no_auth(self):
        """Test that one can not access the versions all view without auth."""
        # Assert that the response is a redirect (to the login page)
        self._assert_get_without_authentication_fails(
            self.versions_all_url, expected_status=status.HTTP_302_FOUND
        )

    @unittest.skip(
        "Fails because the view is currently not accessible for admin users."
    )
    def test_home_view_post_as_admin_user(self):
        """Test HTTP POST method to home view as admin user."""
        response = self.admin.post(
            self.home_url, data={"uuid": str(self.device_owner_device.uuid)}
        )

        # Assert that the response is a redirect to the device page
        self.assertRedirects(
            response,
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            ),
        )

    def test_home_view_post_as_fp_staff(self):
        """Test HTTP POST method to home view as Fairphone staff user."""
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(self.device_owner_device.uuid)}
        )

        # Assert that the response is a redirect to the device page
        self.assertRedirects(
            response,
            self._url_with_params(
                self.device_url, {"uuid": self.device_owner_device.uuid}
            ),
        )

    def test_home_view_post_no_auth(self):
        """Test HTTP POST method to home view without authentication."""
        response = self.client.post(
            self.home_url, data={"uuid": str(self.device_owner_device.uuid)}
        )

        # Assert that the response is a redirect to the login page
        self.assertRedirects(
            response,
            self._url_with_params(
                settings.ACCOUNT_LOGOUT_REDIRECT_URL,
                {"next": settings.LOGIN_REDIRECT_URL},
            ),
        )

    def test_home_view_post_as_device_owner(self):
        """Test HTTP POST method to home view as device owner."""
        response = self.device_owner_client.post(
            self.home_url, data={"uuid": str(self.device_owner_device.uuid)}
        )

        # Assert that the response is a redirect to the login page

        self.assertRedirects(
            response,
            self._url_with_params(
                settings.ACCOUNT_LOGOUT_REDIRECT_URL,
                {"next": settings.LOGIN_REDIRECT_URL},
            ),
        )

    def test_get_home_view(self):
        """Test getting the home view with device search form."""
        response = self.fp_staff_client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(response.context["devices"], None)

    def test_home_view_filter_devices_by_uuid(self):
        """Test filtering devices by UUID."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Filter devices by UUID of the created device
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device.uuid)}
        )

        # Assert that the the client is redirected to the device page
        self.assertRedirects(
            response,
            self._url_with_params(self.device_url, {"uuid": device.uuid}),
        )

    def test_home_view_filter_devices_by_uuid_part(self):
        """Test filtering devices by start of UUID."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Filter devices with start of the created device's UUID
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device.uuid)[:4]}
        )

        # Assert that the the client is redirected to the device page
        self.assertRedirects(
            response,
            self._url_with_params(self.device_url, {"uuid": device.uuid}),
        )

    def test_home_view_filter_devices_by_uuid_part_ambiguous_result(self):
        """Test filtering devices with common start of UUIDs."""
        # Create two devices
        device1 = Dummy.create_dummy_device(Dummy.create_dummy_user())
        device2 = Dummy.create_dummy_device(
            Dummy.create_dummy_user(username=Dummy.USERNAMES[1])
        )

        # Adapt the devices' UUID so that they start with the same characters
        device1.uuid = "4060fd90-6de1-4b03-a380-4277c703e913"
        device1.save()
        device2.uuid = "4061c59b-823d-4ec6-a463-8ac0c1cea67d"
        device2.save()

        # Filter devices with first three (common) characters of the UUID
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": str(device1.uuid)[:3]}
        )

        # Assert that both devices are part of the result
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(set(response.context["devices"]), {device1, device2})

    def test_home_view_filter_devices_empty_database(self):
        """Test filtering devices on an empty database."""
        response = self.fp_staff_client.post(
            self.home_url, data={"uuid": "TestUUID"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

    def test_home_view_filter_devices_no_uuid(self):
        """Test filtering devices without specifying UUID."""
        response = self.fp_staff_client.post(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/home.html", count=1
        )
        self.assertEqual(response.context["devices"], None)

    def test_get_device_view_empty_database(self):
        """Test getting device view on an empty database."""
        response = self.fp_staff_client.get(self.device_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_device_view(self):
        """Test getting device view."""
        # Create a device
        device = Dummy.create_dummy_device(Dummy.create_dummy_user())

        # Get the corresponding device view
        response = self._get_with_params(self.device_url, {"uuid": device.uuid})

        # Assert that the view is constructed from the correct templates and
        # the response context contains the device UUID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(
            response, "crashreport_stats/device.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/device_overview.html", count=1
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_update_history.html",
            count=1,
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_report_history.html",
            count=1,
        )
        self.assertTemplateUsed(
            response,
            "crashreport_stats/tags/device_crashreport_table.html",
            count=1,
        )
        self.assertEqual(response.context["uuid"], str(device.uuid))

    def _assert_versions_view_templates_are_used(self, response):
        self.assertTemplateUsed(
            response, "crashreport_stats/versions.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_table.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_pie_chart.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_bar_chart.html", count=1
        )
        self.assertTemplateUsed(
            response, "crashreport_stats/tags/versions_area_chart.html", count=1
        )

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_view_empty_database(self):
        """Test getting versions view on an empty database."""
        response = self.fp_staff_client.get(self.versions_url)

        # Assert that the correct templates are used and the response context
        # contains the correct value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context["is_official_release"], True)

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_view(self):
        """Test getting versions view."""
        # Create a version
        Dummy.create_dummy_version()

        # Get the versions view
        response = self.fp_staff_client.get(self.versions_url)

        # Assert that the correct templates are used and the response context
        # contains the correct value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context["is_official_release"], True)

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_all_view_no_versions(self):
        """Test getting versions all view on an empty database."""
        response = self.fp_staff_client.get(self.versions_all_url)

        # Assert that the correct templates are used and the response context
        # contains an empty value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context.get("is_official_release", ""), "")

    @unittest.skip("Fails because of wrong boolean usage in views.py")
    def test_get_versions_all_view(self):
        """Test getting versions view."""
        # Create a version
        Dummy.create_dummy_version()

        # Get the versions view
        response = self.fp_staff_client.get(self.versions_all_url)

        # Assert that the correct templates are used and the response context
        # contains the an empty value for is_official_release
        self._assert_versions_view_templates_are_used(response)
        self.assertEqual(response.context.get("is_official_release", ""), "")
