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

def init(stripOne):
	for x in range(0, LED_COUNT):
		stripOne.setPixelColor(x, Color(0, 0, 0))

	stripOne.show()

def run(strip):
	speed = 0.07
	
	time.sleep(speed)

	r = random.randrange(0,255)
	g = random.randrange(0,255)
	b = random.randrange(0,255)

	pixel = random.randrange(0, LED_COUNT)

	strip.setPixelColor(pixel, Color(r,g,b))
	strip.show()

if __name__ == "__main__":
	stripOne = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	stripOne.begin()
	init(stripOne)
	while True:
		run(stripOne)
