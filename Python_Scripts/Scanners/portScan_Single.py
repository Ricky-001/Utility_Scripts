#!/usr/bin/python3

# SIMPLE PORT SCANNER THAT 
# SCANS FOR A GIVEN PORT ON A GIVEN HOST IP ADDRESS
# AND REPORTS BACK WHETHER THE PORT IS OPEN OR NOT

# SYNTAX :-
# ./portScanner.PY <TARGET_IP> <PORT_TO_SCAN>



import socket as soc	# socket handles the port scan and connect functions
import sys		# sys (system) module is used to handle the command line arguments
from termcolor import colored

sock = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
soc.setdefaulttimeout(5)

#host = "10.0.2.15"
#port = 443

if len(sys.argv) < 3:		# syntax error by user (less than required no. of arguments provided)

	if len(sys.argv) == 1:	# nothing is given
		host = input("[*] Enter the host IP address : ")
		port = int(input("[*] Enter the host Port Number : "))
	else:
		print("Please call the script in the following format:-")
		print("portScan.py <TARGET_IP> <PORT_TO_SCAN>")
		exit()
		
else:						# required arguments provided
	host = str(sys.argv[1])		# takes in the first argument (after the name of script) as HOST IP
	port = int(sys.argv[2])		# takes in the second argument as PORT NO.

def PortScanner(port):
	
	if sock.connect_ex((host, port)):				# if connection request throws an exception
		print (colored ("[-] Port %d is closed" % (port), "red"))		# connection failed
	else:											
		print (colored ("[+] Port %d is open" % (port), "green"))			# connection successful
		
PortScanner(port)		# call the function to execute the required commands

