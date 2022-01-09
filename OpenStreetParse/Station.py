def cleanNodeId(nodeId):
	nodeIdCopy = nodeId
	nodeIdCopy = nodeIdCopy.replace("node/", "")
	return nodeIdCopy

class Station:
	def __init__(self, nodeId, name, coordinates, location="", route_ref=""):
		self.nodeId = cleanNodeId(nodeId)
		self.name = name
		self.coordinates = coordinates
		self.location = location
		self.route_ref = route_ref
	
	def getName(self):
		return self.name

	def getId(self):
		return self.nodeId

	def getCoordinates(self):
		coordinates = dict()
		coordinates["lat"] = self.coordinates[0]
		coordinates["long"] = self.coordinates[1]
		return coordinates

	def getLocation(self):
		return self.location

	def getRoutes(self):
		return self.route_ref

	def printSelf(self):
		if self.location and self.route_ref:
			print(self.name, ", ", self.nodeId, ", ", self.coordinates, ", ", self.location, ", ", self.route_ref)
		else:
			print(self.name, ", ", self.nodeId, ", ", self.coordinates)
			