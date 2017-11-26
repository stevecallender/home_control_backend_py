#!/bin/sh

#music playing
#mopidy &
#sleep 30
#python python_workspace/home_control_backend_py/MediaPlayer.py &
#amixer sset 'Master' 50% &


#home control
#python python_workspace/home_control_backend_py/TimeMonitor.py &
#sleep 10
python python_workspace/home_control_backend_py/PlugDriver.py &
#sleep 10
#python python_workspace/home_control_backend_py/HomeController.py &
#sleep 10
#python python_workspace/home_control_backend_py/NetworkMonitor.py &

#node
#cd HAP-NodeJS
#sudo rm -rf perist
#sudo node Core.js
