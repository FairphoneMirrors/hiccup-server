from rest_framework import serializers
from models import Crashreport
from rest_framework import permissions

class CrashReportSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAuthenticated)
    class Meta:
        model = Crashreport
        fields = ('pk','uuid', 'uptime', 'build_fingerprint', 'boot_reason',
        'power_on_reason', 'power_off_reason', 'aux_data', 'date','app_version', 'report_type')
