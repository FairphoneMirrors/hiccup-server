# -*- coding: utf-8 -*-
"""Models for devices, heartbeats, crashreports and log files."""
import logging
import os
import uuid

from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.forms import model_to_dict
from taggit.managers import TaggableManager

LOGGER = logging.getLogger(__name__)


class Device(models.Model):
    """A device representing a phone that has been registered on Hiccup."""

    def __str__(self):
        """Return the UUID as string representation of a device."""
        return self.uuid

    # for every device there is a django user
    uuid = models.CharField(
        db_index=True,
        max_length=64,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        related_name="Hiccup_Device",
        on_delete=models.CASCADE,
        unique=True,
    )
    imei = models.CharField(max_length=32, null=True, blank=True)
    board_date = models.DateTimeField(null=True, blank=True)
    chipset = models.CharField(max_length=200, null=True, blank=True)
    tags = TaggableManager(blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=200, null=True, blank=True)
    next_per_crashreport_key = models.PositiveIntegerField(default=1)
    next_per_heartbeat_key = models.PositiveIntegerField(default=1)

    @transaction.atomic
    def get_crashreport_key(self):
        """Get the next key for a crashreport and update the ID-counter."""
        ret = self.next_per_crashreport_key
        self.next_per_crashreport_key = self.next_per_crashreport_key + 1
        self.save()
        return ret

    @transaction.atomic
    def get_heartbeat_key(self):
        """Get the next key for a heartbeat and update the ID-counter."""
        ret = self.next_per_heartbeat_key
        self.next_per_heartbeat_key = self.next_per_heartbeat_key + 1
        self.save()
        return ret


def crashreport_file_name(instance, filename):
    """Generate the full path for new uploaded log files.

    The path is created by splitting up the device UUID into 3 parts: The
    first 2 characters, the second 2 characters and the rest. This way the
    number of directories in each subdirectory does not get too big.

    Args:
        instance: The log file instance.
        filename: The name of the actual log file.

    Returns: The generated path including the file name.

    """
    return os.path.join(
        str(instance.crashreport.device.uuid)[0:2],
        str(instance.crashreport.device.uuid)[2:4],
        str(instance.crashreport.device.uuid)[4:],
        str(instance.crashreport.id),
        filename,
    )


class Crashreport(models.Model):
    """A crashreport that was sent by a device."""

    BOOT_REASON_UNKOWN = "UNKNOWN"
    BOOT_REASON_KEYBOARD_POWER_ON = "keyboard power on"
    BOOT_REASON_RTC_ALARM = "RTC alarm"
    CRASH_BOOT_REASONS = [BOOT_REASON_UNKOWN, BOOT_REASON_KEYBOARD_POWER_ON]
    SMPL_BOOT_REASONS = [BOOT_REASON_RTC_ALARM]

    device = models.ForeignKey(
        Device,
        db_index=True,
        related_name="crashreports",
        on_delete=models.CASCADE,
    )
    is_fake_report = models.BooleanField(default=False)
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField(db_index=True, max_length=200)
    radio_version = models.CharField(db_index=True, max_length=200, null=True)
    boot_reason = models.CharField(db_index=True, max_length=200)
    power_on_reason = models.CharField(db_index=True, max_length=200)
    power_off_reason = models.CharField(db_index=True, max_length=200)
    date = models.DateTimeField(db_index=True)
    tags = TaggableManager(blank=True)
    device_local_id = models.PositiveIntegerField(blank=True)
    next_logfile_key = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa: D106
        unique_together = ("device", "date")

    @transaction.atomic
    def get_logfile_key(self):
        """Get the next key for a log file and update the ID-counter."""
        ret = self.next_logfile_key
        self.next_logfile_key = self.next_logfile_key + 1
        self.save()
        return ret

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """Save the crashreport and set its local ID if it was not set."""
        try:
            with transaction.atomic():
                if not self.device_local_id:
                    self.device_local_id = self.device.get_crashreport_key()
                super(Crashreport, self).save(
                    force_insert, force_update, using, update_fields
                )
        except IntegrityError:
            # If there is a duplicate entry, log its values and return
            # without throwing an exception to keep idempotency of the
            # interface.
            LOGGER.debug(
                "Duplicate Crashreport received and dropped: %s",
                model_to_dict(self),
            )

    def _get_uuid(self):
        """Return the device UUID."""
        return self.device.uuid

    uuid = property(_get_uuid)


class LogFile(models.Model):
    """A log file that was sent along with a crashreport."""

    logfile_type = models.TextField(max_length=36, default="last_kmsg")
    crashreport = models.ForeignKey(
        Crashreport, related_name="logfiles", on_delete=models.CASCADE
    )
    logfile = models.FileField(upload_to=crashreport_file_name, max_length=500)
    crashreport_local_id = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """Save the log file and set its local ID if it was not set."""
        if not self.crashreport_local_id:
            self.crashreport_local_id = self.crashreport.get_logfile_key()
        super(LogFile, self).save(
            force_insert, force_update, using, update_fields
        )


@receiver(models.signals.post_delete, sender=LogFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete the file from the filesystem on deletion of the db instance."""
    # pylint: disable=unused-argument

    if instance.logfile:
        if os.path.isfile(instance.logfile.path):
            instance.logfile.delete(save=False)


class HeartBeat(models.Model):
    """A heartbeat that was sent by a device."""

    device = models.ForeignKey(
        Device,
        db_index=True,
        related_name="heartbeats",
        on_delete=models.CASCADE,
    )
    app_version = models.IntegerField()
    uptime = models.CharField(max_length=200)
    build_fingerprint = models.CharField(db_index=True, max_length=200)
    radio_version = models.CharField(db_index=True, max_length=200, null=True)
    date = models.DateField(db_index=True)
    device_local_id = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa: D106
        unique_together = ("device", "date")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """Save the heartbeat and set its local ID if it was not set."""
        try:
            with transaction.atomic():
                if not self.device_local_id:
                    self.device_local_id = self.device.get_heartbeat_key()
                super(HeartBeat, self).save(
                    force_insert, force_update, using, update_fields
                )
        except IntegrityError:
            # If there is a duplicate entry, log its values and return
            # without throwing an exception to keep idempotency of the
            # interface.
            LOGGER.debug(
                "Duplicate HeartBeat received and dropped: %s",
                model_to_dict(self),
            )

    def _get_uuid(self):
        """Return the device UUID."""
        return self.device.uuid

    uuid = property(_get_uuid)
