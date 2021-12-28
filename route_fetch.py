import pyrebase

config = {	
  "apiKey": "AIzaSyA6pPg3YslzTehYge58ajEQxpmQ8fmbiJc",
  "authDomain": "publictransportapp-fea50.firebaseapp.com",
  "databaseURL": "https://publictransportapp-fea50-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "publictransportapp-fea50",
  "storageBucket": "publictransportapp-fea50.appspot.com",
  "messagingSenderId": "145206856336"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()  


url = "http://86.125.113.218:61978/html/timpi/trasee.php"
example_route_33_param = "param1=1046"

full_url = url + "?" + example_route_33_param

print(full_url)

allTramRoutes = db.child("transports").child("tram").child("route").get()
print(allTramRoutes.val())
for route in allTramRoutes.val():
	route_id = db.child("transports").child("tram").child("route").child(route).get()
	print(route_id.val())