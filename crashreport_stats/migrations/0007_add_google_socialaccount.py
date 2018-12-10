# -*- coding: utf-8 -*-
"""Migrations to add the Google social account for the allauth plugin."""
# pylint: disable=invalid-name
import logging

from allauth.socialaccount.models import SocialApp

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import migrations

LOGGER = logging.getLogger(__name__)

SOCIALACCOUNT_GOOGLE_NAME = "Google"
SOCIALACCOUNT_GOOGLE_PROVIDER = "google"


def create_google_socialaccount(apps, schema_editor):
    """Create the Google social account.

    The account is only created if it does not exist yet and the
    SOCIALACCOUNT_GOOGLE_CLIENT_ID and the SOCIALACCOUNT_GOOGLE_SECRET
    settings are set.
    """
    # pylint: disable=unused-argument

    if not SocialApp.objects.filter(name=SOCIALACCOUNT_GOOGLE_NAME).exists():
        if (
            settings.SOCIALACCOUNT_GOOGLE_CLIENT_ID
            and settings.SOCIALACCOUNT_GOOGLE_SECRET
        ):
            google_socialapp = SocialApp.objects.create(
                name=SOCIALACCOUNT_GOOGLE_NAME,
                provider=SOCIALACCOUNT_GOOGLE_PROVIDER,
                client_id=settings.SOCIALACCOUNT_GOOGLE_CLIENT_ID,
                secret=settings.SOCIALACCOUNT_GOOGLE_SECRET,
            )
            google_socialapp.sites.add(Site.objects.get(id=settings.SITE_ID))
            google_socialapp.save()
        else:
            LOGGER.info(
                "The Google socialaccount configuration was not created. Set "
                "the SOCIALACCOUNT_GOOGLE_CLIENT_ID and "
                "SOCIALACCOUNT_GOOGLE_SECRET settings and re-run the "
                "migration to create it."
            )


class Migration(migrations.Migration):
    """Run the migration script."""

    dependencies = [
        ("socialaccount", "0003_extra_data_default_dict"),
        ("crashreport_stats", "0006_add_default_site"),
    ]

    operations = [migrations.RunPython(create_google_socialaccount)]
