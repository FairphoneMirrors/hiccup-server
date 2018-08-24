"""Register models for admin site"""
from django.contrib import admin
from crashreport_stats.models import (
    Version,
    VersionDaily,
    RadioVersion,
    RadioVersionDaily,
)


admin.site.register(Version)
admin.site.register(RadioVersion)


@admin.register(VersionDaily, RadioVersionDaily)
class DailyVersionStatsAdmin(admin.ModelAdmin):
    """Admin for daily version stats."""

    list_display = ("version", "date")
