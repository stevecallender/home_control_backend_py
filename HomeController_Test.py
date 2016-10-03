from HomeController import *
from Casting import *
from Seizing import *


class TestDriver(Caster,Seizer):


	def __init__(self):
		Seizer.__init__(self,"MediaCommand",True)
		Caster.__init__(self,"",True)
		
		self.test_steveArrival     = "steve joined"
		self.test_emmaArrival      = "emma joined"
		self.test_steveLeft        = "steve left"
                self.test_emmaLeft         = "emma left"
		self.test_weekdayMorning   = "weekday morning"
		self.test_weekdayAfternoon = "weekday afternoon"
		self.test_weekdayEvening   = "weekday evening"
		self.test_weekdayNight     = "weekday night"

	def run(self):
		while True:
			print "1 - steve   joined"
			print "2 - emma    joined"
			print "3 - steve   left"
                        print "4 - emma    left"
			print "5 - weekday morning"
			print "6 - weekday afternoon"
			print "7 - weekday evening"
			print "8 - weekday night"
			ip = input()
			print ip
			if ip == 1:
				self.castWithHeader("NetworkUpdate",self.test_steveArrival)
			elif ip == 2:
				self.castWithHeader("NetworkUpdate",self.test_emmaArrival)
			elif ip == 3:
                                self.castWithHeader("NetworkUpdate",self.test_steveLeft)
                        elif ip == 4:
                                self.castWithHeader("NetworkUpdate",self.test_emmaLeft)
			elif ip == 5:
				self.castWithHeader("TimeUpdate",self.test_weekdayMorning)
			elif ip == 6:
				self.castWithHeader("TimeUpdate",self.test_weekdayAfternoon)
			elif ip == 7:
				self.castWithHeader("TimeUpdate",self.test_weekdayEvening)
			elif ip == 8:
				self.castWithHeader("TimeUpdate",self.test_weekdayNight)
			
			[header, payload] = self.seize()
			
			print header + payload
		
		
	


if __name__ == "__main__":
	driver = TestDriver()
	driver.run()
