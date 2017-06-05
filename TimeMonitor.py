from Casting import *
import subprocess, time, datetime


class TimeMonitor(Caster):

	def __init__(self):
	
		ownIdentifier = "TimeUpdate"
		super(TimeMonitor,self).__init__()
                self.configureCaster(ownIdentifier,True)

		
	def run(self):
		while True:
			currentTime = datetime.datetime.now()
			self.castWithHeader("TimeValue",str(currentTime.hour)+":"+str(currentTime.minute))
			# WEEKEND
			if currentTime.isoweekday() == 6 or currentTime.isoweekday() == 7:
				if currentTime.hour >= 9 and currentTime.hour <= 13:
					self.cast("weekend morning")
				elif currentTime.hour >= 14 and currentTime.hour <= 20:
					self.cast("weekend afternoon")
				elif currentTime.hour >= 21 and currentTime.hour <= 22:
					self.cast("weekend evening")
				else:
					self.cast("weekend night")
			# WEEKDAY
			else:
				if currentTime.hour == 6:
					self.cast("weekday early morning")
				elif currentTime.hour >= 7 and currentTime.hour <= 11:
					self.cast("weekday morning")
				elif currentTime.hour >= 12 and currentTime.hour <= 20:
					self.cast("weekday afternoon")
				elif currentTime.hour >= 21 and currentTime.hour <= 22:
					self.cast("weekday evening")
				else:
					self.cast("weekday night")
			time.sleep(60)
			
if __name__ == "__main__":
	timeMonitor = TimeMonitor()
	timeMonitor.run()
