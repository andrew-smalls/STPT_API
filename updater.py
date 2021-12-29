from data_initializer import *
from database_config import *
from actual_parser import *

db = getDatabase()    #get reference of our firebase realtime database
initializeData(db)    #will setup all the corresponding params that need to be passed to the parser in order to fetch the stations, destinations etc
allRoutes = getAllRoutesInformation(db)

def getAllRoutesNames():
  routeNames = dict()
  if not allRoutes: 
    print("Couldn't get a hold of all transports")
    return routeNames    
  for key in allRoutes.keys():
    key_dict = key
    values = allRoutes[key].keys() 
    routeNames[key_dict] = values
  return routeNames

def getRouteInfo(routeName, routeNames=None): #ex: 33B / 1 / E8
  if not routeNames:
    routeNames = getAllRoutesNames()
  routeName = routeName.lower()
  result = None
  for key in routeNames.keys():
    if routeName in routeNames[key]:
      node = db.child("transports").child(key).child("route").child(routeName)
      param = node.child("param").get().val()
      transport_type = key 
      result = [transport_type, routeName, param, node]
      return result
  if not result:
    print("\nSorry, no transports with that name")  
    return None

def updateTimesForRoute(routeName):
  routeInfo = getRouteInfo(routeName)
  if routeInfo:
    routeType, routeName, routeParam, routeNode = routeInfo
    routeData = parse_route(routeParam)
    routeDataPath = db.child("transports").child(routeType).child("route").child(routeName).child("data").set(routeData)
    print("Updated successfully: ", routeName)
    return 0 
  else:
    print("Route nonexistent:", routeName)
    return -1

def updateAll():
  #go through all entries in database and update each
  routes = getAllRoutesNames()
  stop = 0
  for key in routes.keys():
    if stop:
      break
    for value in routes[key]:
      print("Updating route: ", value)
      result = updateTimesForRoute(str(value))  #just execute the above method on all routes
      if result != 0:
        stop = 1
        print("Need to stop, route faulty: ", value)
        break