from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from django.db import connection
from . import raw_querys
from crashreport_stats.models import *
import zipfile
from crashreports.models import *
from django.db.models.expressions import F
import django_filters
from rest_framework import filters

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class DeviceUpdateHistory(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None):
        cursor = connection.cursor()
        raw_querys.execute_device_update_history_query(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)

class DeviceReportHistory(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None):
        cursor = connection.cursor()
        raw_querys.execute_device_report_history(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)

class DeviceStat(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None, ):
        device          = Device.objects.filter(uuid=uuid)
        last_active     = HeartBeat.objects.filter(device=device).order_by('-date')[0].date
        heartbeats      = HeartBeat.objects.filter(device=device).count()
        crashreports    = Crashreport.objects.filter(device=device).filter(boot_reason__in=["UNKNOWN", "keyboard power on"]).count()
        crashes_per_day = crashreports*1.0/heartbeats if heartbeats > 0 else 0
        smpls           = Crashreport.objects.filter(device=device).filter(boot_reason__in=["RTC alarm"]).count()
        smpl_per_day    = smpls*1.0/heartbeats if heartbeats > 0 else 0
        return Response(
            {
                'uuid'            : uuid,
                'last_active'     : last_active,
                'heartbeats'      : heartbeats,
                'crashreports'    : crashreports,
                'crashes_per_day' : crashes_per_day,
                'smpls'           : smpls,
                'smpl_per_day'    : smpl_per_day
            })

class LogFileDownload(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, id, format=None):
        try:
            logfile = LogFile.objects.get(id=id)
        except:
            raise NotFound(detail="Logfile does not exist.")
        zf = zipfile.ZipFile(logfile.logfile.path)
        ret = {}
        for f in zf.filelist:
            fo = zf.open(f)
            ret[f.filename] = fo.read()
        return Response(ret)
        

class VersionFilter(filters.FilterSet):
    first_seen_before = django_filters.DateFilter(name="first_seen_on", lookup_expr='lte')
    first_seen_after   = django_filters.DateFilter(name="first_seen_on", lookup_expr='gte')
    released_before = django_filters.DateFilter(name="released_on", lookup_expr='lte')
    released_after   = django_filters.DateFilter(name="released_on", lookup_expr='gte')
    class Meta:
        model = Version

class VersionSerializer(serializers.ModelSerializer):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    class Meta:
        model = Version

class VersionListView(generics.ListAPIView):
    queryset = Version.objects.all().order_by('-heartbeats')
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    serializer_class = VersionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = (VersionFilter)

class VersionDailyFilter(filters.FilterSet):
    date_start = django_filters.DateFilter(name="date", lookup_expr='gte')
    date_end   = django_filters.DateFilter(name="date", lookup_expr='lte')
    version__build_fingerprint = django_filters.CharFilter()
    version__is_official_release = django_filters.BooleanFilter()
    version__is_beta_release = django_filters.BooleanFilter()
    class Meta:
        model = VersionDaily

class VersionDailySerializer(serializers.ModelSerializer):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    build_fingerprint  = serializers.CharField()
    class Meta:
        model = VersionDaily

class VersionDailyListView(generics.ListAPIView):
    queryset = VersionDaily.objects.annotate(build_fingerprint=F('version__build_fingerprint')).all().order_by('date')
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = VersionDailySerializer
    filter_class = (VersionDailyFilter)
    filter_fields = ('version__build_fingerprint','version__is_official_release','version__is_beta_release',)
