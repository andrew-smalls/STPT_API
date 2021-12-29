#import pyrebase
from actual_parser import *
from database_config import *
from data_initializer import initializeData

db = getDatabase()    #get reference of our firebase realtime database
initializeData(db)    #will setup all the corresponding params that need to be passed to the parser in order to fetch the stations, destinations etc

allTramRoutes = db.child("transports").child("tram").child("route").get()
print(allTramRoutes.val())
for route in allTramRoutes.val():
	route_id = db.child("transports").child("tram").child("route").child(route).get()
	print(route_id.val())

#parse_route(1046)

def getAllRoutesInformation():
  trams = db.child("transports").child("tram").child("route").get().val()
  buses = db.child("transports").child("bus").child("route").get().val()
  trolleys = db.child("transports").child("trolley").child("route").get().val()

  allRoutes = dict()
  allRoutes["trams"] = trams
  allRoutes["buses"] = buses
  allRoutes["trolleys"] = trolleys

  return allRoutes

def getAllRoutesNames(allRoutes):
  names = dict()
  for key in allRoutes.keys():
    print("Routes for key: ", key)
    print(allRoutes[key])
    print("All keys for this kind of transport: ")
    key_dict = key
    values = allRoutes[key].keys() 
    names[key_dict] = values
    print("\n")

  return names

def updateRoute(routeName): #ex: 33B / 1 / E8
  print("Need to fetch route ", routeName)

updateRoute("33b")
allRoutes = getAllRoutesInformation()

names = getAllRoutesNames(allRoutes)


#print("All routes values: ", allRoutes.values())