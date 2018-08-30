"""Admin interface for manipulating devices, crashreports and heartbeats."""

from django.contrib import admin
from crashreports.models import Crashreport
from crashreports.models import Device
from crashreports.models import HeartBeat
from crashreports.models import LogFile


@admin.register(Crashreport)
class CrashreportAdmin(admin.ModelAdmin):
    """Manage Crashreports as admin user."""

    pass


@admin.register(HeartBeat)
class CrashreportAdmin(admin.ModelAdmin):
    """Manage HeartBeats as admin user."""

    pass


@admin.register(LogFile)
class CrashreportAdmin(admin.ModelAdmin):
    """Manage LogFiles as admin user."""

    pass


@admin.register(Device)
class CrashreportAdmin(admin.ModelAdmin):
    """Manage Devices as admin user."""

    pass
