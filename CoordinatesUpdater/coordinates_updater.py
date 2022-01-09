from /../database_config import getDatabase


def coordinates_updater():
	db = getDatabase()
	path = db.child("coordinates").set("lat")

coordinates_updater()