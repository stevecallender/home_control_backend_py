from Casting import *
from Seizing import *
import subprocess
import time

class MediaPlayer(Caster,Seizer):
	
	def __init__(self):
		ownIdentifier = "MediaInfo"
		interestedIdentifiers = ["MediaCommand"]
		super(MediaPlayer,self).__init__()
		self.configureSeizer(interestedIdentifiers,True)
                self.configureCaster(ownIdentifier,True)		
		self.freshSetup()
		self.morningMusic   = "Classical\ \(by\ stevecallender\)"
		self.eveningMusic   = "Spoon\ City\ Bitch\ \(by\ stevecallender\)"
		self.afternoonMusic = "Vacation\ Haus\ \(by\ spotify\)" 
		self.morningRadio   = "radio4"
		self.afternoonRadio = "radio4"
		self.eveningRadio   = "radio4"


	def freshSetup(self):
		subprocess.Popen(["mpc clear"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc random true"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc repeat true"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc volume 18"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)

		self.isPlaying = False
		self.currentInfo = ""

	def play(self):
		if not self.isPlaying :
			subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying  = True
	
	def playPlaylist(self,playlist):
		self.freshSetup()
		subprocess.Popen(["mpc load " + playlist], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
		self.isPlaying  = True
	
	def next(self):
		if self.isPlaying :
			subprocess.Popen(["mpc next"], stdout=subprocess.PIPE, shell=True).communicate()
		else:
			subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			subprocess.Popen(["mpc next"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying   = True
	
	def previous(self):
		if self.isPlaying :
			subprocess.Popen(["mpc prev"], stdout=subprocess.PIPE, shell=True).communicate()
		else:
			subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			subprocess.Popen(["mpc prev"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying   = True
	
	def pause(self):
		if self.isPlaying :
			subprocess.Popen(["mpc pause"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying  = False
	
	def handlePlayInfo(self, info):
		if info != self.currentInfo:
			self.cast(info)
			self.currentInfo = info

	def parseCommand(self, command):
		if command == "play":
			self.play()
		if command.split(" ")[0] == "playPlaylist":
			if command.split(" ") [-1] == "radio":
				if command.split(" ")[1] == "morning":
					self.playPlaylist(self.morningRadio)
				elif command.split(" ")[1] == "afternoon":
                        	        self.playPlaylist(self.afternoonRadio)
				elif command.split(" ")[1] == "evening":
                                	self.playPlaylist(self.eveningRadio)
			else: 
				if command.split(" ")[1] == "morning":
                                        self.playPlaylist(self.morningMusic)
                                elif command.split(" ")[1] == "afternoon":
                                        self.playPlaylist(self.afternoonMusic)
                                elif command.split(" ")[1] == "evening":
                                        self.playPlaylist(self.eveningMusic)



		if command == "pause":
			self.pause()
		if command == "next":
			self.next()
		if command == "prev":
			self.prev()
			
			
	def run(self):
		while True:
			[header, payload] = self.seize(False)
			self.parseCommand(payload) 
			(out, err) = subprocess.Popen(["mpc current"], stdout=subprocess.PIPE, shell=True).communicate()
			self.handlePlayInfo(out)
			time.sleep(3)
			
			
			
			
if __name__ == "__main__":
	mediaPlayer = MediaPlayer()
	mediaPlayer.run()
