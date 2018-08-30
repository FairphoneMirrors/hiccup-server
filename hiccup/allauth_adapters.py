"""Allauth adapter for authenticating requests using Google OAuth."""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.forms import SignupForm
from allauth.socialaccount.models import SocialLogin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.http import HttpRequest


class FairphoneAccountAdapter(DefaultSocialAccountAdapter):
    """Account adapter for existing Google accounts."""

    def is_open_for_signup(self, request, sociallogin):
        """Allow signup."""
        return True

    def save_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        form: SignupForm = None,
    ):
        """Save a user to the database.

        Additionally add the user to the FairphoneSoftwareTeam group if his
        or her account was issued by Fairphone, i.e. ends with "@fairphone.com".

        Args:
            request: The HTTP request.
            sociallogin:
                SocialLogin instance representing a Google user that is in
                the process of being logged in.
            form: Request form (not used).

        Returns: The newly created user from the local database.

        """
        user = DefaultSocialAccountAdapter.save_user(
            self, request, sociallogin, form=None
        )
        if user.email.split("@")[1] == "fairphone.com":
            group = Group.objects.get(name="FairphoneSoftwareTeam")
            group.user_set.add(user)
        return user

    def populate_user(
        self, request: HttpRequest, sociallogin: SocialLogin, data: dict
    ):
        """Populate an already existing user instance.

        The permission is denied if the Google account was not issued by
        Fairphone, i.e. does not end with "@fairphone.com".

        Args:
            request: The HTTP request.
            sociallogin:
                SocialLogin instance representing a Google user that is in
                the process of being logged in.
            data: Common user data fields.

        Returns: The user from the database.

        """
        user = DefaultSocialAccountAdapter.populate_user(
            self, request, sociallogin, data
        )
        if not user.email.split("@")[1] == "fairphone.com":
            raise PermissionDenied()
        return user


class FormAccountAdapter(DefaultAccountAdapter):
    """Account adapter for signing up using a form.

    Signup is not allowed using Hiccup, only existing Fairphone Google accounts
    can be used.
    """

    def is_open_for_signup(self, request):
        """Do not allow signup."""
        return False
