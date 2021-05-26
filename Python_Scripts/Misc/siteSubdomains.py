#!/usr/bin/python

import requests
from termcolor import colored

def request(url):

		try:
			requests.get("http://" + url)
		except requests.exceptions.ConnectionError:
			pass
		

page_url = raw_input("[*] Enter the complete URL of the target site: ")

file = open("common.txt", "r")
for line in file:
	try:
	
		word = line.strip()
		full_url = word + "." + page_url

		response = request(full_url)
		if response:
			print(colored("[+] Discovered existent subdomain at : " + full_url, "green"))

	except KeyboardInterrupt:
		print("[!] Stopping the script...")
		quit()
