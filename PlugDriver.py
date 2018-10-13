from Seizing import *
from gpiozero import Energenie

class PlugDriver(Seizer):

	def __init__(self):
		interestedIdentifiers = ["LightsCommand"]
		super(PlugDriver,self).__init__()
		self.configureSeizer(interestedIdentifiers,True)
		self.livingRoomLights = Energenie(1)
		self.bedRoomLights = Energenie(2)

	def handleLightsCommand(self, header):
		if header == "allOn":
			self.allOn()
                elif header == "bedRoomOn": 
                        self.bedRoomLights.on() 
                elif header == "livingRoomOn":
                        self.livingRoomLights.on()
		elif header == "allOff":
			self.allOff()
		elif header == "bedRoomOff":
			self.bedRoomLights.off()
                elif header == "livingRoomOff": 
                        self.livingRoomLights.off()
		else:
			print "Unrecognised command: " + header + "."

	def allOff(self):
		self.livingRoomLights.off()
		self.bedRoomLights.off()

	def allOn(self):
		self.livingRoomLights.on()
		self.bedRoomLights.on()

	def run(self):
		while True:
			[header, payload] = self.seize()
			if header == "LightsCommand":
				self.handleLightsCommand(payload)
			else:
				print "Unrecognised header"


if __name__ == "__main__":
        plugDriver = PlugDriver()
        plugDriver.run()
