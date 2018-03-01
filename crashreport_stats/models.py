from django.db import models
from crashreports.models import *
from django.db.models import F
from django.db.models.signals import post_save
import datetime


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


class RadioVersion(_VersionStats):
    radio_version = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.radio_version

class RadioVersionDaily(_DailyVersionStats):
    version = models.ForeignKey(RadioVersion, db_index=True, related_name='daily_stats',
            on_delete=models.CASCADE)
