from HomeController import *
from Casting import *
from Seizing import *


class TestDriver(Caster,Seizer):


	def __init__(self):
		Seizer.__init__(self,"MediaCommand")
		Caster.__init__(self,"")
		
		self.test_steveArrival     = "steve joined"
		self.test_emmaArrival      = "emma joined"
		self.test_weekdayMorning   = "weekday morning"
		self.test_weekdayAfternoon = "weekday afternoon"
		self.test_weekdayEvening   = "weekday evening"
		self.test_weekdayNight     = "weekday night"

	def run(self):
		while True:
			print "1 - steve joined"
			print "2 - emma joined"
			print "3 - weekday morning"
			print "4 - weekday afternoon"
			print "5 - weekday evening"
			print "6 - weekday night"
			ip = input()
			print ip
			if ip == 1:
				self.castWithHeader("NetworkUpdate",self.test_steveArrival)
			elif ip == 2:
				self.castWithHeader("NetworkUpdate",self.test_emmaArrival)
			elif ip == 3:
				self.castWithHeader("TimeUpdate",self.test_weekdayMorning)
			elif ip == 4:
				self.castWithHeader("TimeUpdate",self.test_weekdayAfternoon)
			elif ip == 5:
				self.castWithHeader("TimeUpdate",self.test_weekdayEvening)
			elif ip == 6:
				self.castWithHeader("TimeUpdate",self.test_weekdayNight)
			
			[header, payload] = self.seize()
			
			print header + payload
		
		
	


if __name__ == "__main__":
	driver = TestDriver()
	driver.run()
