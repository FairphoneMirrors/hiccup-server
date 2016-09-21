# -*- coding: utf-8 -*-
from django import forms

class CrashreportForm(forms.Form):
    uuid = forms.CharField()
    uptime = forms.CharField()
    build_fingerprint = forms.CharField()
    boot_reason = forms.CharField()
    power_on_reason = forms.CharField()
    power_off_reason = forms.CharField()
    aux_data = forms.CharField()
    crashreport = forms.FileField(required=False)
    date = forms.DateTimeField()
    report_type = forms.CharField(required=False)
    app_version = forms.IntegerField(required=False)
