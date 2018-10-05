# -*- coding: utf-8 -*-

"""Migrations to update the path where logfiles are stored."""
# pylint: disable=invalid-name

import logging
import os
import shutil

from django.db import migrations
from django.conf import settings

from crashreports.models import LogFile, crashreport_file_name


def get_django_logger():
    """Get the Django logger instance."""
    logger_name = next(iter(settings.LOGGING["loggers"].keys()))
    return logging.getLogger(logger_name)


def migrate_logfiles(apps, schema_editor):
    """Migrate the logfiles and update the logfile paths in the database."""
    # pylint: disable=unused-argument

    logger = get_django_logger()

    crashreport_uploads_dir = "crashreport_uploads"
    crashreport_uploads_legacy_dir = "crashreport_uploads_legacy"
    if not os.path.isdir(crashreport_uploads_dir):
        logger.info(
            "%s directory not found. Assuming this is a new installation and "
            "the migration does not need to be applied.",
            os.path.join(settings.BASE_DIR, crashreport_uploads_dir),
        )
        return

    shutil.move(crashreport_uploads_dir, crashreport_uploads_legacy_dir)

    for logfile in LogFile.objects.all():
        migrate_logfile_instance(
            logfile, crashreport_uploads_dir, crashreport_uploads_legacy_dir
        )


def migrate_logfile_instance(
    logfile, crashreport_uploads_dir, crashreport_uploads_legacy_dir
):
    """Migrate a single logfile instance."""
    logger = get_django_logger()

    original_path = logfile.logfile.name
    old_logfile_path = original_path.replace(
        crashreport_uploads_dir, crashreport_uploads_legacy_dir, 1
    )
    new_logfile_path = crashreport_file_name(
        logfile, os.path.basename(original_path)
    )
    logger.info("Migrating %s", old_logfile_path)
    if os.path.isfile(old_logfile_path):
        update_logfile_path(logfile, new_logfile_path)
        move_logfile_file(old_logfile_path, new_logfile_path)
    else:
        logger.warning("Logfile does not exist: %s", old_logfile_path)


def move_logfile_file(old_logfile_path, new_logfile_path):
    """Move a logfile to a new path and delete empty directories."""
    logger = get_django_logger()

    logger.debug("Creating directories for %s", new_logfile_path)
    os.makedirs(os.path.dirname(new_logfile_path), exist_ok=True)

    logger.debug("Moving %s to %s", old_logfile_path, new_logfile_path)
    shutil.move(old_logfile_path, new_logfile_path)

    logger.debug("Deleting empty directories from %s", old_logfile_path)
    os.removedirs(os.path.dirname(old_logfile_path))


def update_logfile_path(logfile, new_logfile_path):
    """Update the path of a logfile database instance."""
    logger = get_django_logger()
    logger.debug(
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
