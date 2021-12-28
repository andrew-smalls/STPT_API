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


destinations_for_this_route = []
stations_for_this_route = []
timestamps_for_this_route = []

def initial_fetch():	#kinda sorta works
	tables = soup.find_all('table')#, attrs={'bgcolor': '#0048A1'})
	for table in tables:
		if table.attrs['bgcolor'] == '0048A1':		#hardcoded color, corresponds to destination name
			destinations = table.find_all('td')
			for destination in destinations:
				destinations_for_this_route.append(destination.text)
		if table.attrs['bgcolor'] == 'D8D8D8':
			stations = table.find_all('td', attrs={'align' : 'left'}) #stations are alligned to the left
			times = table.find_all('td', attrs={'align' : 'center'})	#times are alligned in the center
			for station in stations:
				stations_for_this_route.append(station.text)
			for time in times:
				timestamps_for_this_route.append(time.text) #cleanTime


def better_fetch():
	tables = soup.find_all('table')#, attrs={'bgcolor': '#0048A1'})
	for table in tables:
		if table.attrs['bgcolor'] == '0048A1':		#hardcoded color, corresponds to destination name
			destinations = table.find_all('td')
			for destination in destinations:
				destinations_for_this_route.append(destination.text)
		if table.attrs['bgcolor'] == 'D8D8D8':
			stations = table.find_all('td', attrs={'align' : 'left'}) #stations are alligned to the left
			times = table.find_all('td', attrs={'align' : 'center'})	#times are alligned in the center
			for station in stations:
				stations_for_this_route.append(station.text)
			for time in times:
				timestamps_for_this_route.append(time.text) #cleanTime


#initial_fetch()
better_fetch()


#print("Destinations fetched: ")
#printMyList(destinations_for_this_route)

print("Stations fetched: ")
printMyList(stations_for_this_route)

cleanTimestamps = cleanTimeFormat(timestamps_for_this_route)
cleansedAgain = cleanAgain(cleanTimestamps)
print("Timestamps fetched: ")
print(cleansedAgain)

if len(stations_for_this_route) == len(cleansedAgain):
	print("Length stations: ", len(stations_for_this_route))
	print("Length times: ", len(cleansedAgain))
	stations_timestamps = dict(zip(stations_for_this_route, cleansedAgain)) #{stations_for_this_route[i]:cleansedAgain[i] for i in range(len(stations_for_this_route))}
else: 
	print("Lists do not have same size")
	stations_timestamps = {}
for entry in stations_timestamps:
	print(entry)