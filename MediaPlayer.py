from Casting import *
from Seizing import *
import subprocess
import time

class MediaPlayer(Seizer,Caster):
	
	def __init__(self):
		ownIdentifier = "MediaInfo"
		interestedIdentifiers = ["MediaCommand"]
		Caster.__init__(self,ownIdentifier)
		Seizer.__init__(self,interestedIdentifiers)
		
		subprocess.Popen(["mpc clear"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc random"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc repeat"], stdout=subprocess.PIPE, shell=True).communicate()
		time.sleep(1)
		subprocess.Popen(["mpc volume 60"], stdout=subprocess.PIPE, shell=True).communicate()

		self.isPlaying = False
		self.currentInfo = ""
		
		
	def play(self):
		if not self.isPlaying :
			print "Playing"
			(out, err) = subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying  = True
	
	def playPlaylist(self,playlist):
		if not self.isPlaying :
			(out, err) = subprocess.Popen(["mpc clear"], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			(out, err) = subprocess.Popen(["mpc load " + playlist], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			(out, err) = subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying  = True
	
	def next(self):
		if self.isPlaying :
			(out, err) = subprocess.Popen(["mpc next"], stdout=subprocess.PIPE, shell=True).communicate()
		else:
			(out, err) = subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			(out, err) = subprocess.Popen(["mpc next"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying   = True
	
	def previous(self):
		if self.isPlaying :
			(out, err) = subprocess.Popen(["mpc prev"], stdout=subprocess.PIPE, shell=True).communicate()
		else:
			(out, err) = subprocess.Popen(["mpc play"], stdout=subprocess.PIPE, shell=True).communicate()
			time.sleep(1)
			(out, err) = subprocess.Popen(["mpc prev"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying   = True
	
	def pause(self):
		if self.isPlaying :
			(out, err) = subprocess.Popen(["mpc pause"], stdout=subprocess.PIPE, shell=True).communicate()
			self.isPlaying  = False
	
	def handlePlayInfo(self, info):
		if info != self.currentInfo:
			self.cast(info)
			self.currentInfo = info

	def parseCommand(self, command):
		if command == "play":
			self.play()
		if command.split(" ")[0] == "playPlaylist":
			self.playPlaylist(command.split(" ",1)[-1])
		if command == "pause":
			self.pause()
			
			
	def run(self):
		while True:
			[header, payload] = self.seize(False)
			self.parseCommand(payload) 
			(out, err) = subprocess.Popen(["mpc current"], stdout=subprocess.PIPE, shell=True).communicate()
			self.handlePlayInfo(out)
			time.sleep(2)
			
			
			
			
if __name__ == "__main__":
	mediaPlayer = MediaPlayer()
	mediaPlayer.run()
