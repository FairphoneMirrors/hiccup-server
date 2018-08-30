"""Define all Hiccup REST API URLs."""

from django.conf.urls import include, url
from django.contrib import admin
from drf_yasg import openapi

api_info = openapi.Info(  # pylint: disable=C0103
    title="Hiccup API", default_version="v1"
)

urlpatterns = [
    url(r"^hiccup/admin/", admin.site.urls),
    url(r"^hiccup/", include("crashreports.urls")),
    url(r"^hiccup_stats/", include("crashreport_stats.urls")),
    url(r"^accounts/", include("allauth.urls")),
]
