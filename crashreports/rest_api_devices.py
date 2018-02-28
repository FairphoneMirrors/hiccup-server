from crashreports.models import *
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import DeviceSerializer, DeviceCreateSerializer
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
    # Return status '400 Bad Request' if data is not well-formed.
    serializer = DeviceCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    device = Device()
    user = User.objects.create_user("device_" + str(device.uuid), '', None)
    permission = Permission.objects.get(name='Can add crashreport')
    user.user_permissions.add(permission)
    user.save()
    device.board_date = serializer.validated_data['board_date']
    device.chipset = serializer.validated_data['chipset']
    device.user = user
    device.token = Token.objects.create(user=user).key
    device.save()
    return Response({'uuid': device.uuid, 'token': device.token})
