from rest_framework import generics
from django.shortcuts import get_object_or_404
from crashreports.models import HeartBeat
from crashreports.serializers import HeartBeatSerializer
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation

# TODO: There is quite some code duplciation between here and the corresponding
#       crashreport code. We should revisit this later.


class ListCreateView(generics.ListCreateAPIView):
    queryset = HeartBeat.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = HeartBeatSerializer
    filter_fields = ("device", "build_fingerprint", "radio_version")

    def get(self, *args, **kwargs):
        if "uuid" in kwargs:
            self.queryset = HeartBeat.objects.filter(
                device__uuid=kwargs["uuid"]
            )
        return generics.ListCreateAPIView.get(self, *args, **kwargs)


class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeartBeat.objects.all()
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)
    serializer_class = HeartBeatSerializer
    multiple_lookup_fields = {"id", "device__uuid", "device_local_id"}

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
