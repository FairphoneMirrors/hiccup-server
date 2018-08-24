"""Serializers for Crashreport-related models."""
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework import permissions

from crashreports.models import Crashreport, Device, HeartBeat, LogFile
from crashreports.permissions import user_is_hiccup_staff


class PrivateField(serializers.ReadOnlyField):
    """Class for making a field private.

    The private attribute can then only be read by Hiccup staff members
    """

    def get_attribute(self, instance):
        """Get the private attribute.

        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        if user_is_hiccup_staff(self.context["request"].user):
            return super(PrivateField, self).get_attribute(instance)
        return -1


class CrashReportSerializer(serializers.ModelSerializer):
    """Serializer for CrashReport instances."""

    permission_classes = (permissions.AllowAny,)
    logfiles = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="api_v1_logfiles_by_id"
    )
    uuid = serializers.CharField(max_length=64)
    id = PrivateField()
    device_local_id = serializers.IntegerField(required=False)
    date = serializers.DateTimeField(default_timezone=timezone.utc)

    class Meta:  # noqa: D106
        model = Crashreport
        exclude = ("device",)

    def create(self, validated_data):
        """Create a crashreport.

        Args:
            validated_data: Data of the crashreport, excluding the device

        Returns: The created report

        """
        try:
            device = Device.objects.get(uuid=validated_data["uuid"])
        except ObjectDoesNotExist:
            raise NotFound(detail="uuid does not exist")
        validated_data.pop("uuid", None)
        report = Crashreport(**validated_data)
        report.device = device
        report.save()
        return report


class HeartBeatSerializer(serializers.ModelSerializer):
    """Serializer for HeartBeat instances."""

    permission_classes = (permissions.IsAuthenticated,)
    uuid = serializers.CharField(max_length=64)
    id = PrivateField()
    device_local_id = serializers.IntegerField(required=False)
    date = serializers.DateTimeField(default_timezone=timezone.utc)

    class Meta:  # noqa: D106
        model = HeartBeat
        exclude = ("device",)

    def create(self, validated_data):
        """Create a heartbeat report.

        Args:
            validated_data: Data of the heartbeat, excluding the device

        Returns: The created heartbeat

        """
        try:
            device = Device.objects.get(uuid=validated_data["uuid"])
        except ObjectDoesNotExist:
            raise NotFound(detail="uuid does not exist")
        validated_data.pop("uuid", None)
        heartbeat = HeartBeat(**validated_data)
        heartbeat.device = device
        heartbeat.save()
        return heartbeat


class LogFileSerializer(serializers.ModelSerializer):
    """Serializer for LogFile instances."""

    permission_classes = (permissions.IsAdminUser,)

    class Meta:  # noqa: D106
        model = LogFile
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for Device instances."""

    permission_classes = (permissions.IsAdminUser,)
    board_date = serializers.DateTimeField(default_timezone=timezone.utc)
    last_heartbeat = serializers.DateTimeField(default_timezone=timezone.utc)

    class Meta:  # noqa: D106
        model = Device
        fields = "__all__"


class DeviceCreateSerializer(DeviceSerializer):
    """Serializer for creating Device instances."""

    class Meta:  # noqa: D106
        model = Device
        fields = ("board_date", "chipset")
        extra_kwargs = {
            "board_date": {"required": True},
            "chipset": {"required": True},
        }
