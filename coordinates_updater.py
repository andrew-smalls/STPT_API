from database_config import getDatabase
import json

def clean_data(someString):
	if "." in someString:
		someString = someString.replace(".", "")
	return someString

def get_file_contents(filename):
	fileBuses = open(filename, 'r')
	data = json.loads(fileBuses.read())
	fileBuses.close()
	return data

def coordinates_updater():
	db = getDatabase()
	data = get_file_contents("bus_stations_timisoara.json")

	station_names = dict()
	count = 0
	for piece_of_data in data:
		#if count == 3:
		#	break

		stationData = data[piece_of_data] #data[0], data[1]...
		stationDetailsDict = stationData["station_details"]
		stationCoords = stationDetailsDict["stationCoordinates"]
		stationName = stationDetailsDict["stationName"]
		stationName = clean_data(stationName)
		if stationName in station_names:
			stationDuplicateCounter = station_names[stationName]
			station_names[stationName] = stationDuplicateCounter + 1 
			stationNameForFirebase = stationName + "_" + str(stationDuplicateCounter)
		else:
			station_names[stationName] = 0
			stationNameForFirebase = stationName	
		
		print(stationName)
		#print(stationCoords)
			
		
		db.child("coordinates").child(stationNameForFirebase).child("station_data").set(stationData) #overwrites the data at the last child
		count = count + 1

coordinates_updater() #for now, it updates only the stations related to buses and trolleys