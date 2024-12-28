print("Loading model...")
from tensorflow.keras.models import load_model
model = load_model("SpellAI.h5")
model.trainable = False
print("Model loaded!")

from Lights.strip_controller import ez_strip
from Lights import spots, stars, waves, rainbowFade, wakeUpLights

import cv2
import numpy as np
import copy
import math
from time import sleep, time

import threading

#initialize lights
strip = ez_strip()
running = True
mode = "Solid"
lastMode = "Solid"
isOn = False

r = 10
g = 10
b = 10

def lights():
	global strip, r, g, b
	
	while running:
		if not isOn:
			strip.off()
			while not isOn:
				sleep(0.005)
		elif mode == "Waves":
			waves.run(strip.getStrip())
		elif mode == "Stars":
			stars.run(strip.getStrip())
		elif mode == "Spots":
			spots.run(strip.getStrip())
		elif mode == "Rainbow":
			rainbowFade.run(strip.getStrip())
		elif mode == "Bed":
			wakeUpLights.nightLight(strip.getStrip(), False)
		elif mode == "Custom":
			strip.set_color(r, g, b)
		elif mode == "Solid":
			strip.set_color(147, 34, 156)
			
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
draw_buf = np.zeros((0,0)).astype('uint8') #start buffer for drawing new shapes

def reset_draw_frame():
	global draw_buf
	draw_buf = np.zeros(init_frame.shape).astype('uint8') #start buffer for drawing new shapes

def distance(point1, point2):
	return math.sqrt(pow(point2[0]-point1[0], 2) + pow(point2[1] - point1[1], 2))

reset_draw_frame()
EMPTY_FRAMES_FOR_CLEAR = 9 #if the wand isn't visible for this many frames, clear the drawing / spell
MAX_FRAMES_PER_DRAW = 100
cutOff = False #if a spell is taking too long, the system will be cutoff from drawing anymore until movement has stopped
empty_frames_count = 0 #how many frames the wand isn't visible for
drawing = False #whether or not a spell is in progress (should be "casting" to sound cooler...)

drawn_frames = 0

#for interpolating
last_x = 0
last_y = 0

lastTime = time() #automatically turn off lights after set amount of time
TURN_OFF_TIME = 3600

print("Running!")
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
		_, processed = cv2.threshold(processed, 125, 255, cv2.THRESH_BINARY)
		
		#find contours (AKA the wand tip)
		contours, hierarchy = cv2.findContours(processed, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
		
		contourCount = len(contours)
		
		for c in contours:
			x,y,w,h = cv2.boundingRect(c)
			
			if w*h > 30: #making sure the contour is big enough
				contourCount-=1
				continue
			
			if drawing == False or distance((x, y), (last_x, last_y)) > 15: #if starting a new spell, don't interpolate from last x, y
				pass
				#cv2.circle(draw_buf, (x, y), radius=4, color=(255, 255, 255), thickness=-1)
			else:
				#interpolate between each point to get a more clear line
				cv2.line(draw_buf, (x, y), (last_x, last_y), (255, 255, 255), 4)
			
			#for interpolating
			last_x = x
			last_y = y
			
			empty_frames_count = 0
			drawing = True
		
		if drawing and contourCount == 0:
			empty_frames_count += 1
		elif drawing:
			drawn_frames += 1
			if drawn_frames >= MAX_FRAMES_PER_DRAW: #stop the system, restart the drawing
				drawing = False
				drawn_frames = 0
				empty_frames_count = 0
				reset_draw_frame()
		
		#if enough time elapsed since the last clear, automatically turn off the lights
		if time() - lastTime > TURN_OFF_TIME:
			isOn = False
		
		if empty_frames_count >= EMPTY_FRAMES_FOR_CLEAR and drawing:
			#search for spells
			draw_buf = cv2.cvtColor(draw_buf, cv2.COLOR_BGR2GRAY)
			draw_buf = cv2.flip(draw_buf, 1)
			contours, hierarchy = cv2.findContours(draw_buf, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
			
			#reset elapsed time regardless of whether spell is detected
			lastTime = time()
			
			#only check for spells if there is a contour and the user has drawn for at least a certain amount of frames
			if len(contours) != 0 and drawn_frames > 15:
				max_contour = max(contours, key=cv2.contourArea)
				x,y,w,h = cv2.boundingRect(max_contour)

				roi = draw_buf[y:y+h, x:x+w]
				
				#add padding to the roi
				pw = w + 5
				ph = h + 5
				if w > h: #if the width is greater than the hight, expand the height
					ph += w-h
				else: #vise versa
					pw += h-w
					
				center_x = (pw - w) // 2
				center_y = (ph - h) // 2
				
				#add the image to the padded buffer
				padding = np.zeros((pw, ph))
				padding[center_y:center_y+h, center_x:center_x+w] = roi
				roi = padding
				
				roi = cv2.resize(roi, (90, 90), cv2.INTER_AREA)
				cv2.imshow("processed", roi)
				roi = np.reshape(roi, (1, 90, 90, 1))

				pred = model.predict(roi, verbose=0)[0]
				res = pred.argmax()
				
				if res == 6 and pred[pred.argmax()] > .97:
					mode = "Solid"
					isOn = True
				elif res == 5:
					isOn = False
				elif res == 9:
					mode = "Waves"
				elif res == 10:
					mode = "Stars"
				elif res == 4:
					mode = "Rainbow"
				elif res == 12:
					mode = "Spots"
				elif res == 0:
					mode = "Bed"
				elif res == 2:
					mode = "Custom"
				elif res == 1:
					mode = "Custom"
					r += 5
					if r > 255:
						r = 5
				elif res == 3:
					mode = "Custom"
					g += 5
					if g > 255:
						g = 5
				elif res == 11:
					mode = "Custom"
					b += 5
					if b > 255:
						b = 5
				elif res == 8:
					mode = "Custom"
					r = 10
					g = 10
					b = 10
				elif res == 7:
					mode = "Solid"
				
				if mode != lastMode:
					strip.off() #reset the frame
				lastMode = mode
			
			#clear the draw frame
			drawing = False
			reset_draw_frame()
			empty_frames_count = 0
			drawn_frames = 0
		
		#cv2.imshow('Frame', test)
		#cv2.imshow('Processed', processed)
		#cv2.imshow('Drawing', cv2.flip(draw_buf, 1))
		last = copy.copy(frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	except KeyboardInterrupt:
		break

#clean up	
vid.release()
cv2.destroyAllWindows()

running = False
isOn = True
lights_thread.join()
strip.off()
