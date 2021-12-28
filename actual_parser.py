from bs4 import BeautifulSoup
import requests

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

url = "http://86.125.113.218:61978/html/timpi/trasee.php"
example_route_33_param = "param1=1046"
full_url = url + "?" + example_route_33_param
print(full_url)


html_text = requests.get(full_url).text #do not forget to specify .text, otherwise you will only get the responde code 
soup = BeautifulSoup(html_text, "lxml") #make a new bs object and specify the parser (lxml in our case)




def better_fetch():
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
			if len(stations) > 1 or len(times) > 1:	#they missed an </table> inside their html, so we have to do this instead
				continue
			for station in stations:
				stations_for_this_route.append(station.text)
			for time in times:
				timestamps_for_this_route.append(time.text)
			valid_entries = valid_entries + 1

	cleanTimestamps = cleanTimeFormat(timestamps_for_this_route)		#data arrives with some unwanted strings, clean first
	timestamps_for_this_route = cleanAgain(cleanTimestamps)
	number_of_stations_first_direction = number_of_stations_both_ways[1] - 1 #need to decrement to show correct value

	return [destinations_for_this_route, stations_for_this_route, timestamps_for_this_route, number_of_stations_first_direction]


def build_dictionary(destinations, stations, timestamps, number_of_stations_first_direction):
	dictionary = dict()

	nr_stations =  number_of_stations_first_direction
	first_direction_stations = stations[0 : nr_stations]
	second_direction_stations = stations[nr_stations:]
	first_direction_timestamps = timestamps[0 : nr_stations]
	second_direction_timestamps = timestamps[nr_stations:]

	first_direction = dict(zip(first_direction_stations, first_direction_timestamps))
	second_direction = dict(zip(second_direction_stations, second_direction_timestamps))

	dict_list = [first_direction, second_direction]
	i = 0
	for dest in destinations:
		key = dest
		value = dict_list[0]
		i = i + 1
		dictionary[key] = value

	return dictionary

#Use methods built here:
destinations, stations, timestamps, number_of_stations_first_direction = better_fetch()
both_directions = build_dictionary(destinations, stations, timestamps, number_of_stations_first_direction)
print("Both directions as dict: ")
print(both_directions.keys())
print(both_directions.values())