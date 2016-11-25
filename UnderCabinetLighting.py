#!/usr/bin/python

import time
from dotstar import Adafruit_DotStar
import sys
import RPi.GPIO as GPIO
from Adafruit_IO import Client

numpixels = 46 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapin   = 10
clockpin  = 11
strip     = Adafruit_DotStar(numpixels, datapin, clockpin)

# Adafruit.IO userid etc
ADAFRUIT_IO_KEY      = '<insert key here>'
ADAFRUIT_IO_USERNAME = '<insert username here>'

FEED_ID = '<insert feed name here>'

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

cOne  = 0              # Index of first 'on' pixel
cTwo  = -10            # Index of last 'off' pixel
cThree= -20
cFour = -30

red   = 0xFF0000
black = 0x000000
green = 0x00FF00
white = 0xFFFFFF
blue  = 0x0000FF
colorScooter = 1
rainbowCounter1 = 4
rainbowCounter2 = 3
rainbowCounter3 = 2
rainbowCounter4 = 1
rainbowCounter5 = 0

oldDataValue="none"
adaIoCheckerCounter = 0
data=aio.receive(FEED_ID)

while True:  # Loop forever
    if(data.value!=oldDataValue):
        i = 0
        for i in range(0,45):
            strip.setPixelColor(i, black)
            ++i
        strip.show()                        # Refresh strip
        oldDataValue = data.value
    if(oldDataValue=="Off"):
        for i in range(0,45):
            strip.setPixelColor(i, black)
            ++i
        strip.show()
    elif(oldDataValue=="Christmas"):
        i=0
        for i in range(0,45):
            if(i>=0 and i<10):    color=red
            elif(i>=10 and i<20): color=green
            elif(i>=20 and i<30): color=red
            elif(i>=30 and i<40): color=green
            else: color=red
            strip.setPixelColor(((i + colorScooter) % 46), color)
            ++i
        strip.show()
    elif(oldDataValue=="July4"):
        i=0
        for i in range(0,45):
            if(i>=0 and i<10):    color=red
            elif(i>=10 and i<20): color=white
            elif(i>=20 and i<30): color=blue
            elif(i>=30 and i<40): color=red
            else: color=white
            strip.setPixelColor(((i + colorScooter) % 46), color)
            ++i
        strip.show()
    elif(oldDataValue=="Rainbow"):
        i=0
        for i in range(0,45):
            if(i>=0 and i<10):    color=colorWheel(rainbowCounter1)
            elif(i>=10 and i<20): color=colorWheel(rainbowCounter2)
            elif(i>=20 and i<30): color=colorWheel(rainbowCounter3)
            elif(i>=30 and i<40): color=colorWheel(rainbowCounter4)
            else: color=colorWheel(rainbowCounter5)
            strip.setPixelColor(((i + colorScooter) % 46), color)
            ++i
        ++rainbowCounter1
        ++rainbowCounter2
        ++rainbowCounter3
        ++rainbowCounter4
        ++rainbowCounter5
        if(rainbowCounter1 > 255): rainbowCounter1 = 0
        if(rainbowCounter2 > 255): rainbowCounter2 = 0
        if(rainbowCounter3 > 255): rainbowCounter3 = 0
        if(rainbowCounter4 > 255): rainbowCounter4 = 0
        if(rainbowCounter5 > 255): rainbowCounter5 = 0
        strip.show()            
    time.sleep(1.0 / 50)                    # Pause 20 milliseconds
    ++adaIoCheckerCounter
    if(adaIoCheckerCounter >= 1000):        #Check for new programming once every 20 seconds
        data=aio.receive(FEED_ID)
        
        
def colorWheel(WheelPos):
    WheelPos = 255 - WheelPos;
    if(WheelPos < 85):
        return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3)
    if(WheelPos < 170):
        WheelPos -= 85
        return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3)
    else:
        WheelPos -= 170
        return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0)
