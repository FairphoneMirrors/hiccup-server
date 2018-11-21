"""Permissions for accessing the stats API."""
from django.core.exceptions import PermissionDenied

from crashreports.permissions import user_is_hiccup_staff
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


def check_user_is_hiccup_staff(user):
    """Check if the user is part of the Hiccup staff.

    Returns: True if the user is part of the Hiccup staff group.

    Raises:
        PermissionDenied: If the user is not part of the Hiccup staff group.

    """
    if not user_is_hiccup_staff(user):
        raise PermissionDenied(
            "User %s not part of the %s group" % (user, FP_STAFF_GROUP_NAME)
        )
    return True
