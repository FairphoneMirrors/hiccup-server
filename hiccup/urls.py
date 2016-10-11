from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^hiccup/admin/', admin.site.urls),
    url(r'^hiccup/', include('crashreports.urls')),
    url(r'^accounts/login/$', auth_views.login),
#    url(r'^.*$', RedirectView.as_view(url='https://fairphone.com', permanent=False), name='index')
]
