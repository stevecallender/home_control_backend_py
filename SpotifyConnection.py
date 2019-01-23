
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
        self.stevensEchoId = 'f9acccf475ffa3ab406c14e1d01de50768dc4ccc'
        self.username =  "Flatpi"
        self.token = util.prompt_for_user_token(self.username, self.scopes)
        self.playLists = {}

        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            print "Initialising connection failed can't get token for", username
        self.populatePlaylists()

    def populatePlaylists(self):
        playlists = self.sp.user_playlists(self.username)['items']
        for pl in playlists:
            self.playLists[pl['name']] = pl['uri']

    def playPlaylist(self,playlistName):
        self.sp.shuffle(True, device_id=self.stevensEchoId)
        playlistResult = self.playLists[playlistName]
        self.sp.start_playback(device_id=self.stevensEchoId, context_uri=playlistResult, uris=None, offset=None)

    def play(self):
        self.sp.start_playback(device_id=self.stevensEchoId)

    def pause(self):
        print "Pausing"
        self.sp.pause_playback(device_id=self.stevensEchoId)

    def getTrackInfo(self):
        try:
            trackInfo = self.sp.current_user_playing_track()
        except spotipy.client.SpotifyException:
            self.token = util.prompt_for_user_token(self.username, self.scopes)
            self.sp = spotipy.Spotify(auth=self.token)
            trackInfo = self.sp.current_user_playing_track()

        song = trackInfo['item']['name']
        artist = trackInfo['item']['artists'][0]['name']
        progress = float(trackInfo['progress_ms'])
        duration = float(trackInfo['item']['duration_ms'])
        percentage = str(int(progress/duration*100))
        return {'song' : song, 'artist' : artist, 'progress' : percentage}




