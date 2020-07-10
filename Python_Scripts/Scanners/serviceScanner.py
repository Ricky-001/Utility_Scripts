#!/usr/bin/python3

# ADVANCE PORT SCANNER
# USAGE :-
# portScan_Adv.PY -H <TARGET_HOST> -P <TARGET_PORTS>[COMMA SEPARATED LIST]

# SCANS FOR ALL THE PORTS MENTIONED IN THE <TARGET_PORTS>
# OF A HOST PROVIDED BY THE USER



from socket import * 			# socket handles the port scan and connect functions
import optparse as op			# handles all the -h -o <OPTION> command line option parsing used in the Linux environment
from threading import *			# handles threads to speed up operations
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal



# PERFORMS SIMPLE SCAN OF 1 PORT OF A HOST AT A TIME
# USING CONNECTION REQUEST TO THE SPECIFIED PORT




def retBanner(tHost, tPort):

	try:
		setdefaulttimeout(1)
		sock = socket()
		sock.connect((tHost,tPort))
		ban = sock.recv(1024)		
		return ban
	except:
		return




def startScan(host):
	
	try:
		ip = gethostbyname(host)
	except:
		print("Unknown host " + str(host))
	
	try:
		name = gethostbyaddr(ip)
		print("Scan results for " + str(name[0]) + ":-\n\n\tPORT\t\tSTATE\tSERVICE\n")
	except Exception as e:
		print(e)
		print("Scan results for " + str(ip) + ":-\n\n\tPORT\t\tSTATE\tSERVICE\n")

	for port in range (1,100001):
		ban = retBanner(ip,port)
		if ban:
			print(colored("[+] " + str(ip) + "/" + str(port) + "\tOpen\t" + str(ban), "green"))



		
def main():	

	host = input("[*] Enter target hostname : ")
	
	startScan(host)
	
main()

