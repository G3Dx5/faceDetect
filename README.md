# faceDetect
## Python script for detecting human faces from webcam or similar connected camera

EXTRACT FACIAL IMAGES FROM VIDEO FILES (DETECTION)

Version 0.1 October 2020.

Python program to extract human faces detected from a supplied video file. Utilises opencv for facial detection  
Tested successfully with .mp4, .avi and .mov files

Produces: 

- Folder created named faces_detected (video file name) elapsed time of image in video file 
- Images taken of faces in folder with video file name based on the time interval set by user, saved with date of image taken
- Log of dates / times of execution of the program (event.log) with hash of the video file

Requirements (non standard):  
- opencv library 
- 2 haar cascade files for facial detection

Example usage:  

python3 facedetectfromVid.py -f myvideo.avi -i 2

## Licence:

MIT Licence

GaDayas 2020 
