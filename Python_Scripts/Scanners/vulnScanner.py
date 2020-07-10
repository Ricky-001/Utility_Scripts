#!/usr/bin/python3

# VULNERABILITY SCANNER
# USAGE :-
# vulnScanner.py <vuln_FILE>
# vuln_FILE is a text file 
# containing all the vulnerable banners 
# line by line

# SCANS FOR ALL THE PORTS MENTIONED IN THE <TARGET_PORTS>
# OF A HOST PROVIDED BY THE USER
# AND RETURNS ACTIVE SERVICES ON THE OPEN PORTS
# ALSO CHECKS FOR ANY VULNERABLE SERVICE AMONG THE ONES FOUND
# COMPARING FROM THE TEXT FILE vuln_FILE



from socket import * 			# socket handles the port scan and connect functions
import optparse as op			# handles all the -h -o <OPTION> command line option parsing used in the Linux environment
from threading import *			# handles threads to speed up operations
import sys						# sys (system) module is used to handle the command line arguments
import os						# handles file read write permission checking and access controls
from termcolor import colored	# use colored text output on the terminal



# PERFORMS SIMPLE SCAN OF 1 PORT OF A HOST AT A TIME
# USING CONNECTION REQUEST TO THE SPECIFIED PORT




# A simple function to connect to an open port and 
# try to get some message from the service
# running on that port

def retBanner(tHost, tPort):

	try:
		setdefaulttimeout(5)			# default timeout to wait for before connection is closed
		sock = socket()	
		sock.connect((tHost,tPort))		# connection request to specified port @ tHost host
		ban = sock.recv(1024)			# retrieve 1024 bytes of data from the open port	[banner retrieval]
		return ban						# banner is returned 
	except:			# if no banner is returned (or connection not established)
		return



# Function to resolve host names from 
# the given user input
# if ip is given, which can't be resolved into 
# a domain name, ip is used to show results

def hostResolv(host):

	try:
		ip = gethostbyname(host)									# retireve IP address from given hostname
	except:
		print("Unknown host " + str(host))							# if IP address not resolved successfully
		exit()
	
	try:
		name = gethostbyaddr(ip)									# reverse process of above - get back hostname from IP
		print("Scan results for " + str(name[0]) + ":-\n")			# if hostname found - show results for hostname
	except Exception as e:
		print(e)
		print("Scan results for " + str(ip) + ":-\n")				# if hostname not found - show results for IP




# Checks which banners are vulnerable 
# among the ones retrieved by retBanner()
# comparing the banners from a list of vulnerables
# from the file vuln_FILE

def checkVulns(banner, file):
	
	f = open (file, "rU")
	for line in f.readlines():
		if line.strip("\n") in str(banner):
			print("[+!] Server is vulnerable!\t" + str(banner).strip("\n"))
		


		
def main():	
	
	if (len(sys.argv) == 2):				# correct no. of arguments given - proceed for next checks
		file = sys.argv[1]
	
		if not os.path.isfile(file):		# incorrect file name (not a file)
			print(colored("[-] File : " + file + " doesn't exist!\nPlease check for any spelling errors.", "red"))
			exit()
		
		if not os.access(file, os.R_OK):	# not enough permission to access the specified file - permission denied
			print(colored("[-] Access denied for file : " + file + "\nDo you have the required permissions to access the file?", "red"))
			exit()
			
	else:									# incorrect no. of arguments given - show usage
		print(colored("[!] Usage : " + str(sys.argv[0]) + " <vuln_filename> ", "yellow"))
		exit()
	
	ip = input("[*] Enter target hostname/ IP : ")
	ports = input("[*] Enter ports to scan (comma separated) : ")
	hostResolv(ip)														# resolve host from input
	portList = ports.split(',')											# split ports to scan for, from a string input	
	
	for port in portList:
		ban = retBanner(ip, int(port))									# retBanner is called with arguments ; portList is list of strings ... port is a string .. casting it to corresponding int for proper functioning
		if ban:
			print(colored("[+] " + str(ip) + "/" + str(port) + " : " + ban.decode('ascii'), "green"))		# banner retrieved - print it
			checkVulns(ban,file)																# check the banner for vunerabilities
	
main()

