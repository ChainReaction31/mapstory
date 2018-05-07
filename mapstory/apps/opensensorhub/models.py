# OSH_INTEG

from django.db import models
from django.core import validators

#------------------------------------------------------------------------------
# Styler
#
# Model representing an OSH Styler
#------------------------------------------------------------------------------
class Styler(models.Model):
	
	id = models.AutoField(primary_key=True)

#------------------------------------------------------------------------------
# View
#
# Model representing an OSH View
#------------------------------------------------------------------------------
class View(models.Model):
	
	id = models.AutoField(primary_key=True)
	styler = models.ForeignKey(
	        Styler,
	        models.SET_NULL,
	        blank=True,
	        null=True
	    )

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
# Observation
#
# Model representation for OSH Observations
#------------------------------------------------------------------------------
class Observation(models.Model):

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

	SERVICE_CHOICES=(
			('0', 'SOS'),
			('1', 'SPS'),			
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
	service = models.CharField(max_length=1, choices=SERVICE_CHOICES, default='0')
	protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE_CHOICES, default='2')

