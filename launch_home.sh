#!/bin/sh

#home control

export SPOTIPY_CLIENT_ID='1f805d75e5ab462180b4416107973369'
export SPOTIPY_CLIENT_SECRET='368d4efe759b43febb2df6ca9a2432a3'
export SPOTIPY_REDIRECT_URI='http://localhost/'

if screen -ls; then
   echo "Screens alread running"
else


   screen -S Time -dm python /home/pi/python_workspace/home_control_backend_py/TimeMonitor.py
   screen -S Weather -dm python /home/pi/python_workspace/home_control_backend_py/WeatherMonitor.py
   screen -S Home -dm python /home/pi/python_workspace/home_control_backend_py/HomeController.py
   screen -S Network -dm python /home/pi/python_workspace/home_control_backend_py/NetworkMonitor.py
   screen -S Spotify -dm python /home/pi/python_workspace/home_control_backend_py/SpotifyController.py

   sudo rm -rf /home/pi/HAP-NodeJS/persist
   cd /home/pi/HAP-NodeJS

   screen -S Node -dm sudo node /home/pi/HAP-NodeJS/Core.js

fi

