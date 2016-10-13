from Seizing import *
from gpiozero import Energenie

class PlugDriver(Seizer):

	def __init__(self):
		interestedIdentifiers = ["LightsCommand"]
		super(PlugDriver,self).__init__()
		self.configureSeizer(interestedIdentifiers,True)
		self.allLights = Energenie(1)

	def handleLightsCommand(self, header):
		if header == "allOn":
			self.allLights.on()
		elif header == "allOff":
			self.allLights.off()
		else:
			print "Unrecognised command"

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
