\
from Casting import *
import subprocess




class NetworkMonitor(Caster):

	def __init__(self):
	
		ownIdentifier = "NetworkUpdate"
		Caster.__init__(self,ownIdentifier,True)


	def run(self):
	
		EMMA_MAC = "b4:18:d1:d3:35:4e"
		STEVE_MAC= "1c:1a:c0:22:23:e7"

		emmaIp = ""
		steveIp = ""

		stevePresent = False
		emmaPresent = False


		emmaThreshold = 60
		steveThreshold = 60
	
	
		while True:
			#default the detections to false before each attempt
			steveDetected = False
			emmaDetected = False
			print "AHAJHDJKGFKJHSKJGKJFG "
			print emmaThreshold
			emmaIp = self.getIpFromMac(EMMA_MAC)
			steveIp = self.getIpFromMac(STEVE_MAC)
			(out, err) = subprocess.Popen(["fping -m -g 192.168.1.1 192.168.1.12"], stdout=subprocess.PIPE, shell=True).communicate()
			for row in out.split("\n"):
				print "ROW " + row
				if row.find(emmaIp) > -1 and row.find("alive") > -1:
					emmaDetected = True
					print "Emma ip " +emmaIp
					if not emmaPresent:
						self.cast("emma joined")
						emmaPresent = True
					if stevePresent:
						break

				if row.find(steveIp) > -1 and row.find("alive") > -1:
					steveDetected = True
					print "Steve ip " +steveIp
					if not stevePresent:
						self.cast("steve joined")
						stevePresent = True
					if emmaPresent:
						break

			if steveDetected:
				steveThreshold = 60
			elif steveThreshold <= 0:
				if stevePresent:
					self.cast("steve left")
					stevePresent = False
			else:
				steveThreshold -= 1
				steveIp = self.getIpFromMac(STEVE_MAC)
			
			if emmaDetected:
				emmaThreshold = 60
			elif emmaThreshold <= 0: #if the threshold his 0 and she is not detected then she must have left
				if emmaPresent: #but we only want to notify if she was previously present
					self.cast("emma left")
					emmaPresent = False
			else: #we only get here is she is not detected and the threshold is not reached
				emmaThreshold -= 1
				emma = self.getIpFromMac(EMMA_MAC)
				


	def getIpFromMac(self,macAddress):

		(out, err) = subprocess.Popen(["arp -an"], stdout=subprocess.PIPE, shell=True).communicate()
		index = out.find(macAddress)
		if (index > -1):
			substring = out[0:index]
			ipLine = substring.split("\n")[-1]
			ip = ipLine.split("(")[-1].split(")")[0]
			return ip
		
		return "NO_IP"
		

if __name__ == "__main__":
	networkMonitor = NetworkMonitor()
	networkMonitor.run()
