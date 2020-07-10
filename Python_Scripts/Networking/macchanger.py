#!/usr/bin/python3

																							# PROGRAM TO SIMULATE THE ACTUAL WORKING OF
																							# MACCHANGER UTILITY TO CHANGE MAC ADDRESSES
																							# FOR THE INTERFACE SPECIFIED

						# NOTE:-
	# IF NO MAC ADDRESS IS SPECIFIED DURING SCRIPT EXECUTION,
	# THE SCRIPT INVOKES THE SYSTEM UTILITY macchanger
	# TO ASSIGN A RANDOM MAC ADDRESS TO THE SPECIFIED INTERFACE
	# THIS FEATURE CREATES A DEPENDENCY ON THE macchanger UTILITY
	# TO FUNCTION PROPERLY

																							# !!! RUN THIS SCRIPT AS ROOT !!!
																							# ifconfig AND RELATED COMMANDS DO NOT WORK
																							# ON NON ROOT ACCOUNTS IN NEWER VERSIONS
																							# OF LINUX / UNIX TYPE SYSTEMS
																							

import subprocess				# handles command line interactions 
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal




# THIS FUNCTION CARRIES OUT THE FOLLOWING
# COMMAND LINE COMMANDS TO CHANGE THE MAC ADDRESS 
# OF THE SPECIFIED DEVICE OR INTERFACE :-

# ifconfig <INTERFACE> down
# ifconfig <INT> hw ether <NEW_MAC>
# ifconfig <INTERFACE> up

# ARGS :- 
# (str <interface> , str <NEW_MAC_ADDR>)

def macChanger(iface, mac):

	subprocess.call(["ifconfig",iface,"down"])
	subprocess.call(["ifconfig",iface,"hw","ether",mac])
	subprocess.call(["ifconfig",iface,"up"])
	


# TAKES IN THE SCRIPT CALL ALONG WITH 2 REQUIRED ARGUMENTS
# FIRST ONE BEING NAME OF THE INTERFACE
# SECOND ONE IS THE NEW MAC ADDRESS IN ITS PROPER FORMAT

def main():

	if (len(sys.argv) < 2) or (len(sys.argv) > 3):																					# required no. of arguments are not passed along with the script to function
		print(colored("[!] Usage: macchanger.py <INTERFACE> <NEW_MAC_ADDRESS>(optional)", "red"))
		print("[!] If <NEW_MAC_ADDRESS> is not passed, a random MAC address will be assigned\n(Requires macchanger utility to be installed)")
		quit()

	try:
		org_ifConf = subprocess.check_output(["ifconfig",sys.argv[1]]).decode()													# result of ifconfig command before trying to change MAC address	
	except:
		print(colored("[-] Failed to change MAC address to " + sys.argv[2], "red"))
		quit()	
	
	if len(sys.argv) == 2:																										# if only interface name is given, macchanger utility is called to assign a random MAC
		subprocess.call(["macchanger","-r",sys.argv[1]])
		quit()
	else:																														# if interface and new MAC are given, call our macChanger() function
		macChanger(sys.argv[1], sys.argv[2])																					# macChanger() function is called to change the MAC 

	cng_ifConf = subprocess.check_output(["ifconfig",sys.argv[1]]).decode()														# ifconfig result after trying to change MAC

#	print(org_ifConf)	# CAN BE UNCOMMENTED AND USED FOR DEBUGGING PURPOSES
#	print(cng_ifConf)	# OTHERWISE NOT NECESSARY
	
	if org_ifConf == cng_ifConf:																								# if the 2 ifconfig results are same, that means MAC could not be changed
		print(colored("[-] Failed to change MAC address to " + sys.argv[2], "red"))
	else:
		print(colored("[+] MAC address successfully changed to " + sys.argv[2] + " on interface " + sys.argv[1], "green"))
	
main()
