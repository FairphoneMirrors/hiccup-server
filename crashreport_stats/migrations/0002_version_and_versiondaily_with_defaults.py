# -*- coding: utf-8 -*-
#
# Set the default values for the Version and VersionDaily models.
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("crashreport_stats", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="version",
            name="first_seen_on",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="version",
            name="heartbeats",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="version",
            name="other",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="version",
            name="prob_crashes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="version",
            name="released_on",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="version",
            name="smpl",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="versiondaily",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="versiondaily",
            name="heartbeats",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="versiondaily",
            name="other",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="versiondaily",
            name="prob_crashes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="versiondaily",
            name="smpl",
            field=models.IntegerField(default=0),
        ),
    ]
