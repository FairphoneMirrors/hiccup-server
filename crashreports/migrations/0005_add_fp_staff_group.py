# -*- coding: utf-8 -*-

"""Migrations for creating the Fairphone staff authentication group."""
# pylint: disable=invalid-name

from django.contrib.auth.models import Group
from django.db import migrations

from hiccup.allauth_adapters import FP_STAFF_GROUP_NAME


def add_fp_staff_group(apps, schema_editor):
    """Create the Fairphone staff group if it does not exist."""
    # pylint: disable=unused-argument

    if not Group.objects.filter(name=FP_STAFF_GROUP_NAME).exists():
        Group.objects.create(name=FP_STAFF_GROUP_NAME)


class Migration(migrations.Migration):
    """Run the migration script."""

    dependencies = [("crashreports", "0004_update_logfile_paths")]

    operations = [migrations.RunPython(add_fp_staff_group)]
