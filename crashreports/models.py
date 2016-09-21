    # -*- coding: utf-8 -*-
from django.db import models
import datetime

def crashreport_file_name(instance, filename):
    return '/'.join(["crashreport_uploads", instance.uuid, str(datetime.date.today().year), str(datetime.date.today().month), str(datetime.date.today().day), filename])


class Crashreport(models.Model):
    uuid = models.CharField(max_length=200)
    report_type = models.CharField(max_length=200)
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField(max_length=200)
    boot_reason = models.CharField(max_length=200)
    power_on_reason = models.CharField(max_length=200)
    power_off_reason = models.CharField(max_length=200)
    aux_data = models.CharField(max_length=200)
    date = models.DateTimeField()
    crashreport_file = models.FileField(upload_to=crashreport_file_name, null=True, blank=True)

    def crashreport_file_link(self):
        if self.crashreport_file:
            return '<a href="/hiccup/' + str(self.crashreport_file.url) + '">' + 'Logfile' + '</a>'
        else:
            return '<a href="''"></a>'

    crashreport_file_link.allow_tags = True
    crashreport_file_link.short_description = "File Link"
