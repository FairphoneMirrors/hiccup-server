"""REST API for accessing the crashreports statistics."""
import operator
import zipfile
from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import F
from django.utils.decorators import method_decorator

from django_filters.rest_framework import (
    DjangoFilterBackend,
    DateFilter,
    FilterSet,
    CharFilter,
    BooleanFilter,
)

from crashreport_stats.models import (
    Version,
    VersionDaily,
    RadioVersion,
    RadioVersionDaily,
)
from crashreports.models import Device, Crashreport, HeartBeat, LogFile
from crashreports.permissions import (
    HasRightsOrIsDeviceOwnerDeviceCreation,
    HasStatsAccess,
    SWAGGER_SECURITY_REQUIREMENTS_ALL,
    SWAGGER_SECURITY_REQUIREMENTS_OAUTH,
)
from crashreports.response_descriptions import default_desc

_RESPONSE_STATUS_200_DESCRIPTION = "OK"


_DEVICE_UPDATE_HISTORY_SCHEMA = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="DeviceUpdateHistoryEntry",
        properties=OrderedDict(
            [
                ("build_fingerprint", openapi.Schema(type=openapi.TYPE_STRING)),
                ("heartbeats", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("max", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("other", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("prob_crashes", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("smpl", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("update_date", openapi.Schema(type=openapi.TYPE_STRING)),
            ]
        ),
    ),
)


class DeviceUpdateHistory(APIView):
    """View the update history of a specific device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)

    @swagger_auto_schema(
        operation_description="Get the update history of a device",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict(
            [
                default_desc(NotFound),
                (
                    status.HTTP_200_OK,
                    openapi.Response(
                        _RESPONSE_STATUS_200_DESCRIPTION,
                        _DEVICE_UPDATE_HISTORY_SCHEMA,
                    ),
                ),
            ]
        ),
    )
    def get(self, request, uuid):
        """Get the update history of a device.

        Args:
            request: Http request
            uuid: The UUID of the device

        Returns:
            The update history of the requested device, sorted by the update
            date.

        """
        device = Device.objects.get(uuid=uuid)

        device_heartbeats = list(device.heartbeats.all())
        device_crashreports = list(device.crashreports.all())

        build_fingerprints = {hb.build_fingerprint for hb in device_heartbeats}

        response = [
            get_release_stats(
                build_fingerprint,
                device,
                device_crashreports,
                device_heartbeats,
            )
            for build_fingerprint in build_fingerprints
        ]
        response = sorted(response, key=operator.itemgetter("update_date"))

        return Response(response)


def get_release_stats(build_fingerprint, device, crashreports, heartbeats):
    """Get the stats for a device for a specific release."""
    heartbeats = filter_instances(
        heartbeats, lambda hb: hb.build_fingerprint == build_fingerprint
    )
    crashreports = filter_instances(
        crashreports, lambda c: c.build_fingerprint == build_fingerprint
    )

    stats = get_stats(heartbeats, crashreports)
    stats.update(
        {
            "build_fingerprint": build_fingerprint,
            "update_date": min([heartbeat.date for heartbeat in heartbeats]),
            "max": device.id,
        }
    )

    return stats


_DEVICE_REPORT_HISTORY_SCHEMA = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="DeviceReportHistoryEntry",
        properties=OrderedDict(
            [
                ("date", openapi.Schema(type=openapi.TYPE_STRING)),
                ("heartbeats", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("other", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("prob_crashes", openapi.Schema(type=openapi.TYPE_INTEGER)),
                ("smpl", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ]
        ),
    ),
)


class DeviceReportHistory(APIView):
    """View the report history of a specific device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)

    @swagger_auto_schema(
        operation_description="Get the report history of a device",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict(
            [
                default_desc(NotFound),
                (
                    status.HTTP_200_OK,
                    openapi.Response(
                        _RESPONSE_STATUS_200_DESCRIPTION,
                        _DEVICE_REPORT_HISTORY_SCHEMA,
                    ),
                ),
            ]
        ),
    )
    def get(self, request, uuid):
        """Get the report history of a device.

        Args:
            request: Http request
            uuid: The UUID of the device

        Returns: The report history of the requested device, sorted by date.

        """
        device = Device.objects.get(uuid=uuid)

        device_heartbeats = list(device.heartbeats.all())
        device_crashreports = list(device.crashreports.all())

        dates = {heartbeat.date.date() for heartbeat in device_heartbeats}

        response = [
            get_stats_for_date(date, device_crashreports, device_heartbeats)
            for date in sorted(dates)
        ]

        return Response(response)


def get_stats_for_date(date, crashreports, heartbeats):
    """Get the stats for a device for a specific date."""
    heartbeats = filter_instances(heartbeats, lambda hb: hb.date.date() == date)
    crashreports = filter_instances(
        crashreports, lambda c: c.date.date() == date
    )

    stats = get_stats(heartbeats, crashreports)
    stats.update(date=date)
    return stats


def filter_instances(instances, filter_expr):
    """Filter instances using a lambda filter function."""
    return list(filter(filter_expr, instances))


def get_stats(heartbeats, crashreports):
    """Get the numbers of heartbeats and crashes per for each type."""
    crashes = [
        crashreport
        for crashreport in crashreports
        if crashreport.boot_reason in Crashreport.CRASH_BOOT_REASONS
    ]
    smpls = [
        crashreport
        for crashreport in crashreports
        if crashreport.boot_reason in Crashreport.SMPL_BOOT_REASONS
    ]
    others = [
        crashreport
        for crashreport in crashreports
        if crashreport not in crashes + smpls
    ]
    return {
        "heartbeats": len(heartbeats),
        "smpl": len(smpls),
        "prob_crashes": len(crashes),
        "other": len(others),
    }


_STATUS_RESPONSE_SCHEMA = openapi.Schema(
    title="Status",
    type=openapi.TYPE_OBJECT,
    properties=OrderedDict(
        [
            ("devices", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ("crashreports", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ("heartbeats", openapi.Schema(type=openapi.TYPE_INTEGER)),
        ]
    ),
)


class Status(APIView):
    """View the number of devices, crashreports and heartbeats."""

    permission_classes = (HasStatsAccess,)

    @swagger_auto_schema(
        operation_description="Get the number of devices, crashreports and "
        "heartbeats",
        security=SWAGGER_SECURITY_REQUIREMENTS_OAUTH,
        responses=dict(
            [
                (
                    status.HTTP_200_OK,
                    openapi.Response(
                        _RESPONSE_STATUS_200_DESCRIPTION,
                        _STATUS_RESPONSE_SCHEMA,
                    ),
                )
            ]
        ),
    )
    def get(self, request):
        """Get the number of devices, crashreports and heartbeats.

        Args:
            request: Http request

        Returns: The number of devices, crashreports and heartbeats.

        """
        num_devices = Device.objects.count()
        num_crashreports = Crashreport.objects.count()
        num_heartbeats = HeartBeat.objects.count()
        return Response(
            {
                "devices": num_devices,
                "crashreports": num_crashreports,
                "heartbeats": num_heartbeats,
            }
        )


_DEVICE_STAT_OVERVIEW_SCHEMA = openapi.Schema(
    title="DeviceStatOverview",
    type=openapi.TYPE_OBJECT,
    properties=OrderedDict(
        [
            ("board_date", openapi.Schema(type=openapi.TYPE_STRING)),
            ("crashes_per_day", openapi.Schema(type=openapi.TYPE_NUMBER)),
            ("crashreports", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ("heartbeats", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ("last_active", openapi.Schema(type=openapi.TYPE_STRING)),
            ("smpl_per_day", openapi.Schema(type=openapi.TYPE_NUMBER)),
            ("smpls", openapi.Schema(type=openapi.TYPE_INTEGER)),
            ("uuid", openapi.Schema(type=openapi.TYPE_STRING)),
        ]
    ),
)


class DeviceStat(APIView):
    """View an overview of the statistics of a device."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)

    @swagger_auto_schema(
        operation_description="Get some general statistics for a device.",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict(
            [
                default_desc(NotFound),
                (
                    status.HTTP_200_OK,
                    openapi.Response(
                        _RESPONSE_STATUS_200_DESCRIPTION,
                        _DEVICE_STAT_OVERVIEW_SCHEMA,
                    ),
                ),
            ]
        ),
    )
    def get(self, request, uuid):
        """Get some general statistics for a device.

        Args:
            request: Http request
            uuid:  The UUID of the device

        Returns: Some general information of the device in a dictionary.

        """
        device = Device.objects.filter(uuid=uuid)

        heartbeat_instances = HeartBeat.objects.filter(device=device)
        if heartbeat_instances.exists():
            last_active = heartbeat_instances.order_by("-date")[0].date
        else:
            last_active = device[0].board_date

        heartbeats = heartbeat_instances.count()
        crashreports = (
            Crashreport.objects.filter(device=device)
            .filter(boot_reason__in=Crashreport.CRASH_BOOT_REASONS)
            .count()
        )
        crashes_per_day = (
            crashreports * 1.0 / heartbeats if heartbeats > 0 else 0
        )
        smpls = (
            Crashreport.objects.filter(device=device)
            .filter(boot_reason__in=Crashreport.SMPL_BOOT_REASONS)
            .count()
        )
        smpl_per_day = smpls * 1.0 / heartbeats if heartbeats > 0 else 0
        return Response(
            {
                "uuid": uuid,
                "last_active": last_active,
                "heartbeats": heartbeats,
                "crashreports": crashreports,
                "crashes_per_day": crashes_per_day,
                "smpls": smpls,
                "smpl_per_day": smpl_per_day,
                "board_date": device[0].board_date,
            }
        )


_LOG_FILE_SCHEMA = openapi.Schema(title="LogFile", type=openapi.TYPE_FILE)


class LogFileDownload(APIView):
    """View for downloading log files."""

    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation,)

    @swagger_auto_schema(
        operation_description="Get a log file.",
        security=SWAGGER_SECURITY_REQUIREMENTS_ALL,
        responses=dict(
            [
                default_desc(NotFound),
                (
                    status.HTTP_200_OK,
                    openapi.Response(
                        _RESPONSE_STATUS_200_DESCRIPTION, _LOG_FILE_SCHEMA
                    ),
                ),
            ]
        ),
    )
    def get(self, request, id_logfile):
        """Get a logfile.

        Args:
            request: Http request
            id_logfile: The id of the log file

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
    first_seen_before = DateFilter(
        field_name="first_seen_on", lookup_expr="lte"
    )
    first_seen_after = DateFilter(field_name="first_seen_on", lookup_expr="gte")
    released_before = DateFilter(field_name="released_on", lookup_expr="lte")
    released_after = DateFilter(field_name="released_on", lookup_expr="gte")


class _VersionStatsSerializer(serializers.ModelSerializer):
    permission_classes = (HasStatsAccess,)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(security=SWAGGER_SECURITY_REQUIREMENTS_OAUTH),
)
class _VersionStatsListView(generics.ListAPIView):
    permission_classes = (HasStatsAccess,)
    filter_backends = (DjangoFilterBackend,)


class _DailyVersionStatsFilter(FilterSet):
    date_start = DateFilter(field_name="date", lookup_expr="gte")
    date_end = DateFilter(field_name="date", lookup_expr="lte")


class _DailyVersionStatsSerializer(serializers.ModelSerializer):
    permission_classes = (HasStatsAccess,)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(security=SWAGGER_SECURITY_REQUIREMENTS_OAUTH),
)
class _DailyVersionStatsListView(generics.ListAPIView):
    permission_classes = (HasStatsAccess,)
    filter_backends = (DjangoFilterBackend,)


class VersionSerializer(_VersionStatsSerializer):
    """Serializer for the Version class."""

    class Meta:  # noqa: D106
        model = Version
        fields = "__all__"


class VersionFilter(_VersionStatsFilter):
    """Filter for Version instances."""

    class Meta:  # noqa: D106
        model = Version
        fields = "__all__"


class VersionListView(_VersionStatsListView):
    """View for listing versions."""

    queryset = Version.objects.all().order_by("-heartbeats")
    filter_class = VersionFilter
    serializer_class = VersionSerializer


class VersionDailyFilter(_DailyVersionStatsFilter):
    """Filter for VersionDaily instances."""

    version__build_fingerprint = CharFilter()
    version__is_official_release = BooleanFilter()
    version__is_beta_release = BooleanFilter()

    class Meta:  # noqa: D106
        model = VersionDaily
        fields = "__all__"


class VersionDailySerializer(_DailyVersionStatsSerializer):
    """Serializer for VersionDaily instances."""

    build_fingerprint = serializers.CharField()

    class Meta:  # noqa: D106
        model = VersionDaily
        fields = "__all__"


class VersionDailyListView(_DailyVersionStatsListView):
    """View for listing VersionDaily instances."""

    queryset = (
        VersionDaily.objects.annotate(
            build_fingerprint=F("version__build_fingerprint")
        )
        .all()
        .order_by("date")
    )
    filter_class = VersionDailyFilter
    filter_fields = (
        "version__build_fingerprint",
        "version__is_official_release",
        "version__is_beta_release",
    )
    serializer_class = VersionDailySerializer


class RadioVersionSerializer(_VersionStatsSerializer):
    """Serializer for RadioVersion instances."""

    class Meta:  # noqa: D106
        model = RadioVersion
        fields = "__all__"


class RadioVersionFilter(_VersionStatsFilter):
    """Filter for RadioVersion instances."""

    class Meta:  # noqa: D106
        model = RadioVersion
        fields = "__all__"


class RadioVersionListView(_VersionStatsListView):
    """View for listing RadioVersion instances."""

    queryset = RadioVersion.objects.all().order_by("-heartbeats")
    serializer_class = RadioVersionSerializer
    filter_class = RadioVersionFilter


class RadioVersionDailyFilter(_DailyVersionStatsFilter):
    """Filter for RadioVersionDaily instances."""

    version__radio_version = CharFilter()
    version__is_official_release = BooleanFilter()
    version__is_beta_release = BooleanFilter()

    class Meta:  # noqa: D106
        model = RadioVersionDaily
        fields = "__all__"


class RadioVersionDailySerializer(_DailyVersionStatsSerializer):
    """Serializer for RadioVersionDaily instances."""

    radio_version = serializers.CharField()

    class Meta:  # noqa: D106
        model = RadioVersionDaily
        fields = "__all__"


class RadioVersionDailyListView(_DailyVersionStatsListView):
    """View for listing RadioVersionDaily instances."""

    queryset = (
        RadioVersionDaily.objects.annotate(
            radio_version=F("version__radio_version")
        )
        .all()
        .order_by("date")
    )
    filter_class = RadioVersionDailyFilter
    filter_fields = (
        "version__radio_version",
        "version__is_official_release",
        "version__is_beta_release",
    )
    serializer_class = RadioVersionDailySerializer
