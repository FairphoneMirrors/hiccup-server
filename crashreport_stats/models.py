from django.db import models
from crashreports.models import *
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


@receiver(post_save, sender=Crashreport)
def on_crashreport_create(sender, **kwargs):
    crashreport = kwargs.get('instance')
    v, _ = Version.objects.get_or_create(build_fingerprint=crashreport.build_fingerprint)
    vd, _ = VersionDaily.objects.get_or_create(version=v, date=crashreport.date)
    stats = [v, vd]

    if crashreport.boot_reason == "RTC alarm":
        for element in stats:
            element.smpl = F('smpl') + 1
    elif crashreport.boot_reason in ["UNKNOWN", "keyboard power on"]:
        for element in stats:
            element.prob_crashes = F('prob_crashes') + 1
    else:
        for element in stats:
            element.other = F('other') + 1

    for element in stats:
        element.save()


@receiver(post_save, sender=HeartBeat)
def on_heartbeat_create(sender, **kwargs):
    hb = kwargs.get('instance')

    v, _ = Version.objects.get_or_create(build_fingerprint=hb.build_fingerprint)
    vd, _ = VersionDaily.objects.get_or_create(version=v, date=hb.date)

    for element in [v, vd]:
        element.heartbeats = F('heartbeats') + 1
        element.save()


class _VersionStats(models.Model):
    is_official_release = models.BooleanField(default=False)
    is_beta_release = models.BooleanField(default=False)
    first_seen_on = models.DateField(auto_now_add=True)
    released_on = models.DateField(auto_now_add=True)
    heartbeats = models.IntegerField(default=0)
    prob_crashes = models.IntegerField(default=0)
    smpl = models.IntegerField(default=0)
    other = models.IntegerField(default=0)

    class Meta:
        abstract = True

class _DailyVersionStats(models.Model):
    date  = models.DateField(auto_now_add=True)
    heartbeats = models.IntegerField(default=0)
    prob_crashes = models.IntegerField(default=0)
    smpl = models.IntegerField(default=0)
    other = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Version(_VersionStats):
    build_fingerprint = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.build_fingerprint

class VersionDaily(_DailyVersionStats):
    version = models.ForeignKey(Version, db_index=True, related_name='daily_stats',
            on_delete=models.CASCADE)
