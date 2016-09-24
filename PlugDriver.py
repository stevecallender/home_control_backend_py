from Seizing import *
from gpiozero import Energenie

class PlugDriver(Seizer):

	def __init__(self):

		interestedIdentifiers = ["LightsCommand"]
		Seizer.__init__(self,interestedIdentifiers)
		self.allLights = Energenie(1)

	def handleLightsCommand(self, command):
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
				self.handleTimeUpdate(payload)
			else:
				print "Unrecognised header"