# encoding: utf-8

import zmq
from thread import *
from Queue import *
import time
from samplebase import SampleBase
from rgbmatrix import graphics
from Seizing import *
import math

class LEDControl(SampleBase,Seizer):

    def initDraw(self,canvas):
        self.artistX = 2
        self.songX = 2
        self.timeX = 2
        self.dateX = 2
        self.artistY = canvas.height - 12
        self.songY = canvas.height - 2
        self.dateY = canvas.height - 4
        self.timeY = 11

        self.mediaColor = graphics.Color(239, 133, 33)
        self.timeColor = graphics.Color(113, 12, 214) 
        self.minColor = graphics.Color(102, 178, 255) 
        self.maxColor = graphics.Color(255, 102, 102) 
        self.currentColor = graphics.Color(113, 12, 214) 
        self.dateColor = graphics.Color(42, 142, 44) 
	

    def drawLightIndicator(self, canvas):
        if self.lightStatus:
           for x in range(0, canvas.width):
              if (x < 3 or x > canvas.width -4):
                 canvas.SetPixel(x, 0, 255, 255, 255)
                 canvas.SetPixel(x, canvas.height - 1, 255, 255, 255)


    def drawProgress(self, canvas):
	try:
		progressInt = int(self.progress)
        except:
		progressInt = 0
	progressLength = canvas.width * (progressInt/100.0)
        for x in range(0, int(progressLength)):
           canvas.SetPixel(x, canvas.height-1, 80, 30, 0)

    def drawSeperator(self, drawBoth, canvas):
        for y in range(3, (canvas.height/2) -5):
           canvas.SetPixel(canvas.width - 28, y, 20, 60, 120)
        
        if (drawBoth):
           for x in range(4, canvas.width - 4):
              canvas.SetPixel(x, canvas.height/2,20, 60, 120)

    def drawTime(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/helvR12.bdf")
        graphics.DrawText(canvas, font, self.timeX, self.timeY, self.timeColor, self.timeText)

    def drawDate(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/5x8.bdf")
        graphics.DrawText(canvas, font, self.dateX, self.dateY, self.dateColor, self.dateText)

    def monthConverter(self,dateString):
        index = int(dateString)
        months = ["January","February","March","April","May","June","July","August","Sept","October","Nov","Dec"]
        return months[index-1]

    def dayConverter(self,dayString):
        day = int(dayString)
        if (day == 1 or day == 21 or day == 31):
            return dayString + "st"
        if (day == 2 or day == 22):
            return dayString + "nd"
        if (day == 3 or day == 23):
            return dayString + "rd"        
        return dayString + "th"

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
        if (len(weather)>3):
           weather = weather.split(".")[0]
        weather += "c"
        x = 40
        y = 11
        graphics.DrawText(canvas, font, x, y, color, weather)


    def drawMedia(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/5x8.bdf")
        lenArtist   = graphics.DrawText(canvas, font, self.artistX, self.artistY, self.mediaColor, self.artistText)
        lenSong   = graphics.DrawText(canvas, font, self.songX, self.songY, self.mediaColor, self.songText)
        if lenSong > 60:
            self.songX -= 1
            if (self.songX + lenSong < 0):
                self.songX = canvas.width
        else: #this ought to be moved to a seperate operation and songX and artistX renamed
            self.songX = 2
            self.artistX = 2

    def drawRecipe(self,canvas):
        font = graphics.Font()
        font.LoadFont("../fonts/5x8.bdf")
        recipeText = self.recipeList[self.recipeIndex]
        graphics.DrawText(canvas, font, self.artistX, self.artistY, self.mediaColor, "Dinner?")
        if (self.cycleDisplayThreshold <= 1):
            self.recipeIndex+=1
            if (self.recipeIndex >= len(self.recipeList)):
                self.recipeIndex = 0
        lenSong = graphics.DrawText(canvas, font, self.songX, self.songY, self.mediaColor, recipeText)
        if lenSong > 60:
            self.songX -= 1
            if (self.songX + lenSong < 0):
                self.songX = canvas.width
        else:
            self.songX = 2
            self.artistX = 2

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        self.initDraw(canvas)
        initialise = True
        while (True):
            elementsReceived = (self.weatherReceived and self.timeReceived)
            if (elementsReceived):
               canvas.Clear()
               self.drawTime(canvas)
               self.drawWeather(canvas)
               if (self.mediaStatus):
                  self.drawMedia(canvas)
                  self.drawProgress(canvas)
               else:   
                  self.drawDate(canvas)
               self.drawSeperator(not self.mediaStatus,canvas)
               self.drawLightIndicator(canvas)
            else:
               self.runLoadingScreen(initialise,canvas)
            time.sleep(0.005)
            canvas = self.matrix.SwapOnVSync(canvas) 
            self.cycleDisplayThreshold -= 1
            initialise = False

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
			print message
			self.handleTimeUpdate(message)
		time.sleep(0.5)

    def monitorWeatherQueue(self):
	while(True):
		if (not self.weatherQueue.empty()):
			message = self.weatherQueue.get_nowait()
			self.handleWeatherUpdate(message)
		time.sleep(0.5)

    def handleMediaUpdate(self, message):
        self.mediaStatus = (message != "")
	self.mediaStatus = (message != self.prevMessage) 
        self.prevMessage = message
        
        try:
	    songAndArtist,self.progress = message.split("::")
            if (songAndArtist == ""):
               self.progress = "0"
               self.songText = ""
            else:
               self.artistX = 2
               self.songX = 2
               splitArray = songAndArtist.split("-")
               artist = splitArray[0]
               song = splitArray[-1]
               self.songText = (song[1:])#removing last char as it is new line
               self.artistText = (artist)
        except:#catches exception if split fails
            self.songText = message[1:]
        self.songText = self.songText.decode('utf-8')
        self.artistText = self.artistText.decode('utf-8')
    
    def handleLightsUpdate(self, message):
        self.lightStatus = (message == "allOn")


    def handleTimeUpdate(self, message):
        splitTime = message.split(":")
        hours = splitTime[0]
        minutes = splitTime[1]
        day = self.dayConverter(splitTime[2])
        month = self.monthConverter(splitTime[3])
        if len(minutes) < 2:
            minutes = "0"+minutes
        if len(hours) < 2:
            hours = "0"+hours
        self.timeText = (hours+":"+minutes)
        self.dateText = (day+" "+month)
        self.timeReceived = True

    def handleWeatherUpdate(self,message):
        splitWeather = message.split(",")
        self.minTemp = splitWeather[1]
        self.maxTemp = splitWeather[2]
        self.currentTemp = splitWeather[0]
        self.weatherReceived = True

    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    def scale_col(self, val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    def runLoadingScreen(self,initialise,canvas):
        if (initialise):
           self.cent_x = self.matrix.width / 2
           self.cent_y = self.matrix.height / 2

           rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
           self.min_rotate = self.cent_x - rotate_square / 2
           self.max_rotate = self.cent_x + rotate_square / 2

           display_square = min(self.matrix.width, self.matrix.height) * 0.7
           self.min_display = self.cent_x - display_square / 2
           self.max_display = self.cent_x + display_square / 2

           self.deg_to_rad = 2 * 3.14159265 / 360
           self.rotation = 0        

        self.rotation += 1
        self.rotation %= 360

        for x in range(int(self.min_rotate), int(self.max_rotate)):
           for y in range(int(self.min_rotate), int(self.max_rotate)):
              ret = self.rotate(x - self.cent_x, y - self.cent_x, self.deg_to_rad * self.rotation)
              rot_x = ret["new_x"]
              rot_y = ret["new_y"]

              if x >= self.min_display and x < self.max_display and y >= self.min_display and y < self.max_display:
                 canvas.SetPixel(rot_x + self.cent_x, rot_y + self.cent_y, self.scale_col(x, self.min_display, self.max_display), 255 - self.scale_col(y, self.min_display, self.max_display), self.scale_col(y, self.min_display, self.max_display))
              else:
                 canvas.SetPixel(rot_x + self.cent_x, rot_y + self.cent_y, 0, 0, 0)



    def __init__(self):

        interestedIdentifiers = ["TimeValue","MediaInfo","LightsCommand","WeatherInfo"]
        super(LEDControl,self).__init__()
        self.configureSeizer(interestedIdentifiers,True)

        self.songText = ""
        self.artistText = ""
        self.lightStatus = False
        self.mediaStatus = False
        self.timeText = ""
        self.dateText = ""
        self.minTemp = ""
        self.maxTemp = ""
        self.currentTemp = ""
	self.progress = "0"
	self.cycleDisplayThreshold = 60
        self.recipeIndex = 0
        self.recipeList = ["Quiche","Risotto","Soup","Prawn Pasta","Stew","Lasagne","Pasta Bake","Pulled Pork","Baked Potato","Sweet & Sour Chicken","Spag bol","Quorn and Chips","Chicken Teriyaki","Feta courgettes","Mac 'n' Cheese","Blackened Chicken","Chickpeas","Fajitas"]
        self.prevMessage = ""

        self.weatherReceived = False
        self.timeReceived = False

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

