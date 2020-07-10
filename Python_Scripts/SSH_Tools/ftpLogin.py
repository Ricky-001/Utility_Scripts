#!/usr/bin/python3

# SCRIPT THAT AUTOMATES THE SSH LOGIN TO A GIVEN TARGET
# AND EXECUTES A SET OF COMMANDS [NON-INTERACTIVE]

from termcolor import colored	# use colored text output on the terminal
import ftplib 


def anoLogin(host,usr,pwd):
	
	try:
		ftp = ftplib.FTP(host)

		# for anonymous login
#		ftp.login('anonymous', 'anonymous')
		
		# for user defined login credentials
		ftp.login(usr, pwd)
		
		print(colored("[+] " + host + " FTP login successful!", "green"))
	except:
		print(colored("[-] " + host + " FTP login failed!", "red"))




# STARTS THE PROGRAM
# TAKES INPUT FOR THE BASIC FIELDS
# REQUIRED TO CARRY OUT THE ATTACK AUTOMATICALLY
# INVOKES connect() FUNCTION TO CONNECT 
# AND send_command() FUNCTION TO EXECUTE THE (NON-INTERACTIVE) COMMAND

def main():
	
	host = input("[*] Enter the host IP of the target : ")
	user = input("[*] Enter target username : ")
	password = input("[*] Enter target password : ")
	
	anoLogin(host, user, password)

	
main()
