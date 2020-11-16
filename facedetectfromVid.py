#!/usr/bin/env python

import argparse
import cv2
import copy
import hashlib
import logging
import os
import time, datetime

'''
Function to take still images from supplied video file and output to folder 

The function takes the supplied video, opens the video file and draws bounding boxes around any faces on the live video.
If not previously created a folder for storage of the images is created in the nominated location.  Images are taken 
at the selected timing parameter and saved to the nominated folder.  Saved images do not include the bounding box. 
Tested and working on .mp4, .avi and .mov
:Example usage - python3 facedetectfromVid.py -f myvideo.mp4 -i 2 
:Deps - 2 haar-cascade files to assist in facial detection 
'''


parser = argparse.ArgumentParser(description='Extract faces from video file and save as jpg in marked folder.')
parser.add_argument("-f", "--input_file", 	help="Name of the input video file for analysis. Compatible with .mp4 and .avi")
parser.add_argument("-i", "--interval", 	help="Set face detection interval in seconds, 2 means a wait 2 seconds before \
											recording a new face")
args = parser.parse_args()
input_file = args.input_file
picDelay = args.interval

logging.basicConfig(filename='event.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

print("VIDEO ANALYSER: V 0.1")
print("Analysing video.....")

# SETUP PARAMETERS
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
picPrefix = "face_detected_" + "(" + input_file + ")"
capture = cv2.VideoCapture(input_file)

def get_video_hash(input_file):
    file_hash = hashlib.md5()
    with open(input_file, 'rb') as file:
        while True:
            chunk = file.read(file_hash.block_size)
            if not chunk:
                break
            file_hash.update(chunk)
    return file_hash.hexdigest()

logging.info("analysed video: " + input_file + " " + "File hash: " + get_video_hash(input_file))

def setPicPath():
	picPath = "detected faces - " + str(input_file)
	if picPath[-1] == "/":
		picPath = picPath[:-1]
	if not os.path.exists(picPath):
		os.makedirs(picPath)
	return picPath

def picSave(image):
	picPath = setPicPath()
	#time_string = time.strftime("%Y%m%d-%H%M%S")
	time_string = time.perf_counter()
	image_name = "%s/ %s %.3f.jpg" %(picPath, picPrefix, time_string)
	write_image = cv2.imwrite(image_name, image)	
	print("FACE DETECTED - SAVED TO FILE")

# ON LINUX SYSTEMS USE THE ONBOARD (LIVE) CAMERA
#image = cv2.imdecode(buff, 1)

def video_analysis():
	date_time = False
	while True:
		ret, video = capture.read()
		if not ret:
			break
		original = copy.deepcopy(video)
		gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			cv2.rectangle(video, (x,y), (x+w, y+h), (255,0,0), 1)
			roi_gray = gray[y:y+h, x:x+w] 
			roi_color = video[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,0,255), 1)

			numFaces = len(faces)
			if date_time:
				if date_time + datetime.timedelta(0, int(picDelay)) <= datetime.datetime.now():
					picSave(original)
					date_time = datetime.datetime.now()

			else:
				date_time = datetime.datetime.now()
				picSave(original)

		cv2.imshow("PROCESSING: " + input_file,video)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

        
if __name__ == "__main__":
	video_analysis()
