# OSH_INTEG

from fields import RgbField
from fields import ThresholdArrayField
from fields import IntThresholdField

from django.db import models
from django.core import validators

COLOR_MODE_CHOICES = (
    ('0', 'FIXED'),
    ('1', 'THRESHOLD'),
    ('2', 'COLORMAP'),
)


# ------------------------------------------------------------------------------
# View
#
# Model representing an OSH View
# ------------------------------------------------------------------------------
class View(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    sensor_archetype = models.CharField(max_length=200)


# ------------------------------------------------------------------------------
# Styler
#
# Model representing an OSH Styler
# ------------------------------------------------------------------------------
class Styler(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    timeout = models.IntegerField()
    styler_type = models.CharField(max_length=200)
    view = models.ForeignKey(
        View,
        models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


# ------------------------------------------------------------------------------
# TextStyler
#
# Model representing an OSH Text Styler
# ------------------------------------------------------------------------------
class TextStyler(Styler):
    location = models.CharField(max_length=200)
    color_mode = models.CharField(max_length=1, choices=COLOR_MODE_CHOICES, default='0')
    color_rgb = RgbField()
    thresholds = ThresholdArrayField(IntThresholdField())


# ------------------------------------------------------------------------------
# LocationIndicator
#
# Model representing an OSH Location Indicator Styler
# ------------------------------------------------------------------------------
class LocationIndicator(Styler):
    data_source_lat = models.CharField(max_length=200)
    data_source_lon = models.CharField(max_length=200)
    data_source_alt = models.CharField(max_length=200)
    view_icon = models.URLField(max_length=200)
    render_mode = models.CharField(max_length=200)


# ------------------------------------------------------------------------------
# ChartStyler
#
# Model representing an OSH Location Chart Styler
# ------------------------------------------------------------------------------
class ChartStyler(Styler):
    RANGE_MODE_CHOICES = (
        ('0', 'ALL_FIXED'),
        ('1', 'X_DYNAMIC'),
        ('2', 'Y_DYNAMIC'),
        ('3', 'ALL_DYNAMIC')
    )

    data_source_x = models.CharField(max_length=200)
    data_source_y = models.CharField(max_length=200)
    label_x = models.CharField(max_length=200)
    label_y = models.CharField(max_length=200)
    color_mode = models.CharField(max_length=1, choices=COLOR_MODE_CHOICES, default='0')
    color_rgb = RgbField()
    range_mode = models.CharField(max_length=1, choices=RANGE_MODE_CHOICES, default='0')
    range_x = models.FloatField()
    range_y = models.FloatField()
    max_points = models.IntegerField()
    thresholds = ThresholdArrayField(IntThresholdField())


# ------------------------------------------------------------------------------
# VideoView
#
# Model representing an OSH Location Video View Styler
# ------------------------------------------------------------------------------
class VideoView(Styler):
    draggable = models.BooleanField(default=False)
    show = models.BooleanField(default=False)
    dockable = models.BooleanField(default=False)
    closeable = models.BooleanField(default=False)
    keepRatio = models.BooleanField(default=False)


# ------------------------------------------------------------------------------
# OSHLayer
#
# Model representing an OSH Layer
# ------------------------------------------------------------------------------
class OSHLayer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


# ------------------------------------------------------------------------------
# Hub
#
# Model representation for an OpenSensorHub Instance
# ------------------------------------------------------------------------------
class Hub(models.Model):
    PROTOCOL_TYPE_CHOICES = (
        ('0', 'HTTP'),
        ('1', 'HTTPS'),
        ('2', 'WS'),
        ('3', 'WSS'),
    )

    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200)
    protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE_CHOICES, default='2')


# ------------------------------------------------------------------------------
# SweService
#
# Model representation for Sensor Web Enablement Service
# ------------------------------------------------------------------------------
class SweService(models.Model):
    SOS = 0,
    SPS = 1

    class Meta:
        abstract = True


# ------------------------------------------------------------------------------
# Observation
#
# Model representation for OSH Observations
# ------------------------------------------------------------------------------
class Observation(SweService):
    PROTOCOL_TYPE_CHOICES = (
        ('0', 'HTTP'),
        ('1', 'HTTPS'),
        ('2', 'WS'),
        ('3', 'WSS'),
    )

    REPLAY_SPEED_CHOICES = (
        ('0', 'QUARTER'),
        ('1', 'HALF'),
        ('2', 'NORMAL'),
        ('3', 'DOUBLE'),
        ('4', 'QUAD'),
    )

    id = models.AutoField(primary_key=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    layer = models.ForeignKey(OSHLayer)
    view = models.ForeignKey(
        View,
        models.SET_NULL,
        blank=True,
        null=True
    )

    endpoint = models.URLField(max_length=200)
    offering = models.CharField(max_length=200)
    observed_property = models.URLField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sync_master_time = models.BooleanField(default=False)
    buffering_time = models.IntegerField(validators=[validators.MinValueValidator(0)])
    time_shift = models.IntegerField()
    source_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    replay_speed = models.CharField(max_length=1, choices=REPLAY_SPEED_CHOICES, default='2')
    service = models.IntegerField(default=SweService.SOS, validators=[validators.MinValueValidator(SweService.SOS),
                                                                      validators.MaxValueValidator(SweService.SOS)])
    protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE_CHOICES, default='2')
