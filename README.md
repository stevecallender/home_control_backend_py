# home_control_backend_py


In order to connect the pi to bluetooth it is necessary to set the sink to be the bluetooth. However, this will only work after the bluetooth has been connected.

Connect to bluetooth device and then run this command pacmd "set-default-sink bluez_sink.FC_58_FA_6C_42_43"

For Energenie API see: https://gpiozero.readthedocs.io/en/stable/api_boards.html?highlight=energenie#energenie

Note if using the 3.5mm jack and want to adjust the volume via command line then run the following commands:
amixer scontrols
amixer sset 'Master' 50%

How to install ZeroMQ on Raspberry Pi

The following instructions should work on your Raspbian distribution. Please report any problem. :)

Packages

sudo apt-get install libtool pkg-config build-essential autoconf automake
libsodium

ZeroMQ builds against the Sodium library.

wget https://github.com/jedisct1/libsodium/releases/download/1.0.3/libsodium-1.0.3.tar.gz
tar -zxvf libsodium-1.0.3.tar.gz
cd libsodium-1.0.3/
./configure
make
sudo make install
ZeroMQ

wget http://download.zeromq.org/zeromq-4.1.3.tar.gz
tar -zxvf zeromq-4.1.3.tar.gz
cd zeromq-4.1.3/
./configure
make
sudo make install
sudo ldconfig
Optional bindinds

Python bindings: pyzmq

The pyzmq package requires python-dev to compile.

sudo apt-get install python-dev
sudo apt-get install python-pip
sudo pip install pyzmq


Installing HAP-NodeJS for Homekit support:

Follow instrutions on this guide
http://www.instructables.com/id/Raspberry-Pi-2-Homekit-from-zero-to-Hey-Siri/?ALLSTEPS

Further instruction in: https://drive.google.com/file/d/0B6GR9Hj5Ut61bDZlekRMNFdTVEE/view

This involves getting HAP-NodeJS from

git clone https://github.com/KhaosT/HAP-NodeJS.git

Additional npm packages required

sudo npm install node-persist
sudo npm install debug
sudo npm install mdns
sudo npm install fast-srp-hap
sudo npm install ed25519
sudo npm install buffer-shims
sudo npm install curve25519-n
sudo npm install ip

Note that its necessary to get the and install the latest node from this using wget:

https://nodejs.org/dist/v8.4.0/node-v8.4.0-linux-armv6l.tar.gz

tar -xvf node-v8.4.0-linux-armv7l.tar.gz
cd node-v8.4.0-linux-armv6l.tar.gz
sudo cp -R * /usr/local/

node -v and npm -v should return the correct version - 84

It may also be necessary to use npm rebuild --unsafe-perm=true

Currently we must place the python scripts inside the HAP-NodeJS directory and of course place Casting.py in there as well. Ideally these could be totally independent. 

Homebridge code : 031-45-154

Also need to update Casting.py to close connection properly when it destructs as right now i think there will be lots of open connections whenever it is used via home kit.

If iOS device does not find accessories then remove persists directory

Note that the python scripts have to be moved to the HAP-NodeJS directory and accessories updated to call them.


Mopidy

Mopidy can be installed using apt-get see the documentation:

https://docs.mopidy.com/en/latest/installation/debian/#debian-install

Also useful for testing sound on RPi is:

https://docs.mopidy.com/en/latest/installation/raspberrypi/#raspberrypi-installation

To run as a service use: sudo systemctl enable mopidy
And some useful service commands:
sudo systemctl start mopidy
sudo systemctl stop mopidy
sudo systemctl restart mopidy


MPC

Install with apt-get install mpc


DAC

Use this to set up DAC

curl https://get.pimoroni.com/phatdac | bash

More detail: https://learn.pimoroni.com/tutorial/phat/raspberry-pi-phat-dac-install


Weather info:

sudo pip install pyowm


Spotify Connect to allow playback via Echo

Spotipy repo used for this capability, see - https://spotipy.readthedocs.io/en/latest/#

Only gotchas are to ensure that the client id secret and callback uri are set up as system vars, then the call back uri needs added to the spotify dash - just use local host
