from Seizing import *
import subprocess
import sys

class Monitor(Seizer):
        
	def __init__(self):
		interestedIdentifiers = ["TimeUpdate","NetworkUpdate","MediaInfo","HomeControl","MediaCommand"]

		super(Monitor,self).__init__()           

		self.configureSeizer(interestedIdentifiers,True)

		self.lastTimeUpdate = ""
        
	def handleTimeUpdate(self,payload):
		if payload == self.lastTimeUpdate:
			return
		else:
			print payload



	def run(self):
		while True:
			[header, payload] = self.seize(False)
			if header == "TimeUpdate":
				self.handleTimeUpdate(payload)
			else:
				if payload != "":
					print payload               
                                
                                
if __name__ == "__main__":
	monitor = Monitor()
	monitor.run()
