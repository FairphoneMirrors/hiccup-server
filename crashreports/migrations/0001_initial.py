# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-23 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import crashreports.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crashreport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=200)),
                ('uptime', models.CharField(max_length=200)),
                ('build_fingerprint', models.CharField(max_length=200)),
                ('boot_reason', models.CharField(max_length=200)),
                ('power_on_reason', models.CharField(max_length=200)),
                ('power_off_reason', models.CharField(max_length=200)),
                ('aux_data', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('crashreport_file', models.FileField(blank=True, null=True, upload_to=crashreports.models.crashreport_file_name)),
            ],
        ),
    ]
