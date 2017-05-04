from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from crashreports.permissions import HasRightsOrIsDeviceOwnerDeviceCreation
from django.db import connection
from . import raw_querys
import zipfile
from crashreports.models import *

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class DeviceUpdateHistory(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None):
        cursor = connection.cursor()
        raw_querys.execute_device_update_history_query(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)

class DeviceReportHistory(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None):
        cursor = connection.cursor()
        raw_querys.execute_device_report_history(
            cursor,
            {
                'uuid': uuid
            })
        res = dictfetchall(cursor)
        return Response(res)

class DeviceStat(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, uuid, format=None, ):
        device          = Device.objects.filter(uuid=uuid)
        last_active     = HeartBeat.objects.filter(device=device).order_by('-date')[0].date
        heartbeats      = HeartBeat.objects.filter(device=device).count()
        crashreports    = Crashreport.objects.filter(device=device).filter(boot_reason__in=["UNKNOWN", "keyboard power on"]).count()
        crashes_per_day = crashreports*1.0/heartbeats if heartbeats > 0 else 0
        smpls           = Crashreport.objects.filter(device=device).filter(boot_reason__in=["RTC alarm"]).count()
        smpl_per_day    = smpls*1.0/heartbeats if heartbeats > 0 else 0
        return Response(
            {
                'uuid'            : uuid,
                'last_active'     : last_active,
                'heartbeats'      : heartbeats,
                'crashreports'    : crashreports,
                'crashes_per_day' : crashes_per_day,
                'smpls'           : smpls,
                'smpl_per_day'    : smpl_per_day
            })

class LogFileDownload(APIView):
    permission_classes = (HasRightsOrIsDeviceOwnerDeviceCreation, )
    def get(self, request, id, format=None):
        try:
            logfile = LogFile.objects.get(id=id)
        except:
            raise NotFound(detail="Logfile does not exist.")
        zf = zipfile.ZipFile(logfile.logfile.path)
        ret = {}
        for f in zf.filelist:
            fo = zf.open(f)
            ret[f.filename] = fo.read()
        return Response(ret)
