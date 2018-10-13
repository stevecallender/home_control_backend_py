import zmq
import time, datetime

class Seizer(object):

	def __init__(self):
		super(Seizer, self).__init__()
		print "Initialising Seizer"
		self.identifiers = []
		self.shouldLog   = False
		context         = zmq.Context()
		self.subscriber = context.socket(zmq.SUB)
		portList = ["5560","5561","5562","5563","5564","5565"]
		ipMax =10 #connect to the first 10 ip addresses
		for port in portList: 
			self.subscriber.connect("tcp://localhost:"+port)
			for ip in range(1,20):
				self.subscriber.connect("tcp://192.168.1."+str(ip)+":"+port)
			self.subscriber.connect("tcp://192.168.1.75:"+port) #hack for non-static mopoidy ip
			self.subscriber.connect("tcp://192.168.1.102:"+port) #hack for non-static mopoidy ip

	def configureSeizer(self,identifiers,shouldLog = False):
		self.identifiers = identifiers
                self.shouldLog  = shouldLog
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
		if contents != "" and self.shouldLog:
			if blocking:
                        	print "Blocking Seizing message: "+contents+ "at "+str(datetime.datetime.now())
			else:
				print "Non-Blocking Seizing message: "+contents + "at "+str(datetime.datetime.now())
		return [address,contents]

			

