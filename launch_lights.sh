#!/bin/sh

#home control

if screen -ls; then
   echo "Screens alread running"
else
   screen -S Lights -dm python /home/pi/python_workspace/home_control_backend_py/PlugDriver.py
   screen -S Alexa -dm python /home/pi/python_workspace/home_control_backend_py/AlexaConnection.py
fi

