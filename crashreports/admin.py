from django.contrib import admin
from  models import Crashreport
# Register your models here.

@admin.register(Crashreport)
class CrashreportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'build_fingerprint', 'boot_reason', 'power_on_reason', 'power_off_reason', 'aux_data', 'date', 'uuid', 'crashreport_file_link']
    pass
