from rpi_ws281x import *
import time
import math
import random

red = True

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 125
LED_INVERT = False
LED_CHANNEL = 0

offSet = 0

rate = 5

def getCosValue(x):
	return int(255 * ((math.cos(x)+1)/2))
	
def getSinValue(x):
	return int(255 * ((math.sin(x)+1)/2))

def reset():
	global offSet
	offSet = 0

def run(strip):
	global offSet, rate
	
	for x in range(0, LED_COUNT):
		red = getCosValue((x/rate) + offSet)
		green = getSinValue(((LED_COUNT-x)/rate) + offSet)
		
		strip.setPixelColor(x, Color(red, green, 30))

	strip.show()
	
	offSet+=0.04

if __name__ == "__main__":
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	strip.begin()
	
	reset()
	while True:
		run(strip)
