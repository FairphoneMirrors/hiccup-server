from crashreports.models import *
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from itertools import chain
from django.db import connection
from  crashreport_stats import raw_querys
from django.contrib.auth.decorators import user_passes_test

def is_fairphone_staff(user):
    return user.groups.filter(name='FairphoneSoftwareTeam').exists()

@user_passes_test(is_fairphone_staff)
def device_stats(request):
    template = loader.get_template('crashreport_stats/device.html')
    uuid = request.GET.get('uuid', "NO_UUID")
    return HttpResponse(template.render({'uuid':uuid}, request))
