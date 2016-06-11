import sys
import zmq
import os
import subprocess
#  Socket to publish on
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:5555")


EMMA_MAC = "b4-18-d1-d3-35-4e"
STEVE_MAC= "1c-1a-c0-22-23-e7"


emmaIp = ""
steveIp = ""

stevePresent = False
emmaPresent = False

emmaThreshold = 300
steveThreshold = 300

commsout = ""

def mainLoop():
	while True:
	#socket.send("Hello")
	#string = socket.recv_string()
	#print string
		emmaIp = getIpFromMac(EMMA_MAC)
		steveIp = getIpFromMac(STEVE_MAC)
		(out, err) = subprocess.Popen(["fping -m -g 192.168.1.1 192.168.1.10"], stdout=subprocess.PIPE, shell=True).communicate()
		for row in out.split("\n"):
			if row.find(emmaIp) > 1 and row.find("alive") > 1:
				emmaPresent = True
				if stevePresent:
					break
			if row.find(steveIp) > 1 and row.find("alive") > 1:
				stevePresent = True
				if emmaPresent:
					break
		if stevePresent:
			steveThreshold = 300
		else if steveThreshold-- < 0:
			commsout = "STEVE GONE"
			steveThreshold = 300
		else:
			steveIp = getIpFromMac(STEVE_MAC)
		
		if emmaPresent:
			emmaThreshold = 300
		else if emmaThreshold-- < 0:
			commsout = "EMMA GONE"
			emmaThreshold = 300
		else:
			emma = getIpFromMac(EMMA_MAC)
			
			

	
	
def getIpFromMac(macAddress):

	(out, err) = subprocess.Popen(["arp -a"], stdout=subprocess.PIPE, shell=True).communicate()
	index = out.find(macAddress)
	print index
	if (index > -1):
		substring = out[0:index]
		splitarray = substring.split("\n")
		return splitarray[-1].replace(" ","")
	
	return ""
	

	
getIpFromMac("1c-1a-c0-22-23-e7")