import zmq
import time

class Seizer(object):

	def __init__(self,identifiers):
		self.identifiers = identifiers
		context         = zmq.Context()
		self.subscriber = context.socket(zmq.SUB)
		self.subscriber.connect("tcp://localhost:5560")
		self.subscriber.connect("tcp://localhost:5561")
		self.subscriber.connect("tcp://localhost:5562")
		self.subscriber.connect("tcp://localhost:5563")
		self.subscriber.connect("tcp://localhost:5563")
		self.subscriber.connect("tcp://localhost:5564")
		self.subscriber.connect("tcp://localhost:5565")
		
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
		return [address,contents]
			

