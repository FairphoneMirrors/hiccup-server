# -*- coding: utf-8 -*-
#
# Extend the Crashreport and Heartbeat models to support the radio version.
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("crashreports", "0002_auto_20170502_1155")]

    operations = [
        migrations.AddField(
            model_name="crashreport",
            name="radio_version",
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="heartbeat",
            name="radio_version",
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]
