#!/usr/bin/python3



# THIS SCRIPT USES AN ONLINE RESOURCE OF A LARGE LIST OF PASSWORDS
# AND ENCRYPTS THEM WITH SPECIFIED HASHING ALGORITHMS 
# AND THEN MATCHES THE RESULT WITH THE HASH GIVEN BY THE USER
# IT RETURNS THE CORRESPONDING PASSWORD IN PLAIN TEXT FROM THE DICTIONARY
# WHOSE HASH VALUE MATCHES WITH THE USER INPUT

# IF THE USER DOESN'T KNOW THE TYPE OF HASH, 
# THE SCRIPT RUNS THROUGH ALL THE HASHING ALGORITHMS
# MD5, SHA1, SHA224, SHA256 AND SHA512
# AND RETURNS IF ANY HASH VALUE MATCHES ALONG WITH ITS TYPE



import hashlib
from urllib.request import urlopen 
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal




# crackAll() FUNCTION IS INVOKED WHEN THE USER
# DOESN'T KNOW THE TYPE OF HASH TO CRACK
# IT GOES THROUGH ALL THE TYPES OF HASHES 
# FOR EACH WORD IN THE DICTIONARY
# AND SEARCHES FOR A MATCH WITH THE USER INPUT

def crackAll(val):

	# passList is the dictionary of possible passwords read from the online location
	passList = urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read().decode()

	for password in passList.split('\n'):
	
		hashguess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
		if hashguess == val:
			print(colored("[!] Hash type : MD5", "yellow"))
			print(colored("[+] Password found : " + password, "green"))
			quit()

		hashguess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
		if hashguess == val:
			print(colored("[!] Hash type : SHA1", "yellow"))
			print(colored("[+] Password found : " + password, "green"))
			quit()

		hashguess = hashlib.sha224(bytes(password, 'utf-8')).hexdigest()
		if hashguess == val:
			print(colored("[!] Hash type : SHA224", "yellow"))
			print(colored("[+] Password found : " + password, "green"))
			quit()

		hashguess = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
		if hashguess == val:
			print(colored("[!] Hash type : SHA256", "yellow"))
			print(colored("[+] Password found : " + password, "green"))
			quit()

		hashguess = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()
		if hashguess == val:
			print(colored("[!] Hash type : SHA512", "yellow"))
			print(colored("[+] Password found : " + password, "green"))
			quit()

	print(colored("[-!] Password not found in password list!", "red"))
	quit()




# cracker() FUNCTION IS INVOKED WITH THE HASH VALUE TO BE CRACKED
# ALONG WITH ITS HASH TYPE (NEEDS TO BE KNOWN)
# IT ENCRYPTS THE DICTIONARY KEYS ACCORDING TO THE GIVEN HASH TYPE
# AND SEARCHES FOR A MATCH WITH THE HASH GIVEN BY THE USER

# IF HASH TYPE IS NOT KNOWN [htype = 0]
# THE FUNCTION CALLS THE crackAll() FUNCTION
# TO BRUTE FORCE THROUGH ALL THE HASH TYPES
# AND SEARCH FOR A MATCHING RESULT

# ARGS :-
# (int <type_of_hash> , str <HASH_VAL>)		# <type_of_hash> values are defined as in main()

def cracker (htype, hval):

	if htype == 0:																		# hash type not known by the user - call crackAll() function
		crackAll (hval)
	
	passList = urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read().decode()

	
	if htype == 1:																		# md5 hashtype
		for password in passList.split('\n'):
			hashguess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
			if hashguess == hval:
				print(colored("[+] Password found : " + password, "green"))
				quit()
		
	elif htype == 2:																	# sha1 hashtype
		for password in passList.split('\n'):
			hashguess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
			if hashguess == hval:
				print(colored("[+] Password found : " + password, "green"))
				quit()
			
	elif htype == 3:																	# sha224 hashtype
		for password in passList.split('\n'):
			hashguess = hashlib.sha224(bytes(password, 'utf-8')).hexdigest()
			if hashguess == hval:
				print(colored("[+] Password found : " + password, "green"))
				quit()
			
	elif htype == 4:																	# sha256 hashtype
		for password in passList.split('\n'):
			hashguess = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
			if hashguess == hval:
				print(colored("[+] Password found : " + password, "green"))
				quit()

	elif htype == 5:																	# sha512 hashtype
		for password in passList.split('\n'):
			hashguess = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()
			if hashguess == hval:
				print(colored("[+] Password found : " + password, "green"))
				quit()
		

	print(colored("[-!] Password not found in password list!", "red"))					# the hash value match is not found after all the iterations
	quit()


def main():
	
	hashtype = int(input("[*] Enter the type of hash (if known) :-\n(0) Unknown\t(1) MD5\n(2) SHA1\t(3) SHA224\n(4) SHA256\t(5) SHA512\nYour choice here: "))
	
	if hashtype == 0:
		hashVal = input("[*] Enter the hash value : ")
	elif hashtype == 1:
		hashVal = input("[*] Enter the MD5 hash value : ")
	elif hashtype == 2:
		hashVal = input("[*] Enter the SHA1 hash value : ")
	elif hashtype == 3:
		hashVal = input("[*] Enter the SHA224 hash value : ")
	elif hashtype == 4:
		hashVal = input("[*] Enter the SHA256 hash value : ")
	elif hashtype == 5:
		hashVal = input("[*] Enter the SHA512 hash value : ")
		
	cracker(hashtype, hashVal)
	
main()
