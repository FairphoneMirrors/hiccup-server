"""Introduce the StatsMetadata model and remove broken default dates."""
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    """Introduce the StatsMetadata model and remove broken default dates."""

    dependencies = [
        ('crashreport_stats', '0003_radioversion_radioversiondaily'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsMetadata',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(default=None)),
            ],
        ),
        migrations.AlterField(
            model_name='radioversiondaily',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='versiondaily',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='radioversion',
            name='first_seen_on',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='radioversion',
            name='released_on',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='version',
            name='first_seen_on',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='version',
            name='released_on',
            field=models.DateField(),
        ),
    ]
