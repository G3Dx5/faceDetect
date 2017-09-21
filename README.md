# faceDetect
## Python script for detecting human faces from webcam or similar connected camera

Script using the opencv framework for utilising webcams or other similarly connected devices to identify faces in video.  When faces are identified a photograph is taken and saved to the 'pics' folder.  If the folder does not already exist it is created.  Images are saved with a time date stamp of the system time when the image is taken.  

The project utilises haar cascasses to identify facial features and when a face is identified on live view bounding boxes appear and an image is taken according to delay period set at hte top of the script.  

Version 0.3.  

The current version will evolve to include more features over time.  However out of the box it provides a useful way to capture images from live and pre-recorded video. 

Based on the excellent tutorial by Sentdex (https://pythonprogramming.net/).

## Example Usage: 

./faceDetect.py

## Licence:

MIT Licence

GaDayas 2017 
