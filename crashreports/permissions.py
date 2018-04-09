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
    if (user.groups.filter(name='FairphoneSoftwareTeam').exists()):
        return True
    else:
        return user.has_perms([
            # Crashreports
            'crashreports.add_crashreport', 'crashreports.change_crashreport',
            'crashreports.del_crashreport',
            # Heartbeats
            'heartbeat.add_crashreport', 'heartbeat.change_crashreport',
            'heartbeat.del_crashreport',
            # Logfiles
            'heartbeat.add_logfile', 'heartbeat.change_logfile',
            'heartbeat.del_logfile',
            ])

class HasStatsAccess(BasePermission):
    def has_permission(self, request, view):
        return user_is_hiccup_staff(request.user)

class HasRightsOrIsDeviceOwnerDeviceCreation(BasePermission):
    def has_permission(self, request, view):
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
