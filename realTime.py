from Lights.strip_controller import ez_strip

import cv2
import numpy as np
import copy
import math
from time import sleep
import threading

#initialize lights
strip = ez_strip()
colors = []
running = True

last_r = 0
last_g = 0

current_r = 0
current_g = 0

TRAVEL_SPEED = 2

for i in range(strip.LED_COUNT):
	colors.append((0,0))

def lights():
	while running:
		for i in range(strip.LED_COUNT):
			strip.set_pixel(i, (colors[i][0], colors[i][1], 20))
		strip.update()
		sleep(0.005)

lights_thread = threading.Thread(target=lights)
lights_thread.start()

#initialize video and buffers
vid = cv2.VideoCapture(0)

initialized = False
last = np.zeros((0,0))

ret, init_frame = vid.read()
IM_WIDTH = init_frame.shape[0]
IM_HEIGHT = init_frame.shape[1]

while(True):
	try:
		ret, frame = vid.read()
		
		if not ret:
			continue
		
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		if not initialized:
			last = copy.copy(frame)
			initialized = True
			continue
		
		processed = cv2.absdiff(frame, last)
		_, processed = cv2.threshold(processed, 140, 255, cv2.THRESH_BINARY)
		
		#find contours (AKA the wand tip)
		contours, hierarchy = cv2.findContours(processed, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
		
		if len(contours) != 0:
			max_contour = max(contours, key=cv2.contourArea)
			x,y,w,h = cv2.boundingRect(max_contour)

			last_r = int((y / IM_WIDTH) * 255)
			last_g = int((x / IM_HEIGHT) * 255)
		
		dist = math.sqrt(pow(last_r - current_r, 2) + pow(last_g - current_g, 2))
		if dist != 0:
			current_r += ((last_r-int(current_r)) / dist) * TRAVEL_SPEED
			current_g += ((last_g-int(current_g)) / dist) * TRAVEL_SPEED
		
		colors.insert(0, (int(current_r), int(current_g)))
		#colors.insert(0, (last_r, last_g))
		colors.pop(len(colors)-1)
		
		last = copy.copy(frame)
		
		cv2.waitKey(1)
	except KeyboardInterrupt:
		break

#clean up	
vid.release()

running = False
lights_thread.join()
strip.off()
