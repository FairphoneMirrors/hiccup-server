from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework import filters

router = routers.DefaultRouter()
router.register(r'crashreports', views.CrashreportViewSet)

urlpatterns = [
    url(r'^crashreport/', views.index, name='index'),
    url(r'^crashreports/hiccup_stats/', views.hiccup_stats, name='home'),
    url(r'^', include(router.urls)),
]
