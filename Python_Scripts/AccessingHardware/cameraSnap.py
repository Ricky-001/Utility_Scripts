#!/usr/bin/python

import cv2
import os

def imgCapture():		

	img_capture = cv2.VideoCapture(0)
	img_counter = 1
	print('Space\t:\tCapture Image\nESC\t:\tClose')
	while True:
		ret, frame = img_capture.read()
		cv2.imshow("Camera feed", frame)									# this shows the current frames of the machine - disable if not required		
						
		# check to close the program
		if cv2.waitKey(1)%256 == 27:										# ESC Key
		    # ESC pressed
			print("Escape hit, closing...")
			break
		
		# check to capture photo
		elif cv2.waitKey(1)%256 == 32:										# Spacebar Key
			# SPACE pressed
					
			try:
				img_path = os.environ["appdata"] + "\\Image_{}.png".format(img_counter)
			except:
				img_path = os.environ["HOME"] + "/Image_{}.png".format(img_counter)
			
			# saving the image frame to file
			cv2.imwrite(img_path, frame)
			print("{} saved".format(img_path))
			img_counter += 1		

	img_capture.release()

imgCapture()
