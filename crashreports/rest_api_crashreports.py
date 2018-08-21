"""REST API for accessing crash reports."""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import CrashReportSerializer
from crashreports.models import Crashreport
from crashreports.response_descriptions import default_desc


class CreateCrashreportResponseSchema(CrashReportSerializer):
    """Response schema for successful crash report creation."""

    class Meta:  # noqa: D106
        model = Crashreport
        fields = ["device_local_id"]


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(operation_description="List crash reports"),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Create a crash report",
        request_body=CrashReportSerializer,
        responses=dict(
            [
                default_desc(ValidationError),
                (
                    status.HTTP_404_NOT_FOUND,
                    openapi.Response(
                        "No device with the given uuid could be found."
                    ),
                ),
                (
                    status.HTTP_201_CREATED,
                    openapi.Response(
                        "The crash report has been successfully created.",
                        CreateCrashreportResponseSchema,
                    ),
                ),
            ]
        ),
    ),
)
class ListCreateView(generics.ListCreateAPIView):
    """Endpoint for listing crash reports and creating new crash reports."""

    queryset = Crashreport.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = CrashReportSerializer
    filter_fields = ("device", "build_fingerprint", "radio_version")

    def dispatch(self, *args, **kwargs):
        """Dispatch an incoming HTTP request to the right method.

        The method is overridden in order to replace the 'device__uuid'
        parameter value with the 'uuid' value from the parameters.
        """
        if "uuid" in kwargs:
            self.queryset = Crashreport.objects.filter(
                device__uuid=kwargs["uuid"]
            )
        return generics.ListCreateAPIView.dispatch(self, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a crash report instance in the database.

        The method is overridden in order to create a response containing only
        the device_local_id.
        """
        serializer.save()
        return Response(
            {"device_local_id": serializer.data["device_local_id"]},
            status.HTTP_200_OK,
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Get a crash report",
        responses=dict([default_desc(NotFound)]),
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update a crash report",
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Partially update a crash report",
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete a crash report",
        responses=dict([default_desc(NotFound)]),
    ),
)
class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint for retrieving, updating and deleting crash reports."""

    # pylint: disable=too-many-ancestors

    queryset = Crashreport.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = CrashReportSerializer
    multiple_lookup_fields = {"id", "device__uuid", "device_local_id"}

    def get_object(self):
        """Retrieve a crash report."""
        queryset = self.get_queryset()
        query_filter = {}
        for field in self.multiple_lookup_fields:
            if field in self.kwargs:
                query_filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **query_filter)
        self.check_object_permissions(self.request, obj)
        return obj
