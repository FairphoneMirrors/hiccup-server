"""REST API for accessing log files."""
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
)
from rest_framework.exceptions import (
    PermissionDenied,
    NotFound,
    ValidationError,
)
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crashreports.response_descriptions import default_desc
from crashreports.serializers import LogFileSerializer
from crashreports.models import Crashreport, LogFile
from crashreports.permissions import (
    HasRightsOrIsDeviceOwnerDeviceCreation,
    user_owns_uuid,
    user_is_hiccup_staff,
    SWAGGER_SECURITY_REQUIREMENTS_ALL,
)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="List log files",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
    ),
)
class ListCreateView(generics.ListAPIView):
    """Endpoint for listing log files."""

    queryset = LogFile.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = LogFileSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Get a log file",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound)]),
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update a log file",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Partially update a log file",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound), default_desc(ValidationError)]),
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete a log file",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict([default_desc(NotFound)]),
    ),
)
class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint for retrieving, updating and deleting log files."""

    # pylint: disable=too-many-ancestors

    queryset = LogFile.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = LogFileSerializer


@swagger_auto_schema(
    method="post",
    security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
    request_body=LogFileSerializer,
    responses=dict(
        [
            default_desc(ValidationError),
            (
                status.HTTP_404_NOT_FOUND,
                openapi.Response("Crashreport does not exist."),
            ),
            (status.HTTP_201_CREATED, openapi.Response("Created")),
        ]
    ),
)
@api_view(http_method_names=["POST"])
@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
def logfile_put(request, uuid, device_local_id, filename):
    """Upload a log file for a crash report."""
    try:
        crashreport = Crashreport.objects.get(
            device__uuid=uuid, device_local_id=device_local_id
        )
    except ObjectDoesNotExist:
        raise NotFound(detail="Crashreport does not exist.")

    if not (
        user_owns_uuid(request.user, crashreport.device.uuid)
        or user_is_hiccup_staff(request.user)
    ):
        raise PermissionDenied(detail="Not allowed.")
    file = request.data["file"]
    logfile = LogFile(crashreport=crashreport, logfile=file)
    logfile.save()
    return Response(status=201)
