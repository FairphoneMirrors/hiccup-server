from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^hiccup/admin/', admin.site.urls),
    url(r'^hiccup/psensor/', include('psensor.urls')),
    url(r'^hiccup/hiccup/', include('crashreports.urls')),
]
