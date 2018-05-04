# OSH_INTEG

import json
import urllib2
import xml.etree.ElementTree as ET
import dateutil.parser

from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError

from models import Hub
from models import Observation
from models import OSHLayer


# Builds a sensor layer with the data contained in the request
def createSensorLayer(request):

    if request.method == 'POST':
        errors = False
        errorMessages = []

	requestData = json.loads(request.body)

#layer = {
#	sensors: [],
#       hub: {
#           url,
#       }
#	configuration_options: {
#	    editable: true,
#	},
#}

    containingLayer = ''
    offeringHub = ''
    observations = []
    
    try:
        # Instantiate Hub Model
        containingLayer = OSHLayer(name=requestData["layer"]["configuration_options"]["name"])
    
    except KeyError:
        # Error has occurred in reading request, send default response
        errors=True
        errorMessages.append("Malformed Request: Layer name missing")
        
    try:
        # Instantiate Hub Model
        offeringHub = Hub(url=requestData["layer"]["hub"]["url"])
    
    except KeyError:
        # Error has occurred in reading request, send default response
        errors=True
        errorMessages.append("Malformed Request: Hub URL Missing")

	try:
		sensorCollection = requestData["layer"]["sensors"]

        # Instantiate Observation Model(s)
        for sensor in sensorCollection:
            observation = Observation(hub=offeringHub, layer=containingLayer, endpoint=sensor["endPointUrl"],
                offering=sensor["offeringId"], observedProperty=sensor["observedProperty"],
                startTime=sensor["startTime"], endTime=sensor["endTime"],
                syncMasterTime=sensor["syncMasterTime"], name=sensor["name"],
                sourceType=sensor["sourceType"])
                                          
            observations.append(observation)

	except KeyError:
		# Error has occurred in reading request, send default response
		errors=True
		errorMessages.append("Malformed Request: Sensor observation data is incomplete or incorrect")

    if errors:
        return HttpResponse(json.dumps({'status': 'failure', 'errors': error_messages}), status=400,
                                    content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 'success', 'layer': containingLayer.name}), status=201,
                                    content_type='application/json')


# Processes request to retrieve capabilities from a Hub
def getCapabilities(request):

	getCapabilities = "/sos?service=SOS&version=2.0&request=GetCapabilities"

	response = "Malformed Request: Expecting URL of Open Sensor Hub - e.g. http://botts-geo.com:8181/sensorhub"
	requestData = json.loads(request.body)

	try:
		# Append "sos?service=SOS&version=2.0&request=GetCapabilities" to get capabilities from OSH hub
		hubUrl = requestData['hubAddress']
		hubUrl = hubUrl + getCapabilities

		# Get capabilities from selected hub
		capabilities = urllib2.urlopen(hubUrl).read()

		# Parse the cabalities
		response = parseCapabilities(hubUrl, capabilities)

	except KeyError:
		# Error has occurred in reading request, send default response
		HttpResponseServerError(response)

	# Send 
	return HttpResponse(response)

# Parses the capabilities XML document provided by a Hub
def parseCapabilities(serverUrl, capabilitiesXml):

	capabilities = {'serverUrl': serverUrl, 'offerings':[]}

	root = ET.fromstring(capabilitiesXml)

	# Namespace dictionary to help make iterating over elements less verbose below
	ns = { 'swes': 'http://www.opengis.net/swes/2.0',
	       'sos' : 'http://www.opengis.net/sos/2.0',
	       'gml' : 'http://www.opengis.net/gml/3.2' }

	# Retrieve the list of offerings
	offering_list = root.findall('*//sos:ObservationOffering', ns)

	# Iterate through each offering in the list
	for offering in offering_list:
		name = offering.find('swes:name', ns)
		procedure_id = offering.find('swes:procedure', ns)
		offering_id = offering.find('swes:identifier', ns)
		desc = offering.find('swes:description', ns)

		# get all the info we need for the offering (name, desc, time range, etc.)
		offeringInfo = {}

		# Parse the begin time fields
		for begin_time in offering.iterfind('*//gml:beginPosition', ns):
			if begin_time.text is None:
				offeringInfo['start_time'] = 'now'
				offeringInfo['user_start_time'] = datetime.now()
			else:
				offeringInfo['start_time'] = begin_time.text.replace('T', ' ').replace('Z', '')
				offeringInfo['user_start_time'] = dateutil.parser.parse(begin_time.text)

		# Parse the end time fields
		for end_time in offering.iterfind('*//gml:endPosition', ns):
			if end_time.text is None:
				offeringInfo['end_time'] = 'now'
				offeringInfo['user_end_time'] = datetime.now()
			else:
				offeringInfo['end_time'] = end_time.text.replace('T', ' ').replace('Z', '')
				offeringInfo['user_end_time'] = dateutil.parser.parse(end_time.text)

		# Store the offering information
		offeringInfo['name'] = name.text
		offeringInfo['procedure_id'] = procedure_id.text
		offeringInfo['offering_id'] = offering_id.text
		offeringInfo['description'] = desc.text
		offeringInfo['observable_props'] = []
		#offeringInfo['selected_observable_props'] = ""
		#offeringInfo['config_name'] = ""
		offeringInfo['temp_enabled'] = False

		# Place each observable property into the offering
		for observable_property in offering.findall('swes:observableProperty', ns):
			offeringInfo['observable_props'].append(observable_property.text)

		# Add the offering into the list of offerings
		capabilities['offerings'].append(offeringInfo)
	
	# Return a JSON structure representation of the dictionary, default=str is a brute force approach to serailize
	# all elements as strings to avoid JSON serialization problems for objects in the structure
	return json.dumps(capabilities, indent=4, sort_keys=True, default=str)

