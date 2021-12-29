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
    routeData, routeData_proto = parse_route(routeParam)
    print("Before update: ")
    for key in routeData_proto.keys():
      print("For key: ", key)
      print(routeData_proto[key].values())
    
    #routeDataPath = db.child("transports").child(routeType).child("route").child(routeName).child("data").set(routeData_proto)
    print("Updated successfully!", routeName) 
  else:
    print("Route nonexistent:", routeName)


def updateAll():
  #go through all entries in database and update each
  print("Cock and balls")