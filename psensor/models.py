    # -*- coding: utf-8 -*-
from django.db import models

class PSensorSetting(models.Model):
    uuid = models.CharField(max_length=255)
    appVersion = models.CharField(max_length=255)
    old_offset = models.IntegerField()
    old_near_threshold = models.IntegerField()
    old_far_threshold = models.IntegerField()
    new_offset = models.IntegerField()
    new_near_threshold = models.IntegerField()
    new_far_threshold = models.IntegerField()
    timestamp = models.DateTimeField()
