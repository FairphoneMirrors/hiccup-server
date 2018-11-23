# -*- coding: utf-8 -*-

"""Migrations to update the path where logfiles are stored."""
# pylint: disable=invalid-name

import logging
import os
import shutil

from django.db import migrations
from django.conf import settings
from django.core.files.storage import default_storage

from crashreports.models import LogFile, crashreport_file_name

LOGGER = logging.getLogger(__name__)


def migrate_logfiles(apps, schema_editor):
    """Migrate the logfiles and update the logfile paths in the database."""
    # pylint: disable=unused-argument
    crashreport_uploads_dir = "crashreport_uploads"

    if not LogFile.objects.filter(
        logfile__startswith=crashreport_uploads_dir
    ).exists():
        LOGGER.info(
            "No old logfile path found. Assuming this is a new installation "
            "and the migration does not need to be applied."
        )
        return

    crashreport_uploads_legacy_dir = crashreport_uploads_dir + "_legacy"
    assert not os.path.isdir(crashreport_uploads_legacy_dir), (
        "Existing crashreport_uploads_legacy directory found. Remove this"
        "directory in order to run this migration."
    )

    if os.path.isdir(crashreport_uploads_dir):
        shutil.move(crashreport_uploads_dir, crashreport_uploads_legacy_dir)

    for logfile in LogFile.objects.all():
        migrate_logfile_instance(
            logfile, crashreport_uploads_dir, crashreport_uploads_legacy_dir
        )


def migrate_logfile_instance(
    logfile, crashreport_uploads_dir, crashreport_uploads_legacy_dir
):
    """Migrate a single logfile instance."""
    old_logfile_relative_path = logfile.logfile.name.replace(
        crashreport_uploads_dir, crashreport_uploads_legacy_dir, 1
    )
    old_logfile_absolute_path = os.path.join(
        settings.BASE_DIR, old_logfile_relative_path
    )
    new_logfile_path = crashreport_file_name(
        logfile, os.path.basename(old_logfile_relative_path)
    )
    LOGGER.info("Migrating %s", old_logfile_absolute_path)
    if os.path.isfile(old_logfile_absolute_path):
        update_logfile_path(logfile, new_logfile_path)
        move_logfile_file(old_logfile_absolute_path, new_logfile_path)
    else:
        LOGGER.warning("Logfile does not exist: %s", old_logfile_absolute_path)


def move_logfile_file(old_logfile_path, new_logfile_path):
    """Move a logfile to a new path and delete empty directories."""
    new_logfile_absolute_path = default_storage.path(new_logfile_path)

    LOGGER.debug("Creating directories for %s", new_logfile_absolute_path)
    os.makedirs(os.path.dirname(new_logfile_absolute_path), exist_ok=True)

    LOGGER.debug("Moving %s to %s", old_logfile_path, new_logfile_absolute_path)
    shutil.move(old_logfile_path, new_logfile_absolute_path)

    LOGGER.debug("Deleting empty directories from %s", old_logfile_path)
    os.removedirs(os.path.dirname(old_logfile_path))


def update_logfile_path(logfile, new_logfile_path):
    """Update the path of a logfile database instance."""
    LOGGER.debug(
        "Changing logfile path in database from %s to %s",
        logfile.logfile,
        new_logfile_path,
    )

    logfile.logfile = new_logfile_path
    logfile.save()


class Migration(migrations.Migration):
    """Run the migration script."""

    dependencies = [
        ("crashreports", "0003_crashreport_and_heartbeat_with_radio_version")
    ]

    operations = [migrations.RunPython(migrate_logfiles)]
