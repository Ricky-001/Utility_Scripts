#!/usr/bin/python3

# SCRIPT THAT AUTOMATES THE SSH LOGIN TO A GIVEN TARGET
# AND EXECUTES A SET OF COMMANDS [NON-INTERACTIVE]

import pexpect					# this module handles prompts and interactive behaviour in the target shell
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal


# LIST OF ITEMS THAT SPECIFY COMMAND LINE IS ACTIVE TO TAKE COMMANDS
PROMPT = ['# ' , '>>> ' , '> ' , '$ ' , '\$ ' , '/$ ']



# connect() FUNCTION HANDLES THE CONNECTION 
# TO THE HOST MACHINE AND TRIES TO LOGIN
# AND EFFECTIVELY PASS THE INTERACTIVE PROMPTS

def connect(host, user, pwd):
	
	ssh_newkey = 'Are you sure you want to continue connecting'					# expects this prompt (this prompt comes up while trying to login to a ssh remote host for the first time)
	connStr = "ssh " + user + "@" + host										# ssh username@host_ip 
	
	child = pexpect.spawn (connStr)												# spawns the connStr on the host to try and activate the login procedure
	ret = child.expect ([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])		# expects a prompt for the ssh_newkey or a password field
	
	if ret == 0:																# no such prompt occurs - something is wrong
		print(colored("[-] Error connecting!", "red"))
		return
	if ret == 1:																# ssh_newkey prompted - send response 'yes'
		child.sendline("yes")
		ret = child.expect ([pexpect.TIMEOUT, '{P|p}assword: '])				# now expect password
		
		if ret == 0:															# nothing prompted - connection failed
			print(colored("[-] Error connecting!", "red"))
			return
			
	try:
		child.sendline (pwd)														# directly send the password
		child.expect (PROMPT)														# expect shell prompt
		return child		
	except:																			# incorrect password
		print(colored("[-] Error connecting!\n[!] Incorrect Username or Password!", "red"))
		exit()




# THIS FUNCTION WORKS TO PASS THE COMMANDS 
# TO THE COMMAND LINE INTERFACE  

def send_command(conn, command):
	
	conn.sendline(command)					# connector sends the command
	conn.expect(PROMPT)						# expects next prompt (commandline default character)
	print((conn.before).decode())			# default decode type is utf-8
	


# STARTS THE PROGRAM
# TAKES INPUT FOR THE BASIC FIELDS
# REQUIRED TO CARRY OUT THE ATTACK AUTOMATICALLY
# INVOKES connect() FUNCTION TO CONNECT 
# AND send_command() FUNCTION TO EXECUTE THE (NON-INTERACTIVE) COMMAND

def main():
	
	host = input("[*] Enter the host IP of the target : ")
	user = input("[*] Enter target username : ")
	pwd = input("[*] Enter the SSH password : ")
	command = input("[*] Enter the predefined command (set) that the script will try to execute : ")
	
	child = connect(host, user, pwd)
	
	send_command (child, command)
	
main()
