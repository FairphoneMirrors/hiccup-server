from rest_framework import serializers

from rest_framework.exceptions import NotFound
from crashreports.models import Crashreport
from crashreports.models import Device
from crashreports.models import HeartBeat
from rest_framework import permissions


class CrashReportSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.AllowAny,)
    uuid = serializers.CharField(max_length=64)

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
    permission_classes = (permissions.AllowAny,)
    uuid = serializers.CharField(max_length=64)

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


class DeviceSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAdminUser,)

    class Meta:
        model = Device
