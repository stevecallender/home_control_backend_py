from Casting import *
from Seizing import *
import subprocess
import time

class HomeController(Seizer,Caster):
	
	def __init__(self):
		ownIdentifier = "HomeController"
		
		self.mediaCommand = "MediaCommand"
		self.plugCommmand = "PlugCommand"
		
		interestedIdentifiers = ["TimeUpdate","NetworkUpdate","MediaInfo"]
		Caster.__init__(self,ownIdentifier)
		Seizer.__init__(self,interestedIdentifiers)
		
		self.steveAtHome = False
		self.emmaAtHome  = False
		
		self.shouldReact = False
	
	def handleTimeUpdate(self,payload):
		if payload == "weekday morning":
			if not shouldReact:
				self.cast("MediaCommand","playPlaylist morning")
				self.shouldReact = True
				
		elif payload == "weekday afternoon":
			if self.emmaAtHome or self.steveAtHome:
				self.shouldReact = True
			else:
				self.cast("MediaCommand","pause")
				
		elif payload == "weekday evening":
			if not shouldReact:
				self.cast("MediaCommand","playPlaylist evening")
				self.shouldReact = True
				
		elif payload == "weekday night":
			if shouldReact:
				self.cast("MediaCommand","pause")
				self.shouldReact = False

	
	def handleNetworkUpdate(self,payload):

		if payload == "steve joined":
			self.cast("MediaCommand", "greeting steve")
			self.steveAtHome = True
			if self.shouldReact:
				self.cast("MediaCommand","playPlaylist morning")
				self.shouldReact = False
		
		elif payload == "emma joined":
			self.cast("MediaCommand", "greeting emma")
			self.emmaAtHome = True
			if self.shouldReact:
				self.cast("MediaCommand","playPlaylist morning")
				self.shouldReact = False
		
		if payload == "steve left":
			self.steveAtHome = False
			if not self.emmaAtHome:
				self.cast("MediaCommand","pause")
				self.shouldReact = True
		
		elif payload == "emma left":
			self.emmaAtHome = False
			if not self.steveAtHome:
				self.cast("MediaCommand","pause")
				self.shouldReact = True
		

	
	def handleMediaUpdate(payload):
		print "currently unsupported"
		
	
	def run(self):
		while True:
			[header, payload] = self.seize()
			if header == "TimeUpdate":
				self.handleTimeUpdate(payload)
			elif header == "NetworkUpdate":
				self.handleNetworkUpdate(payload)
			elif header == "MediaInfo":
				self.handleMediaUpdate(payload)
				
				
if __name__ == "__main__":
	homeController = HomeController()
	homeController.run()