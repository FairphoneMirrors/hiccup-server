# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 10:30
from __future__ import unicode_literals

import crashreports.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crashreport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_fake_report', models.BooleanField(default=False)),
                ('app_version', models.IntegerField()),
                ('uptime', models.CharField(max_length=200)),
                ('build_fingerprint', models.CharField(max_length=200)),
                ('boot_reason', models.CharField(max_length=200)),
                ('power_on_reason', models.CharField(max_length=200)),
                ('power_off_reason', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('device_local_id', models.PositiveIntegerField(blank=True)),
                ('next_logfile_key', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=64, unique=True)),
                ('imei', models.CharField(blank=True, max_length=32, null=True)),
                ('board_date', models.DateTimeField(blank=True, null=True)),
                ('chipset', models.CharField(blank=True, max_length=200, null=True)),
                ('last_heartbeat', models.DateTimeField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('next_per_crashreport_key', models.PositiveIntegerField(default=1)),
                ('next_per_heartbeat_key', models.PositiveIntegerField(default=1)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Hiccup_Device', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HeartBeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_version', models.IntegerField()),
                ('uptime', models.CharField(max_length=200)),
                ('build_fingerprint', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('device_local_id', models.PositiveIntegerField(blank=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crashreports.Device')),
            ],
        ),
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logfile_type', models.TextField(default='last_kmsg', max_length=36)),
                ('logfile', models.FileField(upload_to=crashreports.models.crashreport_file_name)),
                ('crashreport_local_id', models.PositiveIntegerField(blank=True)),
                ('crashreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crashreports.Crashreport')),
            ],
        ),
        migrations.AddField(
            model_name='crashreport',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crashreports.Device'),
        ),
        migrations.AddField(
            model_name='crashreport',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
