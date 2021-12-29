import pyrebase

def getConfig():
  config = {  
  "apiKey": "AIzaSyA6pPg3YslzTehYge58ajEQxpmQ8fmbiJc",
  "authDomain": "publictransportapp-fea50.firebaseapp.com",
  "databaseURL": "https://publictransportapp-fea50-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "publictransportapp-fea50",
  "storageBucket": "publictransportapp-fea50.appspot.com",
  "messagingSenderId": "145206856336"
  }
  return config

def getDatabase():
  firebase = pyrebase.initialize_app(getConfig())
  db = firebase.database()    
  return db