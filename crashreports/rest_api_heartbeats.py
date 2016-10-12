from rest_framework import generics
from crashreports.models import HeartBeat
from crashreports.serializers import HeartBeatSerializer
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation


class ListCreateHeartBeat(generics.ListCreateAPIView):
    queryset = HeartBeat.objects.all()
    paginate_by = 20
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = HeartBeatSerializer
    pass
