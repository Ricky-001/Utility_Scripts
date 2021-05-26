#!/usr/bin/python3

# MULTIPLE PORT SCANNER
# SCANS FOR ALL 1000 ports ON A GIVEN HOST IP ADDRESS
# AND REPORTS BACK THE STATES OF EACH PORT

# SYNTAX :-
# ./portScanner.PY <TARGET_IP>



import socket as soc	# socket handles the port scan and connect functions
import sys		# sys (system) module is used to handle the command line arguments
from termcolor import colored

sock = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
soc.setdefaulttimeout(3)

#host = "10.0.2.15"
#port = 443

if len(sys.argv) == 1:	# nothing is given
	host = input("[*] Enter the host IP address : ")
		
else:						# required arguments provided
	host = str(sys.argv[1])		# takes in the first argument (after the name of script) as HOST IP

def PortScanner(port):
	
	if sock.connect_ex((host, port)):				# if connection request throws an exception
		print (colored("[-] Port %d is closed" % (port), "red"))		# connection failed
	else:											
		print (colored("[+] Port %d is open" % (port), "green"))		# connection successful

for port in range (1,1001):
	PortScanner(port)		# call the function to execute the required commands

