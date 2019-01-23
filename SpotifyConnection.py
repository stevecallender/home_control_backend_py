
import subprocess
import time
import sys
import spotipy
import spotipy.util as util
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def lookup(k, d):
    if k in d: return d[k]
    for v in d.values():
        if isinstance(v, dict):
            a = lookup(k, v)
            if a is not None: return a
    return None

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
        playlistResult = self.playLists[playlistName]
        self.sp.start_playback(device_id=self.stevensEchoId, context_uri=playlistResult, uris=None, offset=None)

    def play(self):
        self.sp.start_playback(device_id=self.stevensEchoId)

    def pause(self):
        self.sp.pause_playback(device_id=self.stevensEchoId)

    def getTrackInfo(self):
        try:
            trackInfo = self.sp.current_user_playing_track()
        except spotipy.client.SpotifyException:
            self.token = util.prompt_for_user_token(self.username, self.scopes)
            self.sp = spotipy.Spotify(auth=self.token)
            trackInfo = self.sp.current_user_playing_track()

        progress = lookup('progress_ms',trackInfo)
        duration = lookup('duration_ms',trackInfo)
        progress = {'song' : 'test', 'artist' : 'testArtist', 'progress' : '100'}
        #artist   = lookup('name',lookup('artists',trackInfo))
        #song
        return progress


#results = sp.current_user_saved_tracks()
#            for item in results['items']:
#                track = item['track']
#                print track['name'] + ' - ' + track['artists'][0]['name']
#            user = sp.user(username)
#            print(user)
#            print sp.devices()
#            sp.start_playback(device_id=)



