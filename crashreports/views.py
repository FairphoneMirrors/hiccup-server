# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from crashreports.models import Crashreport
from crashreports.forms import CrashreportForm
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from rest_framework import viewsets
from serializers import CrashReportSerializer
from rest_framework.permissions import BasePermission
from rest_framework import filters
from rest_framework import generics
import django_filters
from django.template import loader


import datetime
import time

from ratelimit.decorators import ratelimit

@ratelimit( key='ip', rate='100/h')
@csrf_exempt
def index(request):
    # Handle file upload`
    if request.method == 'POST':
        form = CrashreportForm(request.POST, request.FILES)
        if form.is_valid():
            new_cr = Crashreport(uuid=form.cleaned_data['uuid'],
                        aux_data=form.cleaned_data['aux_data'],
                        uptime=form.cleaned_data['uptime'],
                        boot_reason=form.cleaned_data['boot_reason'],
                        power_on_reason=form.cleaned_data['power_on_reason'],
                        power_off_reason=form.cleaned_data['power_off_reason'],
                        build_fingerprint=form.cleaned_data['build_fingerprint'],
                        date=form.cleaned_data['date'])
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
