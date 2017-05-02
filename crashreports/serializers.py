from rest_framework import serializers
from rest_framework.exceptions import NotFound
from crashreports.models import Crashreport
from crashreports.models import Device
from crashreports.models import HeartBeat
from crashreports.models import LogFile

from rest_framework import permissions
from crashreports.permissions import user_is_hiccup_staff


class PrivateField(serializers.ReadOnlyField):

    def get_attribute(self, instance):
        """
        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        if user_is_hiccup_staff(self.context['request'].user):
            return super(PrivateField, self).get_attribute(instance)
        return -1


class CrashReportSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.AllowAny,)
    logfiles = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='api_v1_logfiles_by_id',
        )
    uuid = serializers.CharField(max_length=64)
    id = PrivateField()
    device_local_id = serializers.IntegerField(required=False)

    class Meta:
        model = Crashreport
        exclude = ('device',)

    def create(self, validated_data):
        try:
            device = Device.objects.get(uuid=validated_data['uuid'])
        except:
            raise NotFound(detail="uuid does not exist")
        validated_data.pop('uuid', None)
        report = Crashreport(**validated_data)
        report.device = device
        report.save()
        return report


class HeartBeatSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAuthenticated,)
    uuid = serializers.CharField(max_length=64)
    id = PrivateField()
    device_local_id = serializers.IntegerField(required=False)

    class Meta:
        model = HeartBeat
        exclude = ('device',)

    def create(self, validated_data):
        try:
            device = Device.objects.get(uuid=validated_data['uuid'])
        except:
            raise NotFound(detail="uuid does not exist")
        validated_data.pop('uuid', None)
        heartbeat = HeartBeat(**validated_data)
        heartbeat.device = device
        heartbeat.save()
        return heartbeat


class LogFileSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAdminUser,)

    class Meta:
        model = LogFile


class DeviceSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAdminUser,)

    class Meta:
        model = Device
