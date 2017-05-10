from django.contrib import admin
from crashreport_stats.models import *

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    pass

@admin.register(VersionDaily)
class VersionDailyAdmin(admin.ModelAdmin):
    list_display=('version','date')
    pass
