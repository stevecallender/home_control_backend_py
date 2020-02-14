
import subprocess
import time
import sys
import spotipy
import spotipy.util as util
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyConnection():

    def __init__(self):
        self.scopes = 'user-library-read user-modify-playback-state user-read-playback-state'
        self.stevensEchoId = ''
        self.stevensDotId = ''
        self.username =  "Flatpi"
        self.token = util.prompt_for_user_token(self.username, self.scopes)
        self.playLists = {}
        self.tokenExpiration = "tokenExpiration"
        self.badGateway = "badGateway"
        self.retryThreshold = 100

        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            print "Initialising connection failed can't get token for", username
        self.populatePlaylists()
        self.getDevices()

    def getDevices(self):
        try:
            print self.sp.devices()
            for device in self.sp.devices()['devices']:
                if device['name'] == 'Steven\'s Echo':
                    self.stevensEchoId = device['id']
                    break
                elif device['name'] == 'Steven\'s Echo Dot':
                    self.stevensDotId = device['id']
                    break

        except spotipy.client.SpotifyException:
            self.fixMyError(self.badGateway,self.getDevices)

    def populatePlaylists(self):
        try:
            playlists = self.sp.user_playlists(self.username)['items']
            for pl in playlists:
                self.playLists[pl['name']] = pl['uri']
        except spotipy.client.SpotifyException:
            self.fixMyError(self.badGateway,self.populatePlaylists)

    def volume(self,value):
        try:
            self.retryThreshold = 100
            self.sp.volume(value,device_id=self.stevensEchoId)
        except spotipy.client.SpotifyException:
            self.fixMyError(self.badGateway,self.volume)

    def playPlaylist(self,playlistName,roomToPlay):
        try:
            deviceToPlay = self.stevensEchoId
            if (roomToPlay == "bedroom"):
                deviceToPlay = self.stevensDotId
            self.retryThreshold = 100
            self.sp.shuffle(True, device_id=deviceToPlay)
            playlistResult = self.playLists[playlistName]
            self.sp.start_playback(device_id=deviceToPlay, context_uri=playlistResult, uris=None, offset=None)
        except spotipy.client.SpotifyException:
            self.fixMyError(self.badGateway,self.playPlaylist,playlistName,roomToPlay)

    def play(self):
        try:
            self.retryThreshold = 100
            self.sp.start_playback(device_id=self.stevensEchoId)
        except spotipy.client.SpotifyException:
            self.fixMyError(self.badGateway,self.play)

    def pause(self):
        try:
            self.retryThreshold = 100
            self.sp.pause_playback()
        except Exception as e:
            print e
            self.fixMyError(self.badGateway,self.pause)

    def getTrackInfo(self):
        try:
            self.retryThreshold = 100
            trackInfo = self.sp.current_user_playing_track()
            if trackInfo:
                song = trackInfo['item']['name']
                artist = trackInfo['item']['artists'][0]['name']
                progress = float(trackInfo['progress_ms'])
                status = trackInfo['is_playing']
                print "Connetion: " + str(status)
                duration = float(trackInfo['item']['duration_ms'])
                percentage = str(int(progress/duration*100))
            else:
                return None
        except spotipy.client.SpotifyException:
            self.fixMyError(self.tokenExpiration,self.getTrackInfo)
            return None


        return {'song' : song, 'artist' : artist, 'progress' : percentage, 'status' : status}


    def fixMyError(self,error,functionToRetry,arg=None,arg1=None):
        if (self.retryThreshold >= 0):
            if (error == self.tokenExpiration):
                self.token = util.prompt_for_user_token(self.username, self.scopes)
                self.sp = spotipy.Spotify(auth=self.token)
                print "Token expired re-auth"
            elif (error == self.badGateway):
                print "Bad gateway retrying func"
            else:
                print "Unhandled error"
            if (arg and not arg1):
                functionToRetry(arg)
            elif (arg and arg1):
                functionToRetry(arg,arg1)
            else:
                functionToRetry()
            self.retryThreshold -= 1

