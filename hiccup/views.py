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

import datetime
import time

@csrf_exempt
def index(request):
    # Handle file upload`
    if request.method == 'POST':
        form = CrashreportForm(request.POST, request.FILES)
        if form.is_valid():
            print form.cleaned_data['uuid'];
            print form.cleaned_data['aux_data'];
            print form.cleaned_data['boot_reason'];
            print form.cleaned_data['build_fingerprint'];
            print form.cleaned_data['date'];
            new_cr = Crashreport(uuid=form.cleaned_data['uuid'],
                        aux_data=form.cleaned_data['aux_data'],
                        uptime=form.cleaned_data['uptime'],
                        boot_reason=form.cleaned_data['boot_reason'],
                        power_on_reason=form.cleaned_data['power_on_reason'],
                        power_off_reason=form.cleaned_data['power_off_reason'],
                        build_fingerprint=form.cleaned_data['build_fingerprint'],
                        date= form.cleaned_data['date'])
            try:
                new_cr.crashreport_file = request.FILES['crashreport']
            except:
                new_cr.crashreport_file = None
            new_cr.save()
            # Redirect to the document list after POST
            return HttpResponse(status=204)
        else:
             return HttpResponse(status=204)
    else:
        raise HttpResponse(status=204) 


# @login_required
# def list_crash_reports(request):
#     context = {
#         'request':request,
#         'crashreport_count':  Crashreport.objects.count(),
#         'unique_devices': Crashreport.objects.values("uuid").distinct().count(),
#         'log_count': Crashreport.objects.exclude(crashreport_file='').count(),
#         'crashreport_hist' : Crashreport.objects.all().order_by('-date')[:5]
#        }
#     return render_to_response('crashreports/list.html',context)


@login_required
def get_crash_statistic(request):
    from_date = request.GET.get('from_date', "2016-01-01")
    to_date = request.GET.get('to_date', "2017-01-01")
    print from_date
    print to_date
    entries = Crashreport.objects.filter(date__range=[from_date, to_date]).extra({'date_created' : "date(date)"}).values('date_created').annotate(created_count=Count('id'))
    for entry in entries:
        entry['date_created']=time.mktime(datetime.datetime.strptime(entry['date_created'], "%Y-%m-%d").timetuple())*1000
    return  render_to_response('crashreports/json/crashreport_by_day.html/', {
        'entries' : entries
    })
