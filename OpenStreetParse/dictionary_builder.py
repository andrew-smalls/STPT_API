import json
from OpenStreetParse.Station import *
from OpenStreetParse.parseNodeView import *

def build_station_dict(station):
  station_dict = dict()
  station_dict["stationName"] = cleanStringFetched(station.getName())
  station_dict["stationCoordinates"] = station.getCoordinates()

  location = station.getLocation()
  if location:
    station_dict["stationLocation"] = cleanStringFetched(location)

  routes = station.getRoutes()
  if routes:
    station_dict["stationRoutes"] = routes

  return station_dict



def JSON_to_station_list(filename):
  #data = local_file_to_JSON(filename)
  fileBuses = open(filename, 'r')
  data = json.loads(fileBuses.read())
  fileBuses.close()
  #print("data Size: ", len(data['features']))
  listOfStations = []
  for i in data['features']:
    properties = i['properties']
    geometry = i['geometry']

    nodeId = properties['@id']
    if 'name' in properties:
      name = properties['name']
    else:
      name = ""
    if 'location' in properties:
      location = properties['location']
    else:
      location = ""
    if 'route_ref' in properties:
      route_ref = properties['route_ref']
    else:
      route_ref = ""

    coordinates = geometry['coordinates']

    station = Station(nodeId, name, coordinates, location, route_ref)
    listOfStations.append(station)

  return listOfStations

def build_stations_details_traffic_dictionary(listOfStations, routeType):
  node_transports_dict = dict()

  count = 0
  for station in listOfStations:
    if station.getName():
      station_dict = build_station_dict(station)
      station_traffic = parse_route(station.getId(), routeType)
      temp_dict = dict()
      temp_dict["station_details"] = station_dict
      temp_dict["station_traffic"] = station_traffic
      node_transports_dict[count] = temp_dict

      count = count + 1

  return node_transports_dict

def saveDictionary(fileName, dictionaryToSave):
  dictionaryFile = open(fileName, "w") #save to file
  json.dump(dictionaryToSave, dictionaryFile)
  dictionaryFile.close()


def transform_json_to_station_dictionary(filenameRead, filenameWrite, transportType):
  listOfStations = JSON_to_station_list(filenameRead)
  print("Size: ", len(listOfStations))
  node_transports_dict = build_stations_details_traffic_dictionary(listOfStations, transportType)
  saveDictionary(filenameWrite, node_transports_dict)