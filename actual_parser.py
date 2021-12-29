from bs4 import BeautifulSoup
import requests

def sanitize_data(someList):
	#print("Old list: ", someList)
	for i, element in enumerate(someList):
		if "." in element:
			element = element.replace(".", "")
			someList[i] = element
	return someList

def cleanTimeFormat(someList):
	for element in someList:
		if "Stația" in element:
			someList.remove(element)
	return someList

def cleanAgain(someList): #for whatever reason, it needs double cleaning 
	for val in someList:
		if "Sosire" in val:
			 someList.remove(val)
	return someList

def printMyList(someList):
	i = 0
	for val in someList:
		print(i,".", val)
		i = i + 1
	print("\n")

def better_fetch(soup):
	destinations_for_this_route = []
	stations_for_this_route = []
	timestamps_for_this_route = []
	number_of_stations_both_ways = []
	valid_entries = 0 #used to get correct nr of stations that go in both ways

	tables = soup.find_all('table')
	for table in tables:
		if table.attrs['bgcolor'] == '0048A1':							#hardcoded color, corresponds to destination name
			destinations = table.find_all('td')
			for destination in destinations:
				destinations_for_this_route.append(destination.text)
				number_of_stations_both_ways.append(valid_entries)
			valid_entries = valid_entries + 1
		if table.attrs['bgcolor'] == 'D8D8D8':							#hardcoded color, corresponds to stations + times
			stations = table.find_all('td', attrs={'align' : 'left'}) 	#stations are alligned to the left
			times = table.find_all('td', attrs={'align' : 'center'})	#times are alligned in the center
			if len(stations) > 1 or len(times) > 1:	#they missed a </table> inside their html, so we have to do this instead
				continue
			for station in stations:
				stations_for_this_route.append(station.text)
			for time in times:
				timestamps_for_this_route.append(time.text)
			valid_entries = valid_entries + 1

	cleanTimestamps = cleanTimeFormat(timestamps_for_this_route)		#data arrives with some unwanted strings, clean first
	timestamps_for_this_route = cleanAgain(cleanTimestamps)
	number_of_stations_first_direction = number_of_stations_both_ways[1] - 1 #need to decrement to show correct value
	sanitize_data(destinations_for_this_route)
	sanitize_data(stations_for_this_route)
	sanitize_data(timestamps_for_this_route)
	return [destinations_for_this_route, stations_for_this_route, timestamps_for_this_route, number_of_stations_first_direction]

def make_iterated_dictionary(someDict):
	dictionary = dict()
	i = 0
	#print("Dictionary before: ", someDict)
	
	#dictionary = {key : value for key,value in zip(range(len(someDict)), someDict.items())}
	dictionary = dict(zip(range(len(someDict)), someDict.items()))
	#print("This new dict now: ", dictionary.items())

	return dictionary

def assign_destinations(someList, destinations):
	dictionary = dict()
	i = 0
	for dest in destinations:
		key = dest
		value = someList[i]
		i = i + 1
		dictionary[key] = value
	return dictionary

def build_dictionary(destinations, stations, timestamps, number_of_stations_first_direction):
	dictionary = dict()

	nr_stations =  number_of_stations_first_direction
	first_direction_stations = stations[0 : nr_stations]
	second_direction_stations = stations[nr_stations:]
	first_direction_timestamps = timestamps[0 : nr_stations]
	second_direction_timestamps = timestamps[nr_stations:]
	first_direction = dict(zip(first_direction_stations, first_direction_timestamps))
	second_direction = dict(zip(second_direction_stations, second_direction_timestamps))

	
	first_direction_proto = first_direction
	second_direction_proto = second_direction
	first_direction_proto = make_iterated_dictionary(first_direction_proto)
	first_direction_proto = make_iterated_dictionary(second_direction_proto)
	dict_list_proto = [first_direction_proto, second_direction_proto]
	#print("Dictionary for now: ", dict_list_proto)		
	dict_proto = assign_destinations(dict_list_proto, destinations)
	#print("Dictionary after assign destinations: ", dict_proto)

	dict_list = [first_direction, second_direction]
	i = 0
	for dest in destinations:
		key = dest
		value = dict_list[i]
		i = i + 1
		dictionary[key] = value

	#print("Dictionary as it should be: ", dictionary)
	return [dictionary, dict_proto]

def parse_route(routeParam):	#1046
	BASE = "http://86.125.113.218:61978/html/timpi/trasee.php?param1="
	FULL_URL = BASE + str(routeParam)
	#print(FULL_URL)

	html_text = requests.get(FULL_URL).text #do not forget to specify .text, otherwise you will only get the responde code 
	soup = BeautifulSoup(html_text, "lxml") #make a new bs object and specify the parser (lxml in our case)

	#Use methods built here:
	destinations, stations, timestamps, number_of_stations_first_direction = better_fetch(soup)
	both_directions, both_directions_proto = build_dictionary(destinations, stations, timestamps, number_of_stations_first_direction)

	return both_directions, both_directions_proto
