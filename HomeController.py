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

		Seizer.__init__(self,interestedIdentifiers)
		Caster.__init__(self,ownIdentifier,True)		

		self.steveAtHome = False
		self.emmaAtHome  = False
		
		self.shouldReact = False
		self.lastTimeUpdate = ""
	
	def handleTimeUpdate(self,payload):

		#this will ensure that each time update only occurs once
		if payload == self.lastTimeUpdate:
			return

		#if we get to here then it is a new time update
		self.lastTimeUpdate = payload

		if payload == "weekday morning":
			self.castWithHeader("MediaCommand","playPlaylist Your\ Coffee\ Break\ \(by\ spotify_uk_\)")
			self.castWithHeader("LightsCommand","allOn")
	
		
		elif payload == "weekend morning":		
			self.castWithHeader("MediaCommand","playPlaylist The\ Great\ British\ Breakfast\ \(by\ spotify_uk_\)")
			self.castWithHeader("LightsCommand","allOn")
						
		elif payload == "weekday afternoon":
			if self.emmaAtHome or self.steveAtHome:
				self.castWithHeader("LightsCommand","allOff")
			else:
				self.castWithHeader("MediaCommand","pause")
				self.castWithHeader("LightsCommand","allOff")
				self.shouldReact = True
				
		elif payload == "weekday evening":
			if self.emmaAtHome or self.steveAtHome:
				self.castWithHeader("LightsCommand","allOn")
			else:
				self.shouldReact = True
				
		elif payload == "weekday night":
			self.castWithHeader("MediaCommand","pause")
			self.castWithHeader("LightsCommand","allOff")
			self.shouldReact = False
		
		elif payload == "weekend night":
			self.castWithHeader("MediaCommand","pause")
			self.castWithHeader("LightsCommand","allOff")
			self.shouldReact = False

	
	def handleNetworkUpdate(self,payload):

		if payload == "steve joined":
			self.castWithHeader("MediaCommand", "greeting steve")
			self.steveAtHome = True
			if self.shouldReact:
				self.castWithHeader("MediaCommand","playPlaylist Spoon\ City\ Bitch\ \(by\ stevecallender\)")
				self.castWithHeader("LightsCommand","allOn")
				self.shouldReact = False
		
		elif payload == "emma joined":
			self.castWithHeader("MediaCommand", "greeting emma")
			self.emmaAtHome = True
			if self.shouldReact:
				self.castWithHeader("MediaCommand","playPlaylist Spoon\ City\ Bitch\ \(by\ stevecallender\)")
				self.castWithHeader("LightsCommand","allOn")
				self.shouldReact = False
		
		if payload == "steve left":
			self.steveAtHome = False
			if not self.emmaAtHome:
				self.castWithHeader("MediaCommand","pause")
				self.castWithHeader("LightsCommand","allOff")
				self.shouldReact = True
		
		elif payload == "emma left":
			self.emmaAtHome = False
			if not self.steveAtHome:
				self.castWithHeader("MediaCommand","pause")
				self.castWithHeader("LightsCommand","allOff")
				self.shouldReact = True



	def run(self):
		while True:
			[header, payload] = self.seize()
			if header == "TimeUpdate":
				self.handleTimeUpdate(payload)
			elif header == "NetworkUpdate":
				self.handleNetworkUpdate(payload)
			
				
				
if __name__ == "__main__":
	homeController = HomeController()
	homeController.run()
