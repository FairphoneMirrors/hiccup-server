from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission

from crashreports.models import Device
from crashreports.models import User

from crashreports.serializers import DeviceSerializer


class ListCreateDevices(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    paginate_by = 20
    permission_classes = (IsAuthenticated, )
    serializer_class = DeviceSerializer
    pass


class RetrieveUpdateDestroyDevice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    permission_classes = (IsAuthenticated, )
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
    device.user = user
    device.token = Token.objects.create(user=user).key
    device.save()
    return Response({'uuid': device.uuid, 'token': device.token})
