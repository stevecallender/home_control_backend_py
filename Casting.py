import zmq
import time

class Caster(object):

	def __init__(self,identifier):
		self.identifier = identifier
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

		
	def cast(self,message):
		print "Casting message: " + message
		self.publisher.send_multipart([self.identifier, message])
	
	def castWithHeader(self,header,message):
		self.publisher.send_multipart([header, message])
