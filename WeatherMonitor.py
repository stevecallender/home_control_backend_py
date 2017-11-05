import pyowm
from Casting import *

class WeatherMonitor(Caster):

        def __init__(self):
        
                ownIdentifier = "WeatherInfo"
                super(WeatherMonitor,self).__init__()
                self.configureCaster(ownIdentifier,True)

                
        def run(self):
		owm = pyowm.OWM('192b6480022247ba540623bdd3da923b')
                while True:
			try:
				observation = owm.weather_at_place('Edinburgh,uk')
				w = observation.get_weather()
				tempString = w.get_temperature('celsius')
				temp = tempString["temp"]
				max = tempString["temp_max"]			
				min = tempString["temp_min"]			
				print tempString
				self.cast(str(temp)+","+str(min)+","+str(max))
			except:
				print "Failed to call"
			time.sleep(60)
			
                        
if __name__ == "__main__":
        weatherMonitor = WeatherMonitor()
        weatherMonitor.run()
