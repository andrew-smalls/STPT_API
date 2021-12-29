from updater import *

#allTramRoutes = db.child("transports").child("tram").child("route").get()
#print(allTramRoutes.val())
#for route in allTramRoutes.val():
	#route_id = db.child("transports").child("tram").child("route").child(route).get()
	#print(route_id.val())


routeName = "33b"
updateTimesForRoute(routeName)

