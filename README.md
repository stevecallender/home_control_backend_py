# home_control_backend_py


In order to connect the pi to bluetooth it is necessary to set the sink to be the bluetooth. However, this will only work after the bluetooth has been connected.

Connect to bluetooth device and then run this command pacmd "set-default-sink bluez_sink.FC_58_FA_6C_42_43"


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
sudo pip install pyzmq
