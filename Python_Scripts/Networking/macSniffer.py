#!/usr/bin/python3

# THIS PROGRAM FLOODS THE TARGET HOST 



from scapy.all import *
import socket as sc
from struct import *
from termcolor import colored	# use colored text output on the terminal



# UTILITY FUNCTION TO DECODE THE BYTE TYPE MAC ADDRESS
# INTO THEIR CORRESPONDING STRING VALUES
# TO MAKE IT HUMAN READABLE

def eth_addr(a):

	eth = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % ( ord(a[0]), ord(a[1]), ord(a[2]), ord(a[3]), ord(a[4]), ord(a[5]) )
	return eth



try:
	sock = sc.socket(sc.AF_PACKET, sc.SOCK_RAW, sc.ntohs(0x0003))					# AF_PACKET - manipulate packets at protocol lvl ; SOCK_RAW - work with raw packets ; ntohs(0x0003) - convert +ve int from network to host byte order
	
except:
	print(colored("[-] Error creating socket object!", "red"))
	quit()
	
try:	
	print(colored("[!] Starting the MAC Sniffer!", "green"))
	while True:
	
		pkt = sock.recvfrom(65535)								# receive the packets from all the ports upto 65535
		pkt = pkt[0]											# strip off the first part of the packet .. because it contains the Ether header which we need

		eth_len = 14											# length of the Ether header (can be directly passed to the following line)
		eth_head = pkt[:eth_len]								# pkt is stripped off to the first 14 bytes
	
		eth = unpack('!6s6sH', eth_head)						# unpacks the binary headers in the format - 6 bytes / 6 bytes / 2 bytes
		eth_pro = sc.ntohs(eth[2])								# result of the 3rd part (last split) from the above command
	
#		print("[+] Destination MAC = " + eth_addr(str(pkt[0:6])) + "\n[+] Source MAC = " + eth_addr(str(pkt[6:12])) + "\n[+] Protocol = " + str(eth_pro))
		print("[+] Destination MAC = " + eth_addr(str(eth[0])) + "\n[+] Source MAC = " + eth_addr(str(eth[1])) + "\n[+] Protocol = " + str(eth_pro))

except KeyboardInterrupt:
	print(colored("[!] Stopping the MAC Sniffer!", "red"))
	
	
