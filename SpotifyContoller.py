#from Casting import *
#from Seizing import *
import subprocess
import time
import requests

class MediaPlayer(Caster,Seizer):
	
	def __init__(self):
		ownIdentifier = "MediaInfo"
		interestedIdentifiers = ["MediaCommand"]
		super(MediaPlayer,self).__init__()
		self.configureSeizer(interestedIdentifiers,True)
                self.configureCaster(ownIdentifier,True)		
		self.morningMusic   = "Spoon\ City\ Bitch\ \(by\ stevecallender\)"
		self.eveningMusic   = "Lax\ \(by\ stevecallender\)"
		self.afternoonMusic = "Lax\ \(by\ stevecallender\)" 
		self.morningRadio   = "radio4"
		self.afternoonRadio = "radio4"
		self.eveningRadio   = "radio4"
		self.freshSetup()


	def freshSetup(self):

		self.isPlaying = False
		self.currentInfo = ""

	def playPlaylist(self,playlist):
		self.freshSetup()
		subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()

		if (playlist == self.morningRadio or playlist == self.afternoonRadio or playlist == self.eveningRadio):
			subprocess.Popen(["mpc volume 100"], stdout=subprocess.PIPE, shell=True).communicate()

        def play(self):
                if not self.isPlaying :
			self.freshSetup()
                        self.playPlaylist(self.eveningMusic)	

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
		try:
			songAndArtist = info.split("\n")[0]
			progress = ((info.split("\n")[1]).split("(")[-1]).split("%")[0]
			payload = songAndArtist + "::" + progress
			self.cast(payload)
			print payload
		except:
			print "exception caught!"
			return

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
			(out, err) = subprocess.Popen(["mpc status"], stdout=subprocess.PIPE, shell=True).communicate()
			self.handlePlayInfo(out)
			time.sleep(3)
			
			
			
			
if __name__ == "__main__":
#	mediaPlayer = MediaPlayer()
#	mediaPlayer.run()

       r = requests.get("https://api.spotify.com/v1/me/player/devices")
       
       print(r.status_code)
       print(r.headers)
       print(r.content)
