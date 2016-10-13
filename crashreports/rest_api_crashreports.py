from rest_framework import generics
from crashreports.models import Crashreport
from django.shortcuts import get_object_or_404
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from crashreports.serializers import CrashReportSerializer
from rest_framework import exceptions
import traceback 


class ListCreateView(generics.ListCreateAPIView):
    queryset = Crashreport.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = CrashReportSerializer
    pass

    def dispatch(self, *args, **kwargs):
        if 'uuid' in kwargs:
            self.queryset = Crashreport.objects.filter(
                device__uuid=kwargs['uuid'])
        return generics.ListCreateAPIView.dispatch(self, *args, **kwargs)


class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crashreport.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = CrashReportSerializer
    multiple_lookup_fields = {'id', 'device__uuid', 'device_local_id'}

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
