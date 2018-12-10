# -*- coding: utf-8 -*-
"""Migrations to add a default site which is required for the allauth plugin."""
# pylint: disable=invalid-name
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import migrations, IntegrityError

LOGGER = logging.getLogger(__name__)


def create_default_site(apps, schema_editor):
    """Create a default site instance if it does not exist."""
    # pylint: disable=unused-argument

    if not Site.objects.filter(id=settings.SITE_ID).exists():
        try:
            Site.objects.create(id=settings.SITE_ID)
        except IntegrityError as e:
            LOGGER.error(
                "Failed to create a site with id %d. Either adapt the SITE_ID "
                "setting or remove the currently existing site.",
                settings.SITE_ID,
            )
            raise e


class Migration(migrations.Migration):
    """Run the migration script."""

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("crashreport_stats", "0005_remove_manual_default_value"),
    ]

    operations = [migrations.RunPython(create_default_site)]
