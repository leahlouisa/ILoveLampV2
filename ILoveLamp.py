# Basic lamp control for my living room lamp

import sys
import RPi.GPIO as GPIO
from Adafruit_IO import Client
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
First_LED = 17

ADAFRUIT_IO_KEY      = '<insert key here>'
ADAFRUIT_IO_USERNAME = '<insert username here>'

FEED_ID = '<insert feed name here>'

GPIO.setup(First_LED, GPIO.OUT)
GPIO.output(First_LED, False)
time.sleep(2)

aio = Client(ADAFRUIT_IO_KEY)

while True:
    data=aio.receive(FEED_ID)
    #print('Received value: {0}'.format(data.value))
    if(data.value=="Off"):
        GPIO.output(First_LED, False)
    else:
        GPIO.output(First_LED, True)
    time.sleep(20)
