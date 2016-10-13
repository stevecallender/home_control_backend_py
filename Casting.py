import zmq
import time, datetime

class Caster(object):

	def __init__(self):
		super(Caster, self).__init__()
		print "Initialising Caster"
		self.identifier = ""
		self.shouldLog  = False
		context         = zmq.Context()
		self.publisher  = context.socket(zmq.PUB)
		
		portList = ["5560","5561","5562","5563","5564","5565"]
		portIndex = 0
		conneted = False
		while not conneted:
			port = portList[portIndex]
			try:
				self.publisher.bind("tcp://*:"+port)
				conneted = True
				print "Connected to port: " + port
			except:
				print "Trying next port"
				portIndex += 1

	def configureCaster(self,identifier, shouldLog = False):
		self.identifier = identifier
                self.shouldLog  = shouldLog		


	def cast(self,message):
		if self.shouldLog:
			print "Casting message: " + message + "at " +str(datetime.datetime.now())
		self.publisher.send_multipart([self.identifier, message])
	
	def castWithHeader(self,header,message):
		if self.shouldLog:
			print "Casting message: " + message + "at "+str(datetime.datetime.now())
		self.publisher.send_multipart([header, message])
