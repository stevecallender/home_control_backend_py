
import subprocess
import time
import sys
import spotipy
import spotipy.util as util



class SpotifyConnection():

	def __init__(self):
		self.scopes = 'user-library-read user-modify-playback-state user-read-playback-state'
        self.stevensEchoId = 'f9acccf475ffa3ab406c14e1d01de50768dc4ccc'
        self.username =  "Flatpi"
        self.token = util.prompt_for_user_token(self.username, self.scopes)

        if self.token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            print "Initialising connection failed can't get token for", username
        
        
        
    def play(self):
        sp.start_playback(device_id=self.stevensEchoId)
   


#results = sp.current_user_saved_tracks()
#            for item in results['items']:
#                track = item['track']
#                print track['name'] + ' - ' + track['artists'][0]['name']
#            user = sp.user(username)
#            print(user)
#            print sp.devices()
#            sp.start_playback(device_id=)


   
