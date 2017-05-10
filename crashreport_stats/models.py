from django.db import models
from crashreports.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


def getVersion(build_fingerprint):
    v= None
    try: 
        v = Version.objects.get(build_fingerprint=build_fingerprint)
    except Version.DoesNotExist:
        v =Version(build_fingerprint=build_fingerprint,
            first_seen_on=datetime.date.today(),
            released_on=datetime.date.today(),
            heartbeats=0, prob_crashes=0, smpl=0, other=0)
        v.save()
    return v

def getVersionDaily(version,day):
    try: 
        v = VersionDaily.objects.get(version=version, date=day)
    except VersionDaily.DoesNotExist:
        v =VersionDaily(version=version, date=day,
            heartbeats=0, prob_crashes=0, smpl=0, other=0)
    return v

@receiver(post_save, sender=Crashreport)
def on_crashreport_create(sender, **kwargs):
    crashreport = kwargs.get('instance')
    v= getVersion(crashreport.build_fingerprint)
    vd = getVersionDaily(v, crashreport.date.date())
    if crashreport.boot_reason == "RTC alarm":
        v.smpl = v.smpl + 1
        vd.smpl = vd.smpl + 1
    elif crashreport.boot_reason in ["UNKNOWN", "keyboard power on"]:
        v.prob_crashes = v.prob_crashes + 1
        vd.prob_crashes = vd.prob_crashes + 1
    else:
        v.other = v.other + 1
        vd.other = vd.other + 1
    v.save()
    vd.save()

@receiver(post_save, sender=HeartBeat)
def on_heartbeat_create(sender, **kwargs):
    hb = kwargs.get('instance')
    v  = getVersion(hb.build_fingerprint)
    vd = getVersionDaily(v, hb.date)
    v.heartbeats = v.heartbeats + 1
    vd.heartbeats = vd.heartbeats + 1
    v.save()
    vd.save()


class Version(models.Model):
    build_fingerprint    = models.CharField(max_length=200,  unique=True)
    is_official_release = models.BooleanField(default=False)
    is_beta_release     = models.BooleanField(default=False)
    first_seen_on        = models.DateField()
    released_on          = models.DateField()
    heartbeats           = models.IntegerField()
    prob_crashes         = models.IntegerField()
    smpl                 = models.IntegerField()
    other                = models.IntegerField()
    def __str__(self):
        return self.build_fingerprint
    
    
class VersionDaily(models.Model):
    version        = models.ForeignKey(Version, db_index=True, related_name='daily_stats', on_delete=models.CASCADE)
    date           = models.DateField()
    heartbeats     = models.IntegerField()
    prob_crashes   = models.IntegerField()
    smpl           = models.IntegerField()
    other          = models.IntegerField()
