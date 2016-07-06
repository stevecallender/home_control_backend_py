
from Casting import *
import subprocess




class NetworkMonitor(Caster):

	def __init__(self):
	
		ownIdentifier = "NetworkUpdate"
		Caster.__init__(self,ownIdentifier)


	def run(self):
	
		EMMA_MAC = "b4-18-d1-d3-35-4e"
		STEVE_MAC= "1c-1a-c0-22-23-e7"

		emmaIp = ""
		steveIp = ""

		stevePresent = False
		emmaPresent = False

		emmaThreshold = 300
		steveThreshold = 300
	
	
		while True:
			emmaIp = self.getIpFromMac(EMMA_MAC)
			steveIp = self.getIpFromMac(STEVE_MAC)
			(out, err) = subprocess.Popen(["fping -m -g 192.168.1.1 192.168.1.10"], stdout=subprocess.PIPE, shell=True).communicate()
			for row in out.split("\n"):
				if row.find(emmaIp) > 1 and row.find("alive") > 1:
					if not emmaPresent:
						self.cast("emma joined")
						emmaPresent = True
					if stevePresent:
						break
				if row.find(steveIp) > 1 and row.find("alive") > 1:
					if not stevePresent:
						self.cast("steve joined")
						stevePresent = True
					if emmaPresent:
						break
			if stevePresent:
				steveThreshold = 300
			elif --steveThreshold < 0:
				self.cast("steve left")
				steveThreshold = 300
			else:
				steveIp = self.getIpFromMac(STEVE_MAC)
			
			if emmaPresent:
				emmaThreshold = 300
			elif --emmaThreshold < 0:
				self.scast("emma left")
				emmaThreshold = 300
			else:
				emma = self.getIpFromMac(EMMA_MAC)
				


	def getIpFromMac(self,macAddress):

		(out, err) = subprocess.Popen(["arp -a"], stdout=subprocess.PIPE, shell=True).communicate()
		index = out.find(macAddress)
		print index
		if (index > -1):
			substring = out[0:index]
			splitarray = substring.split("\n")
			return splitarray[-1].replace(" ","")
		
		return ""
		

if __name__ == "__main__":
	networkMonitor = NetworkMonitor()
	networkMonitor.run()
