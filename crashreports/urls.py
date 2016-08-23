from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^crashreport/', views.index, name='index'),
    url(r'^get_crash_statistic', views.get_crash_statistic, name='get_crash_statistic'),
    url(r'', views.empty, name='empty'),]
