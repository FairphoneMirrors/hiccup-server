# -*- coding: utf-8 -*-
import django_filters
from rest_framework import filters
from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from crashreports.models import Crashreport
from crashreports.serializers import CrashReportSerializer


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
        return super(ListFilter, self).filter(
            qs, django_filters.fields.Lookup(value_list, 'in'))


class CrashreportFilter(filters.FilterSet):
    start_date = django_filters.DateTimeFilter(name="date", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(name="date", lookup_expr='lte')
    boot_reason = ListFilter(name='boot_reason')

    class Meta:
        model = Crashreport
        fields = ['build_fingerprint', 'boot_reason',
                  'power_on_reason', 'power_off_reason']


class CrashreportViewSet(viewsets.ModelViewSet):
    queryset = Crashreport.objects.all()
    serializer_class = CrashReportSerializer
    permission_classes = [IsCreationOrIsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CrashreportFilter
