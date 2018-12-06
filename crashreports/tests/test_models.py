"""Tests for the crashreports models."""
import logging

from django.forms import model_to_dict
from django.test import TestCase

from crashreports.models import HeartBeat, Crashreport
from crashreports.tests.utils import Dummy


class DuplicatesTestCase(TestCase):
    """Test cases for the uniqueness for model instances."""

    def test_creation_of_duplicate_heartbeats(self):
        """Test creation of duplicate heartbeats."""
        self._assert_duplicate_entries_can_not_be_created(HeartBeat)

    def test_creation_of_duplicate_crashreports(self):
        """Test creation of duplicate crashreports."""
        self._assert_duplicate_entries_can_not_be_created(Crashreport)

    def _assert_duplicate_entries_can_not_be_created(self, object_type):
        # Create a user, device and a report
        user = Dummy.create_user()
        device = Dummy.create_device(user)
        Dummy.create_report(object_type, device)

        # Assert creating a duplicate report fails
        logger = logging.getLogger("crashreports")
        with self.assertLogs(logger, "DEBUG") as logging_watcher:
            report = Dummy.create_report(object_type, device)
        self.assertEqual(
            logging_watcher.output,
            [
                "DEBUG:crashreports.models:"
                "Duplicate {} received and dropped: {}".format(
                    object_type.__name__, str(model_to_dict(report))
                )
            ],
        )

        self.assertEqual(object_type.objects.count(), 1)
