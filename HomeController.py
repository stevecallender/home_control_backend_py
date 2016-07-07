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
				self.castWithHeader("MediaCommand","playPlaylist playPlaylist Your\ Coffee\ Break\ \(by \ spotify_uk_\) ")
				self.shouldReact = True
		
		elif payload == "weekend morning":
			if not shouldReact:
				self.castWithHeader("MediaCommand","playPlaylist The\ Great\ British\ Breakfast\ \(by\ spotify_uk_\)")
				self.shouldReact = True
						
		elif payload == "weekday afternoon":
			if self.emmaAtHome or self.steveAtHome:
				self.shouldReact = True
			else:
				self.castWithHeader("MediaCommand","pause")
				self.shouldReact = True
				
		elif payload == "weekday evening":
			if not shouldReact:
				self.shouldReact = True
				
		elif payload == "weekday night":
			if shouldReact:
				self.castWithHeader("MediaCommand","pause")
				self.shouldReact = False

	
	def handleNetworkUpdate(self,payload):

		if payload == "steve joined":
			self.castWithHeader("MediaCommand", "greeting steve")
			self.steveAtHome = True
			if self.shouldReact:
				self.castWithHeader("MediaCommand","playPlaylist Spoon\ City\ Bitch \(by\ stevecallender\)")
				self.shouldReact = False
		
		elif payload == "emma joined":
			self.castWithHeader("MediaCommand", "greeting emma")
			self.emmaAtHome = True
			if self.shouldReact:
				self.castWithHeader("MediaCommand","playPlaylist Spoon\ City\ Bitch \(by\ stevecallender\)")
				self.shouldReact = False
		
		if payload == "steve left":
			self.steveAtHome = False
			if not self.emmaAtHome:
				self.castWithHeader("MediaCommand","pause")
				self.shouldReact = True
		
		elif payload == "emma left":
			self.emmaAtHome = False
			if not self.steveAtHome:
				self.castWithHeader("MediaCommand","pause")
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
