from HomeController import *
from Casting import *
from Seizing import *


class TestDriver(Caster,Seizer):


	def __init__(self):
		super(TestDriver,self).__init__()
		self.configureCaster("",True)
		self.configureSeizer("MediaCommand",True)
		
		self.test_steveArrival     	= "steve joined"
		self.test_emmaArrival      	= "emma joined"
		self.test_steveLeft        	= "steve left"
                self.test_emmaLeft         	= "emma left"
		self.test_weekdayEarlyMorning	= "weekday early morning"
		self.test_weekdayMorning   	= "weekday morning"
		self.test_weekdayAfternoon 	= "weekday afternoon"
		self.test_weekdayEvening   	= "weekday evening"
		self.test_weekdayNight     	= "weekday night"

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
			print "9 - weekday early morning"
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
			elif ip == 9:
                                self.castWithHeader("TimeUpdate",self.test_weekdayEarlyMorning)

			
			[header, payload] = self.seize()
			
			print header + payload
		
		
	


if __name__ == "__main__":
	driver = TestDriver()
	driver.run()
