from crashreports.models import Device
from rest_framework.permissions import BasePermission


class HasRightsOrIsDeviceOwnerDeviceCreation(BasePermission):

    def has_permission(self, request, view):
        # if user has all permissions for crashreport return true
        if (request.user.has_perm('crashreports.add_crashreport')
                and request.user.has_perm('crashreports.change_crashreport')
                and request.user.has_perm('crashreports.del_crashreport')
                and request.user.has_perm('heartbeat.add_crashreport')
                and request.user.has_perm('heartbeat.change_crashreport')
                and request.user.has_perm('heartbeat.del_crashreport')):
            return True
        # special case:
        # user is the owner of a device. in this case creations are allowed.
        # we have to check if the device with the supplied uuid indeed
        # belongs to the user
        if request.method == 'POST':
            try:
                device = Device.objects.get(user=request.user)
            except:
                return False
            if ('uuid' not in request.data):
                return False
            if (request.data['uuid'] == device.uuid):
                return True
        return False
