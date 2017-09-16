#!/usr/bin/env python

#############################################
# Date: 12APR2016                           #
# Author: Gabe. Github: GaDayas             #
# Version: 0.3                              #
#############################################

import cv2
import os
import copy
import time, datetime
# import numpy as np

#number of seconds between saving pictures
picDelay = 0.2

#path to save pics
picPath = "pics"

#filename prefix
picPrefix = "Face_detected_"

#remove / from end of picPath if present
if picPath[-1] == "/":
	picPath = picPath[:-1]

#make the path if it doesn't exist
if not os.path.exists(picPath):
	os.makedirs(picPath)

#create a function called picSave as splitting common "tasks" into functions allows you to write cleaner code
def picSave(pic):
	ts = time.strftime("%Y%m%d-%H%M%S")
	cv2.imwrite("%s/%s%s.jpg" %(picPath, picPrefix, ts), pic)
	print "**** Pic taken!****"

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

capture = cv2.VideoCapture(1)
#image = cv2.imdecode(buff, 1)

dt = False
while True:
	ret, img = capture.read()
	orig = copy.deepcopy(img)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

		numFaces = len(faces)
		if numFaces > 0:
			#use string formatting rather than string concatenation
			print "Found %d face(s)" % numFaces

			#if we have set dt before, check if picDelay seconds have elapsed and take pic
			if dt:
				if dt + datetime.timedelta(0, picDelay) <= datetime.datetime.now():
					picSave(orig)
					dt = datetime.datetime.now()
			#otherwise if it's false, set it and take a pic
			else:
				dt = datetime.datetime.now()
				picSave(orig)

	cv2.imshow('img',img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyALlWindows()
