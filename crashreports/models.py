# -*- coding: utf-8 -*-
from django.db import models
from django.db import transaction

from django.contrib.auth.models import User
from taggit.managers import TaggableManager

import uuid


class Device(models.Model):
    def __str__( self ):
        return self.uuid
    # for every device there is a django user
    uuid = models.CharField( db_index=True,max_length=64, unique=True,
                            default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, related_name='Hiccup_Device', on_delete=models.CASCADE,
        unique=True)
    imei = models.CharField(max_length=32, null=True, blank=True)
    board_date = models.DateTimeField(null=True, blank=True)
    chipset = models.CharField(max_length=200, null=True, blank=True)
    tags = TaggableManager(blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=200, null=True, blank=True)
    next_per_crashreport_key = models.PositiveIntegerField(default=1)
    next_per_heartbeat_key = models.PositiveIntegerField(default=1)

    @transaction.atomic
    def get_crashreport_key(self):
        ret = self.next_per_crashreport_key
        self.next_per_crashreport_key = self.next_per_crashreport_key + 1
        self.save()
        return ret

    @transaction.atomic
    def get_heartbeat_key(self):
        ret = self.next_per_heartbeat_key
        self.next_per_heartbeat_key = self.next_per_heartbeat_key + 1
        self.save()
        return ret


def crashreport_file_name(instance, filename):
    return '/'.join([
        "crashreport_uploads",
        instance.crashreport.device.uuid,
        str(instance.crashreport.id),
        str(instance.crashreport.date),
        filename])


class Crashreport(models.Model):
    device = models.ForeignKey(Device, db_index=True, related_name='crashreports', on_delete=models.CASCADE)
    is_fake_report = models.BooleanField(default=False)
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField(db_index=True, max_length=200)
    boot_reason = models.CharField(db_index=True, max_length=200)
    power_on_reason = models.CharField(db_index=True, max_length=200)
    power_off_reason = models.CharField(db_index=True, max_length=200)
    date = models.DateTimeField(db_index=True)
    tags = TaggableManager(blank=True)
    device_local_id = models.PositiveIntegerField(blank=True)
    next_logfile_key = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @transaction.atomic
    def get_logfile_key(self):
        ret = self.next_logfile_key
        self.next_logfile_key = self.next_logfile_key + 1
        self.save()
        return ret

    def save(self, *args, **kwargs):
        if not self.device_local_id:
            self.device_local_id = self.device.get_crashreport_key()
        super(Crashreport, self).save(*args, **kwargs)

    def _get_uuid(self):
        "Returns the person's full name."
        return self.device.uuid
    uuid = property(_get_uuid)

#TODO remove logfile_type or make it meaningful
class LogFile(models.Model):
    logfile_type = models.TextField(max_length=36, default="last_kmsg")
    crashreport = models.ForeignKey(Crashreport,related_name='logfiles', on_delete=models.CASCADE)
    logfile = models.FileField(upload_to=crashreport_file_name, max_length=500)
    crashreport_local_id = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.crashreport_local_id:
            self.crashreport_local_id = self.crashreport.get_logfile_key()
        super(LogFile, self).save(*args, **kwargs)


class HeartBeat(models.Model):
    device = models.ForeignKey(Device,
        db_index=True,
        related_name='heartbeats',
        on_delete=models.CASCADE)
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField( db_index=True, max_length=200)
    date = models.DateTimeField(db_index=True)
    device_local_id = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.device_local_id:
            self.device_local_id = self.device.get_heartbeat_key()
        super(HeartBeat, self).save(*args, **kwargs)

    def _get_uuid(self):
        "Returns the person's full name."
        return self.device.uuid
    uuid = property(_get_uuid)
