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
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from crashreports.forms import CrashreportForm
from crashreports.models import Crashreport
from serializers import CrashReportSerializer


@ratelimit( key='ip', rate='100/h')
@csrf_exempt
def index(request):
    # Handle file upload`
    if request.method == 'POST':
        form = CrashreportForm(request.POST, request.FILES)
        if form.is_valid():
            # DEAL with the old version of the app:
            if 'app_version' not in request.POST:
                app_version = 0
                boot_reason=form.cleaned_data['boot_reason'],
                report_type = "FAKE_REPORT" if boot_reason == "FAKECRASH" else "CRASH_REPORT",
            else:
                app_version = form.cleaned_data['app_version']
                boot_reason = form.cleaned_data['boot_reason']
                report_type = form.cleaned_data["report_type"]

            new_cr = Crashreport(uuid=form.cleaned_data['uuid'],
                        aux_data=form.cleaned_data['aux_data'],
                        uptime=form.cleaned_data['uptime'],
                        boot_reason=boot_reason,
                        power_on_reason=form.cleaned_data['power_on_reason'],
                        power_off_reason=form.cleaned_data['power_off_reason'],
                        build_fingerprint=form.cleaned_data['build_fingerprint'],
                        date=form.cleaned_data['date'],
                        app_version = app_version,
                        report_type = report_type)

            try:
                new_cr.crashreport_file = request.FILES['crashreport']
            except:
                new_cr.crashreport_file = None

            new_cr.save()
            # Redirect to the document list after POST
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

@login_required
def hiccup_stats(request):
    template = loader.get_template('crashreports/hiccup_stats.html')
    return HttpResponse(template.render({}, request))


@login_required
def serve_saved_crashreport (request, path):
    if settings.DEBUG == False:
        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={0}".format(
            os.path.basename(path))
        response['X-Accel-Redirect'] = "/hiccup/protected/{0}".format(path)
        return response
    else:
        return serve(request, os.path.basename(path), os.path.dirname(settings.BASE_DIR + "/crashreport_uploads/" + path))


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
