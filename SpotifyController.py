from Casting import *
from Seizing import *
import subprocess
import time
import sys
from SpotifyConnection import *

class SpotifyController(Caster,Seizer):

    def __init__(self):
        ownIdentifier = "MediaInfo"
        interestedIdentifiers = ["MediaCommand","LightsCommand"]
        super(SpotifyController,self).__init__()
        self.configureSeizer(interestedIdentifiers,True)
        self.configureCaster(ownIdentifier,True)
        self.morningMusic   = "Spoon City"
        self.eveningMusic   = "Lax"
        self.afternoonMusic = "Lax"
        self.isPlaying = False
        self.shouldPoll = True
        self.spotifyConnection = SpotifyConnection()

    def playPlaylist(self,playlist,roomToPlay):
        if not self.isPlaying:
            self.spotifyConnection.playPlaylist(playlist,roomToPlay)
            self.isPlaying = True

    def play(self):
        if not self.isPlaying:
            self.spotifyConnection.play()
            self.isPlaying = True

    def pause(self):
        if self.isPlaying:
            self.spotifyConnection.pause()
            self.isPlaying = False

    def handlePlayInfo(self, infoDict):
        if infoDict:
            self.isPlaying = infoDict['status']
            payload = infoDict['song'] +'::'+infoDict['artist']+'::'+infoDict['progress']
            self.cast(payload.encode('ascii','ignore'))

    def parseCommand(self, command):
        if command == "play":
            self.play()
        elif command.split(" ")[0] == "playPlaylist":
            if command.split(" ")[1] == "earlyMorning":
                self.spotifyConnection.volume(20,'bedroom')
                self.playPlaylist(self.morningMusic,"bedroom")
            elif command.split(" ")[1] == "morning":
                self.spotifyConnection.volume(25,'everywhere')
                self.playPlaylist(self.morningMusic,"everywhere")
            elif command.split(" ")[1] == "afternoon":
                self.playPlaylist(self.afternoonMusic,"everywhere")
            elif command.split(" ")[1] == "evening":
                self.playPlaylist(self.eveningMusic,"everywhere")

        elif command == "pause":
            self.pause()

    def handleLightsCommand(self, header):
            if header == "allOff" or header == "bedRoomOff" or header == "livingRoomOff": 
                print "Disabling poll"
                self.shouldPoll = False
            elif header == "allOn" or header == "bedRoomOn" or header == "livingRoomOn": 
                print "Enabling poll"
                self.shouldPoll = True

    def getPlayInfo(self):
        return  self.spotifyConnection.getTrackInfo()

    def run(self):
        while True:
            [header, payload] = self.seize(False)
            if (header == "LightsCommand"):
               self.handleLightsCommand(payload)
            else:
               self.parseCommand(payload)
               if (self.shouldPoll):
                   out = self.getPlayInfo()
                   self.handlePlayInfo(out)
            time.sleep(3)


if __name__ == "__main__":
    spotifyController = SpotifyController()
    spotifyController.run()


