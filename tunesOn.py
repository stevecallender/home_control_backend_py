from Casting import *
import time

class Tunes(Caster):

        def __init__(self):

		ownIdentifier = "MediaCommand"
                super(Tunes,self).__init__()
                self.configureCaster(ownIdentifier,True)

        def sendMessage(self):
		self.castWithHeader("MediaCommand","play")
		time.sleep(0.5)
                self.castWithHeader("MediaCommand","play")

if __name__ == "__main__":
        tunes = Tunes()
        tunes.sendMessage()



