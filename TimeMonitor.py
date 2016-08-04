from Casting import *
import subprocess, time, datetime


class TimeMonitor(Caster):

	def __init__(self):
	
		ownIdentifier = "TimeUpdate"
		Caster.__init__(self,ownIdentifier)

		
	def run(self):
		while True:
			currentTime = datetime.datetime.now()
			# WEEKEND
			if currentTime.isoweekday() == 6 or currentTime.isoweekday() == 7:
				if currentTime.hour >= 10 and currentTime.hour <= 13:
					self.cast("weekend morning")
				elif currentTime.hour >= 14 and currentTime.hour <= 18:
					self.cast("weekend afternoon")
				elif currentTime.hour >= 19 and currentTime.hour <= 23:
					self.cast("weekend evening")
				else:
					self.cast("weekend night")
			# WEEKDAY
			else:
				if currentTime.hour >= 6 and currentTime.hour <= 11:
					self.cast("weekday morning")
				elif currentTime.hour >= 12 and currentTime.hour <= 17:
					self.cast("weekday afternoon")
				elif currentTime.hour >= 18 and currentTime.hour <= 21:
					self.cast("weekday evening")
				else:
					self.cast("weekday night")
			time.sleep(50)
			
if __name__ == "__main__":
	timeMonitor = TimeMonitor()
	timeMonitor.run()
