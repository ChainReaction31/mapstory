# OSH_INTEG

from django.conf.urls import patterns, url

from views import *

app_name = 'opensensorhub'

urlpatterns = patterns('.views',
                       url(r'^getCapabilities$', getCapabilities, name='getCapabilities'),
                       url(r'^layers/create$', createSensorLayer, name='createSensorLayer'),
                       )

