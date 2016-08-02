import zmq
import time

class Seizer(object):

	def __init__(self,identifiers):
		self.identifiers = identifiers
		context         = zmq.Context()
		self.subscriber = context.socket(zmq.SUB)
		portList = ["5560","5561","5562","5563","5564","5565"]
		
		for port in portList:
			self.subscriber.connect("tcp://localhost:"+port)
			self.subscriber.connect("tcp://192.168.1.8:"+port)
			self.subscriber.connect("tcp://192.168.1.1:"+port)


		
		for id in self.identifiers:
			self.subscriber.setsockopt(zmq.SUBSCRIBE, id)
		
	def seize(self, blocking = True):
		[address,contents] = ("","")
		if blocking:
			[address, contents] = self.subscriber.recv_multipart()
		else:
			try:
				[address, contents] = self.subscriber.recv_multipart(flags=zmq.NOBLOCK)
			except:
				pass #no message to seize - no problem
		if contents != "": 
			print "Seizing message: "+contents
		return [address,contents]

			

