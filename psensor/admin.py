from django.contrib import admin
from  models import PSensorSetting
# Register your models here.

@admin.register(PSensorSetting)
class PSensorSettingAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'old_offset', 'old_near_threshold', 'old_far_threshold', 'new_offset', 'new_near_threshold', 'new_far_threshold',  'timestamp']
    pass
