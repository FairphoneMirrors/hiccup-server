"""The stats models."""
from django.db import models


class _VersionStats(models.Model):
    """The base class for all-time stats of a version.

    Sub-classes should be created to gather stats about a versioned
    end-product such as a software build.

    Attributes:
        is_official_release (models.BooleanField): If this version is an
            official release. Defaults to False.
        is_beta_release (models.BooleanField): If this version is a beta
            release. Defaults to False.
        first_seen_on (models.DateField): Day this version has been seen for
            the first time as reported by devices (not by the server). Defaults
            to the current date.
        released_on (models.DateField): Day this version has been released on.
            Defaults to the current date.
        heartbeats (models.IntegerField): The total heartbeats counted for this
            version.
        prob_crashes (models.IntegerField): The total probable crash reports
            counted for this version.
        smpl (models.IntegerField): The total SMPL reports counted for this
            version.
        other (models.IntegerField): The total of other reports counted for
            this version.

    """

    is_official_release = models.BooleanField(default=False)
    is_beta_release = models.BooleanField(default=False)
    first_seen_on = models.DateField()
    released_on = models.DateField()
    heartbeats = models.IntegerField(default=0)
    prob_crashes = models.IntegerField(default=0)
    smpl = models.IntegerField(default=0)
    other = models.IntegerField(default=0)

    class Meta:
        abstract = True


class _DailyVersionStats(models.Model):
    """The base class for daily stats of a version.

    Sub-classes MUST define the foreign key `version` pointing back to the
    `_VersionStats` implementation they are gathering stats for.

    Attributes:
        date (models.DateField): Day considered for the stats.
        heartbeats (models.IntegerField): The total heartbeats counted for this
            version on the day `date`.
        prob_crashes (models.IntegerField): The total probable crash reports
            counted for this version on the day `date`.
        smpl (models.IntegerField): The total SMPL reports counted for this
            version on the day `date`.
        other (models.IntegerField): The total of other reports counted for
            this version on the day `date`.

    """

    date = models.DateField()
    heartbeats = models.IntegerField(default=0)
    prob_crashes = models.IntegerField(default=0)
    smpl = models.IntegerField(default=0)
    other = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Version(_VersionStats):
    """The all-time stats of a software version.

    Attributes:
        build_fingerprint (models.CharField): The software build fingerprint
            uniquely identifying this version.

    """

    build_fingerprint = models.CharField(max_length=200, unique=True)

    def __str__(self):  # noqa: D105
        return self.build_fingerprint


class VersionDaily(_DailyVersionStats):
    """The daily stats of a software version.

    Attributes:
        version (models.ForeignKey): The software version object (`Version`)
            these daily stats are about.

    """

    version = models.ForeignKey(
        Version, db_index=True, related_name='daily_stats',
        on_delete=models.CASCADE)


class RadioVersion(_VersionStats):
    """The all-time stats of a radio version.

    Attributes:
        radio_version (models.CharField): The radio version number uniquely
            identifying this version.

    """

    radio_version = models.CharField(max_length=200, unique=True)

    def __str__(self):  # noqa: D105
        return self.radio_version


class RadioVersionDaily(_DailyVersionStats):
    """The daily stats of a radio version.

    Attributes:
        version (models.ForeignKey): The radio version object (`RadioVersion`)
            these daily stats are about.

    """

    version = models.ForeignKey(
        RadioVersion, db_index=True, related_name='daily_stats',
        on_delete=models.CASCADE)


class StatsMetadata(models.Model):
    """The stats metadata.

    Attributes:
        updated_at (models.DateTimeField): The last time the stats were
            updated.

    """

    updated_at = models.DateTimeField()
