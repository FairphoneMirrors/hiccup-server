"""REST API for accessing the crashreports statistics."""
import zipfile

from rest_framework import generics
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models.expressions import F

from django_filters.rest_framework import (
    DjangoFilterBackend, DateFilter,
    FilterSet, CharFilter, BooleanFilter
)

from crashreport_stats.models import (
    Version, VersionDaily, RadioVersion, RadioVersionDaily
)
from crashreports.models import (
    Device, Crashreport, HeartBeat, LogFile
)
from crashreports.permissions import (
    HasRightsOrIsDeviceOwnerDeviceCreation, HasStatsAccess
)
from . import raw_querys


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict."""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class DeviceUpdateHistory(APIView):
    """View the update history of a specific device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )

    def get(self, request, uuid, format=None):
        """Get the update history of a device.

        Args:
            request: Http request
            uuid: The UUID of the device
            format: Optional response format parameter

        Returns: The update history of the requested device.

        """
        cursor = connection.cursor()
        raw_querys.execute_device_update_history_query(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)


class DeviceReportHistory(APIView):
    """View the report history of a specific device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )

    def get(self, request, uuid, format=None):
        """Get the report history of a device.

        Args:
            request: Http request
            uuid: The UUID of the device
            format: Optional response format parameter

        Returns: The report history of the requested device.

        """
        cursor = connection.cursor()
        raw_querys.execute_device_report_history(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)


class Status(APIView):
    """View the number of devices, crashreports and heartbeats."""

    permission_classes = (HasStatsAccess,)

    def get(self, request, format=None, ):
        """Get the number of devices, crashreports and heartbeats.

        Args:
            request: Http request
            format: Optional response format parameter

        Returns: The number of devices, crashreports and heartbeats.

        """
        num_devices = Device.objects.count()
        num_crashreports = Crashreport.objects.count()
        num_heartbeats = HeartBeat.objects.count()
        return Response({
            'devices': num_devices,
            'crashreports': num_crashreports,
            'heartbeats': num_heartbeats
        })


class DeviceStat(APIView):
    """View an overview of the statistics of a device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )

    def get(self, request, uuid, format=None, ):
        """Get some general statistics for a device.

        Args:
            request: Http request
            uuid:  The UUID of the device
            format: Optional response format parameter

        Returns: Some general information of the device in a dictionary.

        """
        device = Device.objects.filter(uuid=uuid)
        last_active = HeartBeat.objects.filter(device=device).order_by(
            '-date')[0].date
        heartbeats = HeartBeat.objects.filter(device=device).count()
        crashreports = Crashreport.objects.filter(device=device).filter(
            boot_reason__in=Crashreport.CRASH_BOOT_REASONS).count()
        crashes_per_day = crashreports*1.0/heartbeats if heartbeats > 0 else 0
        smpls = Crashreport.objects.filter(device=device).filter(
            boot_reason__in=Crashreport.SMPL_BOOT_REASONS).count()
        smpl_per_day = smpls*1.0/heartbeats if heartbeats > 0 else 0
        return Response(
            {
                'uuid': uuid,
                'last_active': last_active,
                'heartbeats': heartbeats,
                'crashreports': crashreports,
                'crashes_per_day': crashes_per_day,
                'smpls': smpls,
                'smpl_per_day': smpl_per_day,
                'board_date': device[0].board_date,
            })


