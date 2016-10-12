from django.conf.urls import url, include
from . import views
from . import rest_api_devices
from . import rest_api_crashreports
from . import rest_api_heartbeats

urlpatterns = [
    url(r'^api/v1/crashreports/$', rest_api_crashreports.ListCreateCrashReport.as_view(), name='api_v1_crashreports'),
    # url(r'^api/v1/crashreports/(?P<pk>[0-9]+)/$', views.index, name='api_v1_crashreports_single'),    
    #url(r'^api/v1/crashreports/(?P<pk>[0-9]+)/logfiles/$', views.index, name='api_v1_crashreports_single_logfiles'),
    # url(r'^api/v1/crashreports/(?P<pk>[0-9]+)/logfiles/(?P<pk>[0-9]+)/$', views.index, name='api_v1_crashreports_single_logfiles_single'),
    
    url(r'^api/v1/heartbeats/$', rest_api_heartbeats.ListCreateHeartBeat.as_view(), name='api_v1_heartbeat'),

    # 
    # url(r'^api/v1//logfiles/$',views.index, name='api_v1_logfiles'),
    # url(r'^api/v1//logfiles/(?P<pk>[0-9]+)/$',views.index, name='api_v1_logfiles_single')

    url(r'^api/v1/devices/$', rest_api_devices.ListCreateDevices.as_view(), name='api_v1_list_devices'),
    url(r'^api/v1/devices/(?P<uuid>[a-f0-9-]+)/$', rest_api_devices.RetrieveUpdateDestroyDevice.as_view(), name='api_v1_retrieve_device'),
    url(r'^api/v1/devices/register/$', rest_api_devices.register_device, name='api_v1_register_device'),
]
