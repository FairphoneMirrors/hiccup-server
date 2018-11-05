"""Authorization permission classes for accessing the API."""
import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from crashreports.models import Device
from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


def user_owns_uuid(user, uuid):
    """Determine whether a user is owning the device with the given UUID.

    Args:
        user: The user making the request.
        uuid: The UUID of the device to be manipulated.

    Returns: True if the user owns the device.

    """
    try:
        device = Device.objects.get(user=user)
    except (ObjectDoesNotExist, TypeError):
        # If the device does not exist or type of the given user is not
        # correct, False is returned.
        return False
    except Exception as exception:  # pylint: disable=broad-except
        # All other exceptions are logged and False is returned.
        logging.exception(exception)
        return False
    if uuid == device.uuid:
        return True
    return False


def user_is_hiccup_staff(user):
    """Determine whether a user is part of the Hiccup staff.

    Returns true if either the user is part of the group
    "FairphoneSoftwareTeam".

    Args:
        user: The user making the request.

    Returns: True if user is part of the Hiccup staff.

    """
    return user.groups.filter(name=FP_STAFF_GROUP_NAME).exists()


class HasStatsAccess(BasePermission):
    """Authorization requires to be part of the Hiccup staff."""

    def has_permission(self, request, view):
        """Check if user is part of the Hiccup staff."""
        return user_is_hiccup_staff(request.user)


class HasRightsOrIsDeviceOwnerDeviceCreation(BasePermission):
    """Authorization requires to be part of Hiccup staff or device owner."""

    def has_permission(self, request, view):
        """Return true if user is part of Hiccp staff or device owner."""
        if user_is_hiccup_staff(request.user):
            return True

        # special case:
        # user is the owner of a device. in this case creations are allowed.
        # we have to check if the device with the supplied uuid indeed
        # belongs to the user
        if request.method == "POST":
            if "uuid" not in request.data:
                return False
            return user_owns_uuid(request.user, request.data["uuid"])
        return False


# Security requirements for swagger documentation
SWAGGER_SECURITY_REQUIREMENTS_OAUTH = [{"Google OAuth": []}]
SWAGGER_SECURITY_REQUIREMENTS_DEVICE_TOKEN = [
    {"Device token authentication": []}
]
SWAGGER_SECURITY_REQUIREMENTS_ALL = (
    SWAGGER_SECURITY_REQUIREMENTS_OAUTH
    + SWAGGER_SECURITY_REQUIREMENTS_DEVICE_TOKEN
)
