from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework import filters


router = routers.DefaultRouter()
router.register(r'crashreports', views.CrashreportViewSet)

urlpatterns = [
    url(r'^crashreport/', views.index, name='index'),
    url(r'^crashreports/hiccup_stats/', views.hiccup_stats, name='home'),
    url(r'^crashreport_uploads/(?P<path>.*)$', views.serve_saved_crashreport, name='serve_saved_crashreport'),
    url(r'^', include(router.urls)),
]
