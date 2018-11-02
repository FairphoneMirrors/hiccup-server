"""REST API for accessing heartbeats."""

from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError

from crashreports.models import HeartBeat
from crashreports.permissions import (
    HasRightsOrIsDeviceOwnerDeviceCreation,
    SWAGGER_SECURITY_REQUIREMENTS_ALL,
)
from crashreports.response_descriptions import default_desc
from crashreports.serializers import HeartBeatSerializer
from crashreports.utils import get_object_by_lookup_fields


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="List heartbeats",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Create a heartbeat",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        request_body=HeartBeatSerializer,
        responses=dict(
            [
                default_desc(ValidationError),
                (
                    status.HTTP_404_NOT_FOUND,
                    openapi.Response(
                        "No device with the given uuid could be found."
                    ),
                ),
            ]
        ),
    ),
)
class ListCreateView(generics.ListCreateAPIView):
    """Endpoint for listing heartbeats and creating new heartbeats."""

    queryset = HeartBeat.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = HeartBeatSerializer
    filter_fields = ("device", "build_fingerprint", "radio_version")

    def get(self, request, *args, **kwargs):
        """Override device__uuid parameter with uuid."""
        if "uuid" in kwargs:
            self.queryset = HeartBeat.objects.filter(
                device__uuid=kwargs["uuid"]
            )
        return generics.ListCreateAPIView.get(self, request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Get a heartbeat",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound)]),
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update a heartbeat",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Partially update a heartbeat",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete a heartbeat",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound)]),
    ),
)
class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint for retrieving, updating and deleting heartbeats."""

    # pylint: disable=too-many-ancestors

    queryset = HeartBeat.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = HeartBeatSerializer
    multiple_lookup_fields = {"id", "device__uuid", "device_local_id"}

    def get_object(self):
        """Retrieve a heartbeat."""
        return get_object_by_lookup_fields(self, self.multiple_lookup_fields)
