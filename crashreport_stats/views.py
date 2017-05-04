from crashreports.models import *
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from itertools import chain
from django.db import connection
from  crashreport_stats import raw_querys
from django.contrib.auth.decorators import user_passes_test
from django import forms
from django.contrib import messages
from django.urls import reverse

def is_fairphone_staff(user):
    return user.groups.filter(name='FairphoneSoftwareTeam').exists()


class DeviceUUIDForm(forms.Form):
    uuid = forms.CharField(label='Device UUID:', max_length=100)

@user_passes_test(is_fairphone_staff)
def device_stats(request):
    template = loader.get_template('crashreport_stats/device.html')
    uuid = request.GET.get('uuid', "NO_UUID")
    if not Device.objects.filter(uuid=uuid).exists():
        raise Http404("Device doesn't exist.")
    return HttpResponse(template.render({'uuid':uuid}, request))
    
@user_passes_test(is_fairphone_staff)
def home(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeviceUUIDForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data['uuid']
            if not Device.objects.filter(uuid=uuid).exists():
                messages.warning(request, "Device does not exist")
            else:
                return HttpResponseRedirect(reverse("hiccup_stats_device")+'?uuid='+uuid)
    else:
        form = DeviceUUIDForm()
    template = loader.get_template('crashreport_stats/home.html')
    return HttpResponse(template.render({'form':form}, request))