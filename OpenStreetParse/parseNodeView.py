from bs4 import BeautifulSoup
import requests
import re
import unidecode
#connect to https://www.openstreetmap.org/node/{nodeId}
#get <ul class="list-unstyled"> that contains all transports that go through there


def cleanStringFetched(someString):
	#print("Old string: ", someString)
	someString = someString.strip()
	someString = someString.replace(")", "")
	someString = unidecode.unidecode(someString)
	#print("New string: ", someString)
	return someString

def fetch_details_from_transport(transport):
	routeName = ""
	startStation = ""
	endStation = ""
	routeId = ""
	try:
		split_string = transport.split(":")
		routeName = split_string[0]
		routeName = routeName.replace("Relation ", "")

		split_string = split_string[1].split("=>")
		startStation = split_string[0]
		endStation = split_string[1]
		endStation = endStation.split("(")
		routeId = endStation[1]

		endStation = endStation[0]

		routeName = cleanStringFetched(routeName)
		routeId = cleanStringFetched(routeId)
		startStation = cleanStringFetched(startStation)
		endStation = cleanStringFetched(endStation)

		transportElements = [routeName, routeId, startStation, endStation] #store all  4 elements that make up the relation in a list
	except Exception:
		transportElements = []

	return transportElements #return the list, having the name of the route as first element

def fetch_transports(soup):
	transport_dict = dict()
	relations = soup.find('ul', {"class" : "list-unstyled"})
	transports_around_node = list()
	if not relations:
		return transport_dict
	for relation in relations:
		try:
			transports_around_node.append(relation.text) #guard against illegal types that do not have the .text attribute
		except AttributeError:
			pass

	for transport in transports_around_node: 
		transportDetails = fetch_details_from_transport(transport) 
		if not transportDetails:
			print("Better to print than to null crash")
			continue
		transport_dict[transportDetails[0]] = transportDetails

	#print("Fetched ", len(transport_dict), " transports")
	return transport_dict



def parse_route(nodeId, routeType):	
	BASE = "https://www.openstreetmap.org/node/"
	FULL_URL = BASE + str(nodeId)
	#print("Accessing... ", FULL_URL)
	html_text = requests.get(FULL_URL).text 
	soup = BeautifulSoup(html_text, "lxml") #make a new bs object and specify the parser (lxml in our case)

	newDict = dict() #nodeId : {routeName : {}}
	final_dict = dict()
	
	transports = fetch_transports(soup)
	if not transports:
		return final_dict

	for trans in transports:  #for each transport in the dictionary, having key routeName, get all values
		#print("At transport, inside parse route: ", transports[trans])

		tempDict = dict()
		elements = transports[trans] #get elements of the map based on this id
		tempDict['routeName'] = trans
		tempDict['routeType'] = routeType
		tempDict['routeId'] = elements[1]
		tempDict['routeStart'] = elements[2]
		tempDict['routeEnd'] = elements[3]
		newDict[trans] = tempDict

	
	final_dict[nodeId] = newDict #of the form {nodeId : {transport}}, where transport = {routeName : {routeDetails}}
	return final_dict

