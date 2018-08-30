"""Authorization permission classes for accessing the API."""
import logging

from rest_framework.permissions import BasePermission
from crashreports.models import Device


def user_owns_uuid(user, uuid):
    """Determine whether a user is owning the device with the given UUID.

    Args:
        user: The user making the request.
        uuid: The UUID of the device to be manipulated.

    Returns: True if the user owns the device.

    """
    try:
        device = Device.objects.get(user=user)
    except Exception as exception:  # pylint: disable=broad-except
        logging.exception(exception)
        return False
    if uuid == device.uuid:
        return True
    return False


def user_is_hiccup_staff(user):
    """Determine whether a user is part of the Hiccup staff.

    Returns true if either the user is part of the group
    "FairphoneSoftwareTeam", or he/she has all permissions for manipulating
    crashreports, heartbeats and logfiles.

    Args:
        user: The user making the request.

    Returns: True if user is part of the Hiccup staff.

    """
    if user.groups.filter(name="FairphoneSoftwareTeam").exists():
        return True
    else:
        return user.has_perms(
            [
                # Crashreports
                "crashreports.add_crashreport",
                "crashreports.change_crashreport",
                "crashreports.del_crashreport",
                # Heartbeats
                "heartbeat.add_crashreport",
                "heartbeat.change_crashreport",
                "heartbeat.del_crashreport",
                # Logfiles
                "heartbeat.add_logfile",
                "heartbeat.change_logfile",
                "heartbeat.del_logfile",
            ]
        )


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
