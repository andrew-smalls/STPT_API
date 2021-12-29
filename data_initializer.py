#from database_config import *

def initializeData(db):
  initializeTrams(db)
  initializeBuses(db)
  initializeTrolleys(db)

#STPT stuff
def initializeTrams(db):
  tram_dict = {
  "1" :{"param" : "1106"},
  "2" :{"param" : "1126"},
  "4" :{"param" : "1266"},
  "6a" :{"param" : "2686"},
  "6b" :{"param" : "2706"},
  "7a" :{"param" : "1556"},
  "7b" :{"param" : "1557"},
  "8" :{"param" : "1558"},
  "9" :{"param" : "2406"}
  }

  path = db.child("transports").child("tram").child("route").set(tram_dict)

def initializeTrolleys(db):
  trolley_dict = {
  "11" :{"param" : "990"},
  "M11" :{"param" : "2786"},
  "13" :{"param" : "2826"},
  "14" :{"param" : "1006"},
  "M14" :{"param" : "2766"},
  "15" :{"param" : "989"},
  "16" :{"param" : "1206"},
  "17" :{"param" : "1086"},
  "18" :{"param" : "1166"}
  }

  path = db.child("transports").child("trolley").child("route").set(trolley_dict)

def initializeBuses(db):
  bus_dict = {
  "3" :{"param" : "1207"},
  "4B" :{"param" : "3586"},
  "5" :{"param" : "2246"},
  "21" :{"param" : "1146"},
  "28" :{"param" : "1226"},
  "32" :{"param" : "1546"},
  "33" :{"param" : "1046"},
  "33B" :{"param" : "2466"},
  "40" :{"param" : "886"},
  "46" :{"param" : "1406"},

  "E1" :{"param" : "1550"},
  "E2" :{"param" : "1551"},
  "E3" :{"param" : "1552"},
  "E4" :{"param" : "1926"},
  "E4B" :{"param" : "2486"},
  "E6" :{"param" : "1928"},
  "E7" :{"param" : "2026"},
  "E8" :{"param" : "1547"},

  "M22" :{"param" : "2906"},
  "M27" :{"param" : "3566"},
  "M29" :{"param" : "3086"},
  "M30" :{"param" : "1746"},
  "M35" :{"param" : "1986"},
  "M36" :{"param" : "2006"},
  "M37" :{"param" : "3606"},
  "M41" :{"param" : "3306"},
  "M42" :{"param" : "3307"},
  "M43" :{"param" : "2646"}
  }

  path = db.child("transports").child("bus").child("route").set(bus_dict)  