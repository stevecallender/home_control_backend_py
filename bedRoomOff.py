from Casting import *
import time

class Lights(Caster):

        def __init__(self):

                ownIdentifier = "LightsCommand"
                super(Lights,self).__init__()
                self.configureCaster(ownIdentifier,True)

        def sendMessage(self):
                self.castWithHeader("LightsCommand","bedRoomOff")
                time.sleep(0.5)
                self.castWithHeader("LightsCommand","bedRoomOff")
                time.sleep(2)
                self.castWithHeader("LightsCommand","bedRoomOff")

if __name__ == "__main__":
        lights = Lights()
        lights.sendMessage()
