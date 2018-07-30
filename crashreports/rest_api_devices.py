"""REST API for accessing devices."""

from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from crashreports.models import Device, User
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import DeviceSerializer, DeviceCreateSerializer
from crashreports.response_descriptions import default_desc


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description='List devices'))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description='Create a device',
    responses=dict([default_desc(ValidationError)])))
class ListCreateDevices(generics.ListCreateAPIView):
    """Endpoint for listing devices and creating new devices."""

    queryset = Device.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = DeviceSerializer
    filter_fields = ('uuid', 'board_date', 'chipset')


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description='Get a device',
    responses=dict([default_desc(NotFound)])))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description='Update a device',
    responses=dict([default_desc(NotFound), default_desc(ValidationError)])))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description='Make a partial update for a device',
    responses=dict([default_desc(NotFound), default_desc(ValidationError)])))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description='Delete a device',
    responses=dict([default_desc(NotFound)])))
class RetrieveUpdateDestroyDevice(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint for retrieving, updating, patching and deleting devices."""

    # pylint: disable=too-many-ancestors

    queryset = Device.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = DeviceSerializer
    lookup_field = 'uuid'


class DeviceRegisterResponseSchema(DeviceSerializer):
    """Response schema for successful device registration."""

    class Meta:  # noqa: D106
        model = Device
        fields = ['uuid', 'token']


@swagger_auto_schema(
    method='post',
    request_body=DeviceCreateSerializer,
    responses=dict([
        default_desc(ValidationError),
        (status.HTTP_200_OK,
         openapi.Response('The device has been successfully registered.',
                          DeviceRegisterResponseSchema))
    ]))
@api_view(http_method_names=['POST'], )
@permission_classes((AllowAny,))
def register_device(request):
    """Register a new device.

    This endpoint will generate a django user for the new device. The device is
    identified by a uuid, and authenticated with a token.
    We generate the uuid here as this makes it easier to deal with collisions.
    """
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
