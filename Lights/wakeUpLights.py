from rpi_ws281x import *
import time

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

startLight = 125
endLight = 231

def redLight(strip):
    for x in range(0, LED_COUNT):
        strip.setPixelColor(x, Color(255, 0, 0))
        
    strip.setBrightness(0) #Starting the brightness at zero and slowly fading in and out of full brightness
    
    for i in range(0, 255):
        strip.setBrightness(i)
        strip.show()
        
    for i in range(255, 0, -1):
        strip.setBrightness(i)
        strip.show()
    
    strip.setBrightness(255) #resetting the brightness for future use
    #resetting the strip to black
    for x in range(0, LED_COUNT):
        strip.setPixelColor(x, Color(0,0,0))

def nightLight(strip, warm=False):
    global startLight, endLight
    
    for x in range(startLight, endLight):
        if warm:
            strip.setPixelColor(x, Color(255, 206, 59))
        else:
            strip.setPixelColor(x, Color(0, 233, 255))
    
    strip.show()

def run():
    global startLight, endLight
    
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    for x in range(startLight, endLight):
        strip.setPixelColor(x, Color(255, 255, 255))
    strip.show()
    
    time.sleep(0.05)
    
    for x in range(startLight, endLight):
        strip.setPixelColor(x, Color(0, 0, 0))
    strip.show()
    
    time.sleep(0.05)

if __name__ == "__main__":
    while True:
        redLight()
