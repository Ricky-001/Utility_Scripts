#!/usr/bin/python

import cv2
import os


def captureVideo():
	
	#Capture video from webcam
	vid_capture = cv2.VideoCapture(0)
	vid_cod = cv2.VideoWriter_fourcc(*'XVID')

	try:
		vid_path = os.environ["appdata"] + "\\VideoCapture.mp4"
	except:
		vid_path = os.environ["HOME"] + "/VideoCapture.mp4"


	output = cv2.VideoWriter(vid_path, vid_cod, 20.0, (640,480))
	print('Starting recording video from primary camera.')
	print('Press X to stop recording.')
	
	while not (cv2.waitKey(1) & 0xFF == ord('x')):
		# Capture each frame of webcam video
		ret,frame = vid_capture.read()
		cv2.imshow("Video feed", frame)								# this shows the current frames of the machine - disable if not required
		output.write(frame)
		
	# close the already opened camera
	vid_capture.release()
	# close the already opened file
	output.release()
	# close the window and de-allocate any associated memory usage
	cv2.destroyAllWindows()
	
captureVideo()
