# -*- coding: utf-8 -*-

"""Migrations to set the unique constraints and drop duplicates."""
# pylint: disable=invalid-name
import logging

from django.db import migrations, models, connection
from django.db.models import Count, Min

from crashreports.models import HeartBeat, Crashreport

LOGGER = logging.getLogger(__name__)


def drop_heartbeat_duplicates(apps, schema_editor):
    """Drop duplicate heartbeat entries."""
    # pylint: disable=unused-argument
    find_and_drop_duplicates(HeartBeat)


def drop_crashreport_duplicates(apps, schema_editor):
    """Drop duplicate crashreport entries."""
    # pylint: disable=unused-argument
    find_and_drop_duplicates(Crashreport)


def find_and_drop_duplicates(object_type):
    """Drop all duplicates of the given object type."""
    unique_fields = ("device", "date")
    duplicates = (
        object_type.objects.values(*unique_fields)
        .order_by()
        .annotate(min_id=Min("id"), num_duplicates=Count("id"))
        .filter(num_duplicates__gt=1)
    )

    LOGGER.info(
        "Found %d %s instances that have duplicates. These will be removed.",
        duplicates.count(),
        object_type.__name__,
    )
    for duplicate in duplicates:
        LOGGER.debug("Removing duplicates: %s", duplicate)
        (
            object_type.objects.filter(
                device=duplicate["device"], date=duplicate["date"]
            )
            .exclude(id=duplicate["min_id"])
            .delete()
        )

    # Manually commit the data migration before schema migrations are applied
    connection.cursor().execute("COMMIT;")


class Migration(migrations.Migration):
    """Change heartbeat date field, set unique constraints, drop duplicates."""

    dependencies = [("crashreports", "0005_add_fp_staff_group")]

    operations = [
        migrations.AlterField(
            model_name="heartbeat",
            name="date",
            field=models.DateField(db_index=True),
        ),
        migrations.RunPython(
            drop_heartbeat_duplicates, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            drop_crashreport_duplicates, reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterUniqueTogether(
            name="crashreport", unique_together=set([("device", "date")])
        ),
        migrations.AlterUniqueTogether(
            name="heartbeat", unique_together=set([("device", "date")])
        ),
    ]
