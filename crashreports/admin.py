from django.contrib import admin
from crashreports.models import Crashreport


@admin.register(Crashreport)
class CrashreportAdmin(admin.ModelAdmin):
    pass
