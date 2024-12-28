from rpi_ws281x import *
import time
import random

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

r = 0.0
g = 125.0
b = 255.0

rUp = True
gUp = True
bUp = True

roc = 0.1
rocM = 0.3

def run(strip):
	global r, g, b, rUp, gUp, bUp, roc, rocM

		#red
	if rUp:
		r+=roc
		if r>255:
			r-=random.uniform(roc, rocM)
			rUp = False
	else:
		r-=roc
		if r<0:
			r+=random.uniform(roc, rocM)
			rUp = True

	#green
	if gUp:
		g+=roc
		if g>255:
			g-=random.uniform(roc, rocM)
			gUp = False
	else:
		g-=roc
		if g<0:
			g+=random.uniform(roc, rocM)
			gUp = True

	#blue
	if bUp:
		b+=roc
		if b>255:
			b-=random.uniform(roc, rocM)
			bUp = False
	else:
		b-=roc
		if b<0:
			b+=random.uniform(roc, rocM)
			bUp = True
			
	for x in range(0, LED_COUNT):
		strip.setPixelColor(x, Color(int(r), int(g), int(b)))

	strip.show()
	
if __name__ == '__main__':
	while True:
		strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
		strip.begin()
		run(strip)
