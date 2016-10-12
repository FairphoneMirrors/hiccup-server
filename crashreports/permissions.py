from crashreports.models import Device
from rest_framework.permissions import BasePermission


def user_owns_uuid(user, uuid):
    try:
        device = Device.objects.get(user=user)
    except:
        return False
    if (uuid == device.uuid):
        return True
    return False


def user_is_hiccup_staff(user):
    return (user.has_perm('crashreports.add_crashreport')
            and user.has_perm('crashreports.change_crashreport')
            and user.has_perm('crashreports.del_crashreport')
            and user.has_perm('heartbeat.add_crashreport')
            and user.has_perm('heartbeat.change_crashreport')
            and user.has_perm('heartbeat.del_crashreport')
            and user.has_perm('heartbeat.add_logfile')
            and user.has_perm('heartbeat.change_logfile')
            and user.has_perm('heartbeat.del_logfile'))


class HasRightsOrIsDeviceOwnerDeviceCreation(BasePermission):

    def has_permission(self, request, view):
        # if user has all permissions for crashreport return true
        if (user_is_hiccup_staff(request.user)):
            return True
        # special case:
        # user is the owner of a device. in this case creations are allowed.
        # we have to check if the device with the supplied uuid indeed
        # belongs to the user
        if request.method == 'POST':
            if ('uuid' not in request.data):
                return False
            return user_owns_uuid(request.user, request.data["uuid"])
        return False
