from django.conf.urls import url
from . import views
from . import rest_endpoints


urlpatterns = [
    url(r'^device/$',
        views.device_stats,
        name='hiccup_stats_device'),
    url(r'^$',
        views.home,
        name='device'),
    url(r'^versions/$',
        views.versions_overview,
        name='hiccup_stats_versions'),
    url(r'^versions/all/$',
        views.versions_all_overview,
        name='hiccup_stats_versions_all'),
    url(r'^api/v1/device_overview/(?P<uuid>[a-f0-9-]+)/$',
        rest_endpoints.DeviceStat.as_view(),
        name='hiccup_stats_api_v1_device_overview'),
    url(r'^api/v1/status/$',
        rest_endpoints.Status.as_view(),
        name='hiccup_stats_api_v1_status'),
    url(r'^api/v1/device_update_history/(?P<uuid>[a-f0-9-]+)/$',
        rest_endpoints.DeviceUpdateHistory.as_view(),
        name='hiccup_stats_api_v1_device_update_history'),
    url(r'^api/v1/device_report_history/(?P<uuid>[a-f0-9-]+)/$',
        rest_endpoints.DeviceReportHistory.as_view(),
        name='hiccup_stats_api_v1_device_report_history'),

    url(r'^api/v1/logfile_download/(?P<id>[0-9]+)/$',
        rest_endpoints.LogFileDownload.as_view(),
        name='hiccup_stats_api_v1_logfile_download'),
        
    url(r'^api/v1/versions/$',
        rest_endpoints.VersionListView.as_view(),
        name='hiccup_stats_api_v1_versions'),
    
    url(r'^api/v1/version_daily/$',
        rest_endpoints.VersionDailyListView.as_view(),
        name='hiccup_stats_api_v1_version_daily'),
]
