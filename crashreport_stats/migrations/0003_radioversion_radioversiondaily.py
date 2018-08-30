# -*- coding: utf-8 -*-

"""Migrations to introduce the RadioVersion and RadioVersionDaily models."""

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Introduce the RadioVersion and RadioVersionDaily models."""

    dependencies = [
        ("crashreport_stats", "0002_version_and_versiondaily_with_defaults")
    ]

    operations = [
        migrations.CreateModel(
            name="RadioVersion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_official_release", models.BooleanField(default=False)),
                ("is_beta_release", models.BooleanField(default=False)),
                ("first_seen_on", models.DateField(auto_now_add=True)),
                ("released_on", models.DateField(auto_now_add=True)),
                ("heartbeats", models.IntegerField(default=0)),
                ("prob_crashes", models.IntegerField(default=0)),
                ("smpl", models.IntegerField(default=0)),
                ("other", models.IntegerField(default=0)),
                (
                    "radio_version",
                    models.CharField(max_length=200, unique=True),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="RadioVersionDaily",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("heartbeats", models.IntegerField(default=0)),
                ("prob_crashes", models.IntegerField(default=0)),
                ("smpl", models.IntegerField(default=0)),
                ("other", models.IntegerField(default=0)),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_stats",
                        to="crashreport_stats.RadioVersion",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
