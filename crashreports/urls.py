from django.conf.urls import url
from . import rest_api_devices
from . import rest_api_crashreports
from . import rest_api_heartbeats
from . import rest_api_logfiles


urlpatterns = [
    url(r'^api/v1/crashreports/$',
        rest_api_crashreports.ListCreateView.as_view(),
        name='api_v1_crashreports'),
    url(r'^api/v1/devices/(?P<uuid>[a-f0-9-]+)/crashreports/$',
        rest_api_crashreports.ListCreateView.as_view(),
        name='api_v1_crashreports_by_uuid'),
    url(r'^api/v1/crashreports/(?P<id>[0-9]+)/$',
        rest_api_crashreports.RetrieveUpdateDestroyView.as_view(),
        name='api_v1_crashreport'),
    url(r'^api/v1/devices/(?P<device__uuid>[a-f0-9-]+)/crashreports/' +
        '(?P<device_local_id>[0-9]+)/$',
        rest_api_crashreports.RetrieveUpdateDestroyView.as_view(),
        name='api_v1_crashreports_by_uuid'),

    # url(r'^api/v1/logfile_put$',
    #     rest_api_logfiles.logfile_put,
    #     name='api_v1_crashreports_put_logfile'),

    url(r'^api/v1/heartbeats/$',
        rest_api_heartbeats.ListCreateView.as_view(),
        name='api_v1_heartbeats'),
    url(r'^api/v1/devices/(?P<uuid>[a-f0-9-]+)/heartbeats/$',
        rest_api_heartbeats.ListCreateView.as_view(),
        name='api_v1_heartbeats_by_uuid'),
    url(r'^api/v1/heartbeats/(?P<id>[0-9]+)/$',
        rest_api_heartbeats.RetrieveUpdateDestroyView.as_view(),
        name='api_v1_heatbeat'),
    url(r'^api/v1/devices/(?P<device__uuid>[a-f0-9-]+)/heartbeats/' +
        '(?P<device_local_id>[0-9]+)/$',
        rest_api_heartbeats.RetrieveUpdateDestroyView.as_view(),
        name='api_v1_heartbeat_by_uuid'),

    url(r'^api/v1/devices/$', rest_api_devices.ListCreateDevices.as_view(),
        name='api_v1_list_devices'),
    url(r'^api/v1/devices/(?P<uuid>[a-f0-9-]+)/$',
        rest_api_devices.RetrieveUpdateDestroyDevice.as_view(),
        name='api_v1_retrieve_device'),
    url(r'^api/v1/devices/register/$', rest_api_devices.register_device,
        name='api_v1_register_device'),
]
