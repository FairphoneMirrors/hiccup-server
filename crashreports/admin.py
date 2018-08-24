from django.contrib import admin
from crashreports.models import Crashreport
from crashreports.models import Device
from crashreports.models import HeartBeat
from crashreports.models import LogFile


@admin.register(Crashreport)
class CrashreportAdmin(admin.ModelAdmin):
    pass


@admin.register(HeartBeat)
class CrashreportAdmin(admin.ModelAdmin):
    pass


@admin.register(LogFile)
class CrashreportAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class CrashreportAdmin(admin.ModelAdmin):
    pass
