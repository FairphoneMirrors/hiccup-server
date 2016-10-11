    # -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import uuid

class Device(models.Model):
    # for every device there is a django user
    uuid           = models.CharField(max_length=64, unique=True, default=uuid.uuid4, editable=False)
    user           = models.OneToOneField(User, related_name='Hiccup_Device', on_delete=models.CASCADE, unique=True)
    imei           = models.CharField(max_length=32, null=True, blank=True)
    board_date     = models.DateTimeField(null=True, blank= True)
    chipset        = models.CharField(max_length=200, null=True, blank= True)
    tags           = TaggableManager(blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    token          = models.CharField(max_length=200, null=True, blank=True)

def crashreport_file_name(instance, filename):
    return '/'.join([
        "crashreport_uploads",
        instance.device.uuid,
        instance.crashreport.id,
        str(instance.crashreport.date),
        filename])

class Crashreport(models.Model):
    device            = models.ForeignKey(Device, on_delete=models.CASCADE)
    is_fake_report    = models.BooleanField(default=False)
    app_version       = models.IntegerField()
    uptime            = models.CharField(max_length=200)
    build_fingerprint = models.CharField(max_length=200)
    boot_reason       = models.CharField(max_length=200)
    power_on_reason   = models.CharField(max_length=200)
    power_off_reason  = models.CharField(max_length=200)
    date              = models.DateTimeField()
    tags = TaggableManager(blank=True)
    def _get_uuid(self):
        "Returns the person's full name."
        return self.device.uuid
    uuid = property(_get_uuid)
    

class LogFile(models.Model):
    logfile_type      = models.TextField(max_length=36)
    device       = models.ForeignKey(Device, on_delete=models.CASCADE)
    crashreport       = models.ForeignKey(Crashreport, on_delete=models.CASCADE)
    crashreport_file  = models.FileField(upload_to=crashreport_file_name)

class HeartBeat(models.Model):    
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField(max_length=200)
    date = models.DateTimeField()
