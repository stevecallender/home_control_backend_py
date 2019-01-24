from Casting import *
from Seizing import *
import subprocess
import time
import sys
from SpotifyConnection import * 

class SpotifyController(Caster,Seizer):
    
    def __init__(self):
        ownIdentifier = "MediaInfo"
        interestedIdentifiers = ["MediaCommand"]
        super(SpotifyController,self).__init__()
        self.configureSeizer(interestedIdentifiers,True)  
        self.configureCaster(ownIdentifier,False)        
        self.morningMusic   = "Spoon City"
        self.eveningMusic   = "Lax"
        self.afternoonMusic = "Lax" 
        self.spotifyConnection = SpotifyConnection()
        


    def playPlaylist(self,playlist):
        self.spotifyConnection.playPlaylist(playlist)

    def play(self):
        self.spotifyConnection.play()

    def pause(self):
        self.spotifyConnection.pause()
    
    def handlePlayInfo(self, infoDict):
        payload = infoDict['song'] +'::'+infoDict['artist']+'::'+infoDict['progress'] 
        self.cast(payload.encode())
        print payload

    def parseCommand(self, command):
        if command == "play":
            self.play()
        elif command.split(" ")[0] == "playPlaylist": 
            if command.split(" ")[1] == "morning":
                self.playPlaylist(self.morningMusic)
            elif command.split(" ")[1] == "afternoon":
                self.playPlaylist(self.afternoonMusic)
            elif command.split(" ")[1] == "evening":
                self.playPlaylist(self.eveningMusic)

        elif command == "pause":
            self.pause()
        else:
            print "Unrecognised command: "
            print command

    def getPlayInfo(self):
        return  self.spotifyConnection.getTrackInfo()

    def run(self):
        while True:
            [header, payload] = self.seize(False)
            self.parseCommand(payload)
            out = self.getPlayInfo()
            self.handlePlayInfo(out)
            time.sleep(3)


if __name__ == "__main__":
    spotifyController = SpotifyController()
    spotifyController.run()


