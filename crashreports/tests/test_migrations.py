"""Tests for the Django database migrations."""
import logging
import os
import tempfile
from datetime import datetime, date

import pytz
from django.test import TransactionTestCase, override_settings
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

from crashreports.models import Crashreport, HeartBeat, LogFile
from crashreports.tests.utils import Dummy


class MigrationTestCase(TransactionTestCase):
    """Test for Django database migrations."""

    # Make data from migrations available in the test cases
    serialized_rollback = True

    # These must be defined by subclasses.
    migrate_from = None
    migrate_to = None

    def setUp(self):
        """Set up the database up to the state of the first migration."""
        super(MigrationTestCase, self).setUp()

        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_from)

    def migrate_to_dest(self):
        """Migrate the database to the desired destination migration."""
        self.executor.loader.build_graph()
        self.executor.migrate(self.migrate_to)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(".hiccup-tests"))
class DropDuplicatesMigrationTestCase(MigrationTestCase):
    """Test the migration for dropping duplicate heartbeats and crashreports."""

    migrate_from = [("crashreports", "0005_add_fp_staff_group")]
    migrate_to = [
        ("crashreports", "0006_add_unique_constraints_and_drop_duplicates")
    ]

    def test_duplicate_heartbeats_are_deleted(self):
        """Test that duplicate heartbeats are deleted after migrating."""
        self._assert_duplicates_are_deleted(HeartBeat)

    def test_duplicate_crashreports_are_deleted(self):
        """Test that duplicate crashreports are deleted after migrating."""
        self._assert_duplicates_are_deleted(Crashreport)

    def _assert_duplicates_are_deleted(self, object_type):
        # Create a user, device and two duplicate reports
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user)
        report_1 = Dummy.create_dummy_report(object_type, device)
        Dummy.create_dummy_report(object_type, device)

        # Assert that 2 instances have been created
        self.assertEqual(object_type.objects.count(), 2)

        # Run the migration
        logger = logging.getLogger("crashreports")
        with self.assertLogs(logger, "DEBUG") as logging_watcher:
            self.migrate_to_dest()

        # Assert the correct message is logged
        self.assertTrue(
            {
                "INFO:crashreports.migrations."
                "0006_add_unique_constraints_and_drop_duplicates:"
                "Found 1 {} instances that have duplicates. "
                "These will be removed.".format(object_type.__name__),
                "DEBUG:crashreports.migrations"
                ".0006_add_unique_constraints_and_drop_duplicates:Removing "
                "duplicates: {}".format(
                    str(
                        {
                            "device": device.id,
                            "date": report_1.date,
                            "min_id": report_1.id,
                            "num_duplicates": 2,
                        }
                    )
                ),
            }.issubset(set(logging_watcher.output))
        )

        # Assert that only one instance is left in the database
        self.assertEqual(object_type.objects.count(), 1)

    def test_delete_duplicate_crashreport_with_logfile(self):
        """Test deletion of a duplicate crashreport with logfile."""
        # Create a user, device and two duplicate reports with logfiles
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user)
        crashreport_1 = Dummy.create_dummy_report(Crashreport, device)
        crashreport_2 = Dummy.create_dummy_report(Crashreport, device)
        _, logfile_1_path = Dummy.create_dummy_log_file_with_actual_file(
            crashreport_1
        )
        _, logfile_2_path = Dummy.create_dummy_log_file_with_actual_file(
            crashreport_2, logfile=Dummy.DEFAULT_DUMMY_LOG_FILE_PATHS[1]
        )

        # Assert that 2 crashreports and logfiles have been created
        self.assertEqual(Crashreport.objects.count(), 2)
        self.assertEqual(LogFile.objects.count(), 2)
        self.assertTrue(os.path.isfile(logfile_1_path))
        self.assertTrue(os.path.isfile(logfile_2_path))

        # Run the migration
        self.migrate_to_dest()

        # Assert that only one crashreport and one logfile is left in the
        # database
        self.assertEqual(Crashreport.objects.count(), 1)
        self.assertEqual(Crashreport.objects.first().logfiles.count(), 1)
        self.assertEqual(LogFile.objects.count(), 1)

        # Assert that the correct log file has been deleted
        self.assertTrue(os.path.isfile(logfile_1_path))
        self.assertFalse(os.path.isfile(logfile_2_path))

    def test_change_of_date_field_type(self):
        """Test that the 'date' field of heartbeats is changed to a date."""
        # Create a user, device and a heartbeat
        user = Dummy.create_dummy_user()
        device = Dummy.create_dummy_device(user)
        heartbeat_timestamp = datetime(2015, 12, 15, 1, 23, 45, tzinfo=pytz.utc)

        heartbeat = Dummy.create_dummy_report(
            HeartBeat, device, date=heartbeat_timestamp
        )

        # Assert that the date is of type datetime
        self.assertIsInstance(heartbeat.date, datetime)

        # Run the migration
        self.migrate_to_dest()

        # Assert that the date is now of type date and has the correct value
        heartbeat = HeartBeat.objects.first()
        self.assertIsInstance(heartbeat.date, date)
        self.assertEqual(heartbeat.date, heartbeat_timestamp.date())