class LogFileDownload(APIView):
    """View for downloading log files."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )

    def get(self, request, id_logfile, format=None):
        """Get a logfile.

        Args:
            request: Http request
            id_logfile: The id of the log file
            format: Optional response format parameter

        Returns: The log file with the corresponding id.

        """
        try:
            logfile = LogFile.objects.get(id=id_logfile)
        except ObjectDoesNotExist:
            raise NotFound(detail="Logfile does not exist.")
        zip_file = zipfile.ZipFile(logfile.logfile.path)
        ret = {}
        for file in zip_file.filelist:
            file_open = zip_file.open(file)
            ret[file.filename] = file_open.read()
        return Response(ret)


class _VersionStatsFilter(FilterSet):
    first_seen_before = DateFilter(field_name="first_seen_on",
                                   lookup_expr='lte')
    first_seen_after = DateFilter(field_name="first_seen_on",
                                  lookup_expr='gte')
    released_before = DateFilter(field_name="released_on", lookup_expr='lte')
    released_after = DateFilter(field_name="released_on", lookup_expr='gte')


class _VersionStatsSerializer(serializers.ModelSerializer):
    permission_classes = (HasStatsAccess,)


class _VersionStatsListView(generics.ListAPIView):
    permission_classes = (HasStatsAccess,)
    filter_backends = (DjangoFilterBackend,)


class _DailyVersionStatsFilter(FilterSet):
    date_start = DateFilter(field_name="date", lookup_expr='gte')
    date_end = DateFilter(field_name="date", lookup_expr='lte')


class _DailyVersionStatsSerializer(serializers.ModelSerializer):
    permission_classes = (HasStatsAccess,)


class _DailyVersionStatsListView(generics.ListAPIView):
    permission_classes = (HasStatsAccess,)
    filter_backends = (DjangoFilterBackend,)


class VersionSerializer(_VersionStatsSerializer):
    """Serializer for the Version class."""

    class Meta:  # noqa: D106
        model = Version
        fields = '__all__'


class VersionFilter(_VersionStatsFilter):
    """Filter for Version instances."""

    class Meta:  # noqa: D106
        model = Version
        fields = '__all__'


class VersionListView(_VersionStatsListView):
    """View for listing versions."""

    queryset = Version.objects.all().order_by('-heartbeats')
    filter_class = VersionFilter
    serializer_class = VersionSerializer


class VersionDailyFilter(_DailyVersionStatsFilter):
    """Filter for VersionDaily instances."""

    version__build_fingerprint = CharFilter()
    version__is_official_release = BooleanFilter()
    version__is_beta_release = BooleanFilter()

    class Meta:  # noqa: D106
        model = VersionDaily
        fields = '__all__'


class VersionDailySerializer(_DailyVersionStatsSerializer):
    """Serializer for VersionDaily instances."""

    build_fingerprint = serializers.CharField()

    class Meta:  # noqa: D106
        model = VersionDaily
        fields = '__all__'


class VersionDailyListView(_DailyVersionStatsListView):
    """View for listing VersionDaily instances."""

    queryset = (
        VersionDaily
        .objects
        .annotate(build_fingerprint=F('version__build_fingerprint'))
        .all()
        .order_by('date')
    )
    filter_class = VersionDailyFilter
    filter_fields = (
        'version__build_fingerprint',
        'version__is_official_release',
        'version__is_beta_release',
    )
    serializer_class = VersionDailySerializer


class RadioVersionSerializer(_VersionStatsSerializer):
    """Serializer for RadioVersion instances."""

    class Meta:  # noqa: D106
        model = RadioVersion
        fields = '__all__'


class RadioVersionFilter(_VersionStatsFilter):
    """Filter for RadioVersion instances."""

    class Meta:  # noqa: D106
        model = RadioVersion
        fields = '__all__'


class RadioVersionListView(_VersionStatsListView):
    """View for listing RadioVersion instances."""

    queryset = RadioVersion.objects.all().order_by('-heartbeats')
    serializer_class = RadioVersionSerializer
    filter_class = RadioVersionFilter


class RadioVersionDailyFilter(_DailyVersionStatsFilter):
    """Filter for RadioVersionDaily instances."""

    version__radio_version = CharFilter()
    version__is_official_release = BooleanFilter()
    version__is_beta_release = BooleanFilter()

    class Meta:  # noqa: D106
        model = RadioVersionDaily
        fields = '__all__'


class RadioVersionDailySerializer(_DailyVersionStatsSerializer):
    """Serializer for RadioVersionDaily instances."""

    radio_version = serializers.CharField()

    class Meta:  # noqa: D106
        model = RadioVersionDaily
        fields = '__all__'


class RadioVersionDailyListView(_DailyVersionStatsListView):
    """View for listing RadioVersionDaily instances."""

    queryset = (
        RadioVersionDaily.objects.annotate(
            radio_version=F('version__radio_version'))
        .all()
        .order_by('date')
    )
    filter_class = RadioVersionDailyFilter
    filter_fields = (
        'version__radio_version',
        'version__is_official_release',
        'version__is_beta_release',
    )
    serializer_class = RadioVersionDailySerializer
