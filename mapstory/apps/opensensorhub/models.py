# OSH_INTEG

import fields

from django.db import models
from django.core import validators

COLOR_MODE_CHOICES = (
		('0', 'FIXED'),
		('1', 'THRESHOLD'),
		('2', 'COLORMAP'),		
	)

#------------------------------------------------------------------------------
# Styler
#
# Model representing an OSH Styler
#------------------------------------------------------------------------------
class Styler(models.Model):
	
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	timeout = models.IntegerField()
	stylerType = models.CharField(max_length=200)
	view = models.ForeignKey(
	        View,
	        models.SET_NULL,
	        blank=True,
	        null=True
	    )

	class Meta:
		abstract = True
		

#------------------------------------------------------------------------------
# TextStyler
#
# Model representing an OSH Text Styler
#------------------------------------------------------------------------------
class TextStyler(Styler):

	location = models.CharField(max_length=200)
	colorMode = models.CharField(max_length=1, choices=COLOR_MODE_CHOICES, default='0')
	colorRGB = RgbField()
	thresholds = ThresholdArrayField(IntThresholdField())

#------------------------------------------------------------------------------
# LocationIndicator
#
# Model representing an OSH Location Indicator Styler
#------------------------------------------------------------------------------
class LocationIndicator(Styler):
	
	dataSourceLat = models.CharField(max_length=200)
	dataSourceLon = models.CharField(max_length=200)
	dataSourceAlt = models.CharField(max_length=200)
	viewIcon = models.URLField(max_length=200)
	renderMode = models.CharField(max_length=200)

#------------------------------------------------------------------------------
# ChartStyler
#
# Model representing an OSH Location Chart Styler
#------------------------------------------------------------------------------
class ChartStyler(Styler):

	RANGE_MODE_CHOICES = (
			('0', 'ALL_FIXED'),
			('1', 'X_DYNAMIC'),
			('2', 'Y_DYNAMIC'),
			('3', 'ALL_DYNAMIC')	
		)

	dataSourceX = models.CharField(max_length=200)
	dataSourceY = models.CharField(max_length=200)
	labelX = models.CharField(max_length=200)
	labelY = models.CharField(max_length=200)
	colorMode = models.CharField(max_length=1, choices=COLOR_MODE_CHOICES, default='0')
	colorRGB = RgbField()
	rangeMode = models.CharField(max_length=1, choices=RANGE_MODE_CHOICES, default='0')
	rangeX = model.FloatField()
	rangeY = model.FloatField()
	maxPoints = models.IntegerField()
	thresholds = ThresholdArrayField(IntThresholdField())

#------------------------------------------------------------------------------
# VideoView
#
# Model representing an OSH Location Video View Styler
#------------------------------------------------------------------------------
class VideoView(Styler):
	
	draggable = models.BooleanField(default=False)
	show = models.BooleanField(default=False)
	dockable = models.BooleanField(default=False)
	closeable = models.BooleanField(default=False)
	keepRatio = models.BooleanField(default=False)


#------------------------------------------------------------------------------
# View
#
# Model representing an OSH View
#------------------------------------------------------------------------------
class View(models.Model):
	
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	sensorArchetype = models.CharField(max_length=200)

#------------------------------------------------------------------------------
# OSHLayer
#
# Model representing an OSH Layer
#------------------------------------------------------------------------------
class OSHLayer(models.Model):

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)

#------------------------------------------------------------------------------
# Hub
#
# Model representation for an OpenSensorHub Instance
#------------------------------------------------------------------------------
class Hub(models.Model):

	PROTOCOL_TYPE_CHOICES=(
			('0', 'HTTP'),
			('1', 'HTTPS'),
			('2', 'WS'),
			('3', 'WSS'),			
		)

	id = models.AutoField(primary_key=True)
	url = models.URLField(max_length=200)
	protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE_CHOICES, default='2')

#------------------------------------------------------------------------------
# SweService
#
# Model representation for Sensor Web Enablement Service
#------------------------------------------------------------------------------
class SweService(models.Model):

	SOS=0,
	SPS=1

	class Meta:
		abstract = True

#------------------------------------------------------------------------------
# Observation
#
# Model representation for OSH Observations
#------------------------------------------------------------------------------
class Observation(SweService):

	PROTOCOL_TYPE_CHOICES=(
			('0', 'HTTP'),
			('1', 'HTTPS'),
			('2', 'WS'),
			('3', 'WSS'),			
		)

	REPLAY_SPEED_CHOICES=(
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
	observedProperty = models.URLField(max_length=200)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	syncMasterTime = models.BooleanField(default=False)
	bufferingTime = models.IntegerField(validators=[validators.MinValueValidator(0)])
	timeShift = models.IntegerField()
	sourceType = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	replaySpeed = models.CharField(max_length=1, choices=REPLAY_SPEED_CHOICES, default='2')
	service = models.IntegerField(default=SweService.SOS, validators=[validators.MinValueValidator(SweService.SOS), validators.MaxValueValidator(SweService.SOS)])
	protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE_CHOICES, default='2')

