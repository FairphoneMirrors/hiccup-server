from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^hiccup/admin/', admin.site.urls),
    url(r'^psensor/', include('psensor.urls')),
    url(r'^hiccup/', include('crashreports.urls')),
]
