#!/usr/bin/python3

import hashlib
from urllib.request import urlopen 
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal

hashVal = input("[*] Enter the SHA1 hash value : ")

passList = urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt").read().decode()

#print(passList)

for password in passList.split('\n'):
	
	hashguess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
	if hashguess == hashVal:
		print(colored("[+] Password found : " + password, "green"))
		quit()

print(colored("[-!] Password not found in password list!", "red"))
