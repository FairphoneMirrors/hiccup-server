"""Tests for the allauth adapters module."""

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialLogin, SocialAccount
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.test import TestCase

from hiccup.allauth_adapters import (
    FairphoneAccountAdapter,
    FormAccountAdapter,
    FP_STAFF_GROUP_NAME,
)
from hiccup import settings


class Dummy:
    """Create dummies class instances for testing."""

    # pylint: disable=too-few-public-methods

    EMAIL_FAIRPHONE = "test@fairphone.com"
    EMAIL_OTHER = "test@test.com"

    @staticmethod
    def create_sociallogin(user_email):
        """Create a dummy sociallogin instance.

        Args:
            user_email: The email used to login.

        Returns: The sociallogin instance.

        """
        sociallogin = SocialLogin(
            user=User(email=user_email),
            account=SocialAccount(
                provider=next(iter(settings.SOCIALACCOUNT_PROVIDERS))
            ),
            email_addresses=[EmailAddress(email=user_email, verified=True)],
        )
        return sociallogin


class FairphoneAccountAdapterTests(TestCase):
    """Tests for the Fairphone account adapter."""

    def setUp(self):
        """Create a Fairphone account adapter instance."""
        self.fp_account_adapter = FairphoneAccountAdapter()

    def test_is_open_for_signup(self):
        """Validate that the adapter is open for signup."""
        request = HttpRequest()
        sociallogin = Dummy.create_sociallogin(Dummy.EMAIL_FAIRPHONE)

        self.assertTrue(
            self.fp_account_adapter.is_open_for_signup(request, sociallogin)
        )

    def _save_user(self, user_email):
        request = HttpRequest()
        request.session = self.client.session

        sociallogin = Dummy.create_sociallogin(user_email)

        return self.fp_account_adapter.save_user(request, sociallogin)

    def test_save_user_with_fp_email(self):
        """Test saving a user with a Fairphone E-Mail address."""
        # Get the Fairphone staff group
        fp_staff_group = Group.objects.get(name=FP_STAFF_GROUP_NAME)

        # Save a user with a Fairphone E-Mail address
        user = self._save_user(Dummy.EMAIL_FAIRPHONE)

        # Assert that the user has been added to the Fairphone staff group
        self.assertIn(fp_staff_group, user.groups.all())

    def test_save_user_without_fp_email(self):
        """Test saving a user without a Fairphone E-Mail address."""
        # Get the Fairphone staff group
        fp_staff_group = Group.objects.get(name=FP_STAFF_GROUP_NAME)

        # Save a user without a Fairphone E-Mail address
        user = self._save_user(Dummy.EMAIL_OTHER)

        # Assert that the user has not been added to the Fairphone staff group
        self.assertNotIn(fp_staff_group, user.groups.all())

    def _populate_user(self, user_email):
        request = HttpRequest()
        sociallogin = Dummy.create_sociallogin(user_email)
        data = {"email": user_email}

        return self.fp_account_adapter.populate_user(request, sociallogin, data)

    def test_populate_user_with_fp_email(self):
        """Test populating a user with a Fairphone E-Mail address."""
        user = self._populate_user(Dummy.EMAIL_FAIRPHONE)

        # Assert that the user has been populated successfully and its email
        # address is correct
        self.assertEqual(user.email, Dummy.EMAIL_FAIRPHONE)

    def test_populate_user_without_fp_email(self):
        """Test populating a user without a Fairphone E-Mail address."""
        user_email = Dummy.EMAIL_OTHER

        # Assert that a permission denied error is raised when attempting to
        # populate the user
        with self.assertRaises(PermissionDenied):
            self._populate_user(user_email)


class FormAccountAdapterTests(TestCase):
    """Tests for the form account adapter."""

    def setUp(self):
        """Create a form account adapter instance."""
        self.form_account_adapter = FormAccountAdapter()

    def test_is_not_open_for_signup(self):
        """Validate that the adapter is not open for signup."""
        request = HttpRequest()
        self.assertFalse(self.form_account_adapter.is_open_for_signup(request))
