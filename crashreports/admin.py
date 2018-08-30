"""Admin interface for manipulating devices, crashreports and heartbeats."""

from django.contrib import admin
from crashreports.models import Crashreport
from crashreports.models import Device
from crashreports.models import HeartBeat
from crashreports.models import LogFile

admin.site.register(Crashreport)
admin.site.register(HeartBeat)
admin.site.register(LogFile)
admin.site.register(Device)
