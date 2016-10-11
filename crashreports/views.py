# -*- coding: utf-8 -*-
import datetime
import django_filters
import os
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from ratelimit.decorators import ratelimit

from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework import viewsets

import rest_framework

from crashreports.models import Crashreport

from crashreports.serializers import CrashReportSerializer

# @login_required
# def serve_saved_crashreport (request, path):
#     if settings.DEBUG == False:
#         response = HttpResponse()
#         response["Content-Disposition"] = "attachment; filename={0}".format(
#             os.path.basename(path))
#         response['X-Accel-Redirect'] = "/hiccup/protected/{0}".format(path)
#         return response
#     else:
#         return serve(request, os.path.basename(path), os.path.dirname(settings.BASE_DIR + "/crashreport_uploads/" + path))


class IsCreationOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True



class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        value_list = value.split(u',')
        return super(ListFilter, self).filter(qs, django_filters.fields.Lookup(value_list, 'in'))


class CrashreportFilter(filters.FilterSet):
    start_date = django_filters.DateTimeFilter(name="date", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(name="date", lookup_expr='lte')
    boot_reason = ListFilter(name='boot_reason')
    class Meta:
        model = Crashreport
        fields = ['build_fingerprint','boot_reason', 'power_on_reason', 'power_off_reason']

class CrashreportViewSet(viewsets.ModelViewSet):
    queryset = Crashreport.objects.all()
    serializer_class =  CrashReportSerializer
    permission_classes = [IsCreationOrIsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CrashreportFilter
