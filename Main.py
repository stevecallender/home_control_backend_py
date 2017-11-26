# encoding: utf-8

import zmq
from thread import *
from Queue import *
import time
from samplebase import SampleBase
from rgbmatrix import graphics
from Seizing import *

class LEDControl(SampleBase,Seizer):

    def initDraw(self,canvas):
        self.artistX = 2
        self.songX = 2
        self.artistY = canvas.height - 12
        self.songY = canvas.height - 2
        self.mediaColor = graphics.Color(232, 81, 0)
        self.timeColor = graphics.Color(113, 12, 214) 
        self.minColor = graphics.Color(102, 178, 255) 
        self.maxColor = graphics.Color(255, 102, 102) 
        self.currentColor = graphics.Color(113, 12, 214) 
	

    def drawLightIndicator(self, canvas):
        if self.lightStatus:
           for x in range(0, canvas.width):
              if (x < 3 or x > canvas.width -4):
                 canvas.SetPixel(x, 0, 255, 255, 255)
                 canvas.SetPixel(x, canvas.height - 1, 255, 255, 255)

    def drawTime(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/helvR12.bdf")
        x = 2
        y = 11
        graphics.DrawText(canvas, font, x, y, self.timeColor, self.timeText)

    def drawWeather(self,canvas):
	weather = self.currentTemp
	color = self.currentColor
	if (self.cycleDisplayThreshold <= 0):
		self.cycleDisplayThreshold = 60
	elif (self.cycleDisplayThreshold <= 20):
		weather = self.maxTemp
		color = self.maxColor
	elif (self.cycleDisplayThreshold <= 40):
		weather = self.minTemp
		color = self.minColor

        font = graphics.Font()
        font.LoadFont("../fonts/helvR12.bdf")
        weather = weather[:3]
        weather += "c"
        x = 40
        y = 11
        graphics.DrawText(canvas, font, x, y, color, weather)


    def drawMedia(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/5x8.bdf")
        lenArtist = graphics.DrawText(canvas, font, self.artistX, self.artistY, self.mediaColor, self.artistText)
        lenSong = graphics.DrawText(canvas, font, self.songX, self.songY, self.mediaColor, self.songText)        
        if lenSong > 60:
            self.songX -= 1
            if (self.songX + lenSong < 0):
                self.songX = canvas.width

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        self.initDraw(canvas)
        while (True):
            canvas.Clear()
            self.drawTime(canvas)
            self.drawMedia(canvas)
            self.drawLightIndicator(canvas)
            self.drawWeather(canvas)
            time.sleep(0.005)
            canvas = self.matrix.SwapOnVSync(canvas) 
            self.cycleDisplayThreshold -= 1


    def monitorInBound(self):
        while True:
            [header, payload] = self.seize(True)
            if header == "TimeValue":
                self.timeQueue.put(payload)
            elif header == "MediaInfo":
                self.mediaQueue.put(payload)
            elif header == "LightsCommand":
                self.lightsQueue.put(payload)
            elif header == "WeatherInfo":
                self.weatherQueue.put(payload)
	time.sleep(0.005)

    def monitorMediaQueue(self):
        while (True):
            if (not self.mediaQueue.empty()):
                message = self.mediaQueue.get_nowait()
                self.handleMediaUpdate(message)
        time.sleep(0.5)

    def monitorLightsQueue(self):
        while (True):
            if (not self.lightsQueue.empty()):
                message = self.lightsQueue.get_nowait()
                self.handleLightsUpdate(message)
        time.sleep(0.5)

    def monitorTimeQueue(self):
        while(True):
            if (not self.timeQueue.empty()):
                message = self.timeQueue.get_nowait()
                self.handleTimeUpdate(message)
        time.sleep(0.5)

    def monitorWeatherQueue(self):
        while(True):
            if (not self.weatherQueue.empty()):
                message = self.weatherQueue.get_nowait()
                self.handleWeatherUpdate(message)
        time.sleep(0.5)

    def handleMediaUpdate(self, message):
        trimmedPayload = message[:-1]
        if (message == ""):
            self.songText = "Media Currently Paused"
        try:
            artist,song = trimmedPayload.split("-")
            self.songText = (song[1:])#removing last char as it is new line
            self.artistText = (artist)
        except:#catches exception if split fails
            self.songText = trimmedPayload[1:]

    
    def handleLightsUpdate(self, message):
        self.lightStatus = (message == "allOn")


    def handleTimeUpdate(self, message):
        splitTime = message.split(":")
        hours = splitTime[0]
        minutes = splitTime[1]
        if len(minutes) < 2:
            minutes = "0"+minutes
        if len(hours) < 2:
            hours = "0"+hours
        self.timeText = (hours+":"+minutes)


    def handleWeatherUpdate(self,message):
        splitWeather = message.split(",")
        self.minTemp = splitWeather[1]
        self.maxTemp = splitWeather[2]
        self.currentTemp = splitWeather[0]

    def __init__(self):

        interestedIdentifiers = ["TimeValue","MediaInfo","LightsCommand","WeatherInfo"]
        super(LEDControl,self).__init__()
        self.configureSeizer(interestedIdentifiers,True)

        self.songText = "Media Currently Paused"
        self.artistText = ""
        self.lightStatus = False
        self.timeText = ""
        self.minTemp = ""
        self.maxTemp = ""
        self.currentTemp = ""
	self.cycleDisplayThreshold = 60
        self.mediaQueue = Queue()
        self.timeQueue = Queue()
        self.lightsQueue = Queue()
	self.weatherQueue = Queue()
        self.outboundMessageQueue = Queue()
        self.inboundMessageQueue = Queue()

        start_new_thread(self.monitorInBound,())
        start_new_thread(self.monitorTimeQueue,())
        start_new_thread(self.monitorMediaQueue,())
        start_new_thread(self.monitorLightsQueue,())
        start_new_thread(self.monitorWeatherQueue,())

if __name__ == "__main__":
    control = LEDControl()
    control.process()
    control.run()

