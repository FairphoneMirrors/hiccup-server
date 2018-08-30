"""URLs for accessing the Hiccup statistics."""

from django.conf.urls import url
from . import views
from . import rest_endpoints


urlpatterns = [
    # Single device statistics page
    url(r"^device/$", views.device_stats, name="hiccup_stats_device"),
    # Home page with device search form
    url(r"^$", views.home, name="device"),
    # Version statistics overview pages
    url(r"^versions/$", views.versions_overview, name="hiccup_stats_versions"),
    url(
        r"^versions/all/$",
        views.versions_all_overview,
        name="hiccup_stats_versions_all",
    ),
    # Single device statistics API
    url(
        r"^api/v1/device_overview/(?P<uuid>[a-f0-9-]+)/$",
        rest_endpoints.DeviceStat.as_view(),
        name="hiccup_stats_api_v1_device_overview",
    ),
    url(
        r"^api/v1/device_update_history/(?P<uuid>[a-f0-9-]+)/$",
        rest_endpoints.DeviceUpdateHistory.as_view(),
        name="hiccup_stats_api_v1_device_update_history",
    ),
    url(
        r"^api/v1/device_report_history/(?P<uuid>[a-f0-9-]+)/$",
        rest_endpoints.DeviceReportHistory.as_view(),
        name="hiccup_stats_api_v1_device_report_history",
    ),
    url(
        r"^api/v1/logfile_download/(?P<id>[0-9]+)/$",
        rest_endpoints.LogFileDownload.as_view(),
        name="hiccup_stats_api_v1_logfile_download",
    ),
    # Version statistics API
    url(
        r"^api/v1/versions/$",
        rest_endpoints.VersionListView.as_view(),
        name="hiccup_stats_api_v1_versions",
    ),
    url(
        r"^api/v1/version_daily/$",
        rest_endpoints.VersionDailyListView.as_view(),
        name="hiccup_stats_api_v1_version_daily",
    ),
    url(
        r"^api/v1/radio_versions/$",
        rest_endpoints.RadioVersionListView.as_view(),
        name="hiccup_stats_api_v1_radio_versions",
    ),
    url(
        r"^api/v1/radio_version_daily/$",
        rest_endpoints.RadioVersionDailyListView.as_view(),
        name="hiccup_stats_api_v1_radio_version_daily",
    ),
    # General statistics API
    url(
        r"^api/v1/status/$",
        rest_endpoints.Status.as_view(),
        name="hiccup_stats_api_v1_status",
    ),
]
