from rest_framework import serializers
from models import PSensorSetting
from rest_framework import permissions

class PSensorSettingSerializer(serializers.ModelSerializer):
    permission_classes = (permissions.IsAuthenticated)
    class Meta:
        model = PSensorSetting
        fields = ('pk','uuid', 'old_offset', 'old_near_threshold', 'old_far_threshold', 'new_offset', 'new_near_threshold', 'new_far_threshold',  'timestamp')
