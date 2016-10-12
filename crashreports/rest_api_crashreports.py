from rest_framework import generics
from crashreports.models import Crashreport
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import CrashReportSerializer


class ListCreateCrashReport(generics.ListCreateAPIView):
    queryset = Crashreport.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = CrashReportSerializer
    pass
