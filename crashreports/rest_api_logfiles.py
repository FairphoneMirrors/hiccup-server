from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import permission_classes

from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound

from rest_framework.response import Response

from crashreports.serializers import LogFileSerializer

from crashreports.models import LogFile
from crashreports.models import Crashreport
from crashreports.permissions import user_owns_uuid
from crashreports.permissions import user_is_hiccup_staff
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from rest_framework import generics


class ListCreateView(generics.ListAPIView):
    queryset = LogFile.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = LogFileSerializer


class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LogFile.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = LogFileSerializer


@api_view(http_method_names=["POST"])
@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
def logfile_put(request, uuid, device_local_id, filename):
    try:
        crashreport = Crashreport.objects.get(
            device__uuid=uuid, device_local_id=device_local_id
        )
    except:
        raise NotFound(detail="Crashreport does not exist.")

    if not (
        user_owns_uuid(request.user, crashreport.device.uuid)
        or user_is_hiccup_staff(request.user)
    ):
        raise PermissionDenied(detail="Not allowed.")
    f = request.data["file"]
    logfile = LogFile(crashreport=crashreport, logfile=f)
    logfile.save()
    return Response(status=201)
