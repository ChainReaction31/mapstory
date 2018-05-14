# OSH_INTEG

import json
import urllib2
import xml.etree.ElementTree as ElementTree
import dateutil.parser

from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError

from models import Hub
from models import Observation
from models import OSHLayer


# Builds a sensor layer with the data contained in the request
def create_sensor_layer(request):

	if request.method == 'POST':
		errors = False
		error_messages = []

		request_data = json.loads(request.body)

		containing_layer = ''
		offering_hub = ''
		observations = []

		try:
			# Instantiate Hub Model
			containing_layer = OSHLayer.objects.create(name=request_data["layer"]["configuration_options"]["name"])

		except KeyError:
			# Error has occurred in reading request, send default response
			errors=True
			error_messages.append("Malformed Request: Layer name missing")

		try:
			# Instantiate Hub Model
			offering_hub = Hub.objects.create(url=request_data["layer"]["hub"]["url"])

		except KeyError:
			# Error has occurred in reading request, send default response
			errors=True
			error_messages.append("Malformed Request: Hub URL Missing")

		try:
			sensor_collection = request_data["layer"]["sensors"]

			# Instantiate Observation Model(s)
			for sensor in sensor_collection:
				observation = Observation.objects.create(hub=offering_hub, layer=containing_layer, endpoint=sensor["endPointUrl"],
					offering=sensor["offeringId"], observedProperty=sensor["observedProperty"],
					startTime=sensor["startTime"], endTime=sensor["endTime"],
					syncMasterTime=sensor["syncMasterTime"], name=sensor["name"],
					sourceType=sensor["sourceType"])

				observations.append(observation)

		except KeyError:
			# Error has occurred in reading request, send default response
			errors=True
			error_messages.append("Malformed Request: Sensor observation data is incomplete or incorrect")

		if errors:
			return HttpResponse(json.dumps({'status': 'failure', 'errors': error_messages}), status=400,
										content_type='application/json')

		else:
			# No errors have occurred, save the created objects to the OSH Database
#			containing_layer.save(using='opensensorhub')
#			offering_hub.save(using='opensensorhub')
#			for observation in observations:
#				observation.save(using='opensensorhub')

			return HttpResponse(json.dumps({'status': 'success', 'layer': containing_layer.name}), status=201,
						content_type='application/json')


# Processes request to retrieve capabilities from a Hub
def get_capabilities(request):

	get_capabilities_req = "/sos?service=SOS&version=2.0&request=GetCapabilities"

	response = "Malformed Request: Expecting URL of Open Sensor Hub - e.g. http://botts-geo.com:8181/sensorhub"
	request_data = json.loads(request.body)

	try:
		# Append "sos?service=SOS&version=2.0&request=GetCapabilities" to get capabilities from OSH hub
		hub_url = request_data['hubAddress']
		hub_url = hub_url + get_capabilities_req

		# Get capabilities from selected hub
		capabilities = urllib2.urlopen(hub_url).read()

		# Parse the cabalities
		response = parse_capabilities(hub_url, capabilities)

	except KeyError:
		# Error has occurred in reading request, send default response
		HttpResponseServerError(response)

	# Send 
	return HttpResponse(response)

# Parses the capabilities XML document provided by a Hub
def parse_capabilities(server_url, capabilities_xml):

	capabilities = {'serverUrl': server_url, 'offerings':[]}

	root = ElementTree.fromstring(capabilities_xml)

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
		offering_info = {}

		# Parse the begin time fields
		for begin_time in offering.iterfind('*//gml:beginPosition', ns):
			if begin_time.text is None:
				offering_info['start_time'] = 'now'
				offering_info['user_start_time'] = datetime.now()
			else:
				offering_info['start_time'] = begin_time.text.replace('T', ' ').replace('Z', '')
				offering_info['user_start_time'] = dateutil.parser.parse(begin_time.text)

		# Parse the end time fields
		for end_time in offering.iterfind('*//gml:endPosition', ns):
			if end_time.text is None:
				offering_info['end_time'] = 'now'
				offering_info['user_end_time'] = datetime.now()
			else:
				offering_info['end_time'] = end_time.text.replace('T', ' ').replace('Z', '')
				offering_info['user_end_time'] = dateutil.parser.parse(end_time.text)

		# Store the offering information
		offering_info['name'] = name.text
		offering_info['procedure_id'] = procedure_id.text
		offering_info['offering_id'] = offering_id.text
		offering_info['description'] = desc.text
		offering_info['observable_props'] = []
		#offering_info['selected_observable_props'] = ""
		#offering_info['config_name'] = ""
		offering_info['temp_enabled'] = False

		# Place each observable property into the offering
		for observable_property in offering.findall('swes:observableProperty', ns):
			offering_info['observable_props'].append(observable_property.text)

		# Add the offering into the list of offerings
		capabilities['offerings'].append(offering_info)
	
	# Return a JSON structure representation of the dictionary, default=str is a brute force approach to serailize
	# all elements as strings to avoid JSON serialization problems for objects in the structure
	return json.dumps(capabilities, indent=4, sort_keys=True, default=str)

