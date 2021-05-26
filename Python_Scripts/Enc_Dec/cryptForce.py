#!/usr/bin/python3



# THIS SCRIPT IS USED TO DIG OUT PASSWORDS AND CREDENTIALS
# FROM A GIVEN LIST OF CREDENTIAL FILE [AS THE /etc/shadow]
# THE SCRIPT USES A PRE-DEFINED LIST OF PASSWORDS
# AND ENCRYPTS THEM WITH THE SAME SALT [WHICH NEEDS TO BE KNOWN]
# THEN MATCHES THE RESULTS WITH THOSE PICKED UP FROM THE 
# CREDENTIAL LIST

# IF THE VALUES MATCH, THAT IMPLIES THAT A PASSWORD IS FOUND
# AND THE CORRESPONDING USERNAME-PASSWORD CREDENTIAL PAIR
# IS RETURNED TO THE USER



import hashlib
import crypt
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal




def decrypt(pwd):
	
	salt = pwd[0:2]
	dic = open("passList.txt", "r")																			# password list used as a dictionary to match password crypts
	
	for word in dic.readlines():
		if crypt.crypt(word.strip(), salt) == pwd:
			print("[+] Password match found : " + word.strip())
			return word.strip()
		else:
			pass
	print(colored("[-] No Password found", "red"))


def main():
	flag = 0
	File = input("[*] Enter the complete path to the file containing the encrypted passwords : ")				# test file is credList.txt [line #6 #7 has matching passwords]
	passFile = open(File, "r")
	for line in passFile.readlines():
		usr = line.split(":")[0]
		pwd = line.split(":")[1].strip()
		print(colored("[!] Trying to crack password for " + usr, "white"))
		passwd = decrypt(pwd)
		if passwd:
			print(colored("[!] Found credentials -> " + usr + " : " + passwd, "green"))
			flag = 1
	if flag == 0:
		print(colored("[-] No credentials found in default dictionary!", "red"))
		
main()

