from rpi_ws281x import *
import time
import random

red = True

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 125
LED_INVERT = False
LED_CHANNEL = 0

createStarTime = 0.055
current_time = time.time()

starDecay = 0.8

#What color the rest of the channels should return to
star_channel_normal_value = 2

def reset(strip):
	for x in range(0, LED_COUNT):
		strip.setPixelColor(x, Color(2, 2, 50))


def run(strip):
	global createStarTime, current_time, starDecay, star_channel_normal_value
	
	#get current time and determine if a new star should be made
	if time.time() - current_time > createStarTime:
		current_time = time.time()
		randomPosition = random.randrange(0, LED_COUNT)
		
		randC = random.randrange(0,3)
		r = strip.getPixelColorRGB(randomPosition).r
		g = strip.getPixelColorRGB(randomPosition).g
		b = strip.getPixelColorRGB(randomPosition).b
		
		if randC == 0:
			r = random.randrange(2, 255)
		elif randC == 1:
			g = random.randrange(2, 255)
		else:
			b = random.randrange(50, 255)
		strip.setPixelColor(randomPosition, Color(r, g, b))
	
	
	#loop through the strip to see if any needs to be changed
	for x in range(0, LED_COUNT):
		pixelColor = strip.getPixelColorRGB(x)
		
		if pixelColor.r > star_channel_normal_value:
			setattr(pixelColor, 'r', pixelColor.r-starDecay)
			strip.setPixelColor(x, Color(int(pixelColor.r), int(pixelColor.g), int(pixelColor.b)))
		
		if pixelColor.g > star_channel_normal_value:
			setattr(pixelColor, 'g', pixelColor.g-starDecay)
			strip.setPixelColor(x, Color(int(pixelColor.r), int(pixelColor.g), int(pixelColor.b)))
			
		if pixelColor.b > 50:
			setattr(pixelColor, 'b', pixelColor.b-starDecay)
			strip.setPixelColor(x, Color(int(pixelColor.r), int(pixelColor.g), int(pixelColor.b)))

	
	#render
	strip.show()

if __name__ == "__main__":
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	strip.begin()
	
	reset(strip)
	
	while True:
		run(strip)
