from crashreports.models import *
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import DeviceSerializer
from django.contrib.auth.models import Permission
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ListCreateDevices(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = DeviceSerializer
    filter_fields = ('uuid', 'board_date', 'chipset')
    pass


class RetrieveUpdateDestroyDevice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = DeviceSerializer
    lookup_field = 'uuid'
    pass


@api_view(http_method_names=['POST'], )
@permission_classes((AllowAny,))
def register_device(request):
    """ Register a new device. This endpoint will generate a django user for
    the new device. The device is identified by a uuid, and authenticated with
    a token.
    We generate the uuid here as this makes it easier to deal with collisions.
    """
    device = Device()
    user = User.objects.create_user("device_" + str(device.uuid), '', None)
    permission = Permission.objects.get(name='Can add crashreport')
    user.user_permissions.add(permission)
    user.save()
    device.board_date = request.data['board_date']
    device.chipset = request.data['chipset']
    device.user = user
    device.token = Token.objects.create(user=user).key
    device.save()
    return Response({'uuid': device.uuid, 'token': device.token})


class DeviceStat(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None, ):
        device          = Device.objects.filter(uuid=uuid)
        last_active     = HeartBeat.objects.filter(device=device).order_by('-date')[0].date
        heartbeats      = HeartBeat.objects.filter(device=device).count()
        crashreports    = Crashreport.objects.filter(device=device).filter(boot_reason__in=["UNKNOWN", "keyboard power on"]).count()
        crashes_per_day = crashreports*1.0/heartbeats if heartbeats > 0 else 0
        smpls           = Crashreport.objects.filter(device=device).filter(boot_reason__in=["RTC alarm"]).count()
        smpl_per_day    = smpls*1.0/heartbeats if heartbeats > 0 else 0
        return Response(
            {
                'uuid'            : uuid,
                'last_active'     : last_active,
                'heartbeats'      : heartbeats,
                'crashreports'    : crashreports,
                'crashes_per_day' : crashes_per_day,
                'smpls'           : smpls,
                'smpl_per_day'    : smpl_per_day
            })
