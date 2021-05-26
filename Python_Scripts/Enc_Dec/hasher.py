#!/usr/bin/python3

import hashlib
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal



def main():
	
	orgStr = input("[*] Enter the string to hash: ")
	hashtype = int(input("[*] Enter the type of hash algorithm to use:-\n(1) MD5\t\t(2) SHA1\n(3) SHA224\t(4) SHA256\n(5) SHA512\t(0) All hashes\nYour choice here: "))

	if hashtype == 0:
		hobj1 = hashlib.md5()
		hobj2 = hashlib.sha1()
		hobj3 = hashlib.sha224()
		hobj4 = hashlib.sha256()
		hobj5 = hashlib.sha512()
		hobj1.update(orgStr.encode())
		hobj2.update(orgStr.encode())
		hobj3.update(orgStr.encode())
		hobj4.update(orgStr.encode())
		hobj5.update(orgStr.encode())
		
		print("MD5\t= " + hobj1.hexdigest())
		print("SHA1\t= " + hobj2.hexdigest())
		print("SHA224\t= " + hobj3.hexdigest())
		print("SHA256\t= " + hobj4.hexdigest())
		print("SHA512\t= " + hobj5.hexdigest())
		return
		exit(0)
		
	elif hashtype == 1:
		hashobj = hashlib.md5()
	elif hashtype == 2:
		hashobj = hashlib.sha1()
	elif hashtype == 3:
		hashobj = hashlib.sha224()
	elif hashtype == 4:
		hashobj = hashlib.sha256()
	elif hashtype == 5:
		hashobj = hashlib.sha512()
	hashobj.update(orgStr.encode())
	
	print(hashobj.hexdigest())
	
main()
