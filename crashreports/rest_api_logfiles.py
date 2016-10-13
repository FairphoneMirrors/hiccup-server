from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import permission_classes

from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound


from rest_framework.response import Response
from crashreports.models import LogFile
from crashreports.models import Crashreport
from crashreports.permissions import user_owns_uuid
from crashreports.permissions import user_is_hiccup_staff


@api_view(http_method_names=['POST'], )
@parser_classes(FileUploadParser)
@permission_classes(IsAuthenticated,)
def logfile_put(request):
    try:
        crashreport = Crashreport.objects.get(crashreport_pk)
    except:
        raise NotFound(detail="crashreport does not exist")
    if (not (user_owns_uuid(request.user, crashreport.device.uuid)
             or user_is_hiccup_staff(request.user))):
        raise PermissionDenied(detail="Not allowed.")
    logfile = LogFile(crashreport=crashreport, logfile=request.data["file"])
    logfile.save()
    return Response(201, data={'result': 'ok'})
