#!/usr/bin/python3

import socket as sc
import os,sys
import struct
from termcolor import colored
import binascii as bs



sock_created = False
sniffer_sock = 0



def analyse_udp(data):

	udp_head = struct.unpack('!4H', data[:8])
	src_port = udp_head[0]
	dst_port = udp_head[1]
	length = udp_head[2]
	chk = udp_head[3]
	Data = data[8:]
	
	print("\n__________UDP HEADER__________")
	print("[+] Source Port : " + str(src_port))
	print("[+] Destination Port : " + str(dst_port))
	print("[+] Length : " + str(length))
	print("[+] Checksum : " + str(chk))
	
	return Data	



def analyse_tcp(data):

	tcp_head = struct.unpack('!2H2I4H', data[:20])
	src_port = tcp_head[0]
	dst_port = tcp_head[1]
	seq_num = tcp_head[2]
	ack_num = tcp_head[3]
	data_offset = tcp_head[4] >> 12
	reserved = (tcp_head[4] >> 6) & 0x03ff
	flags = tcp_head[4] & 0x003f
	window = tcp_head[5]
	checksum = tcp_head[6]
	urg_pointer = tcp_head[7]
	Data = data[20:]
	
	urg = bool(flags & 0x0020)
	ack = bool(flags & 0x0010)
	psh = bool(flags & 0x0008)
	rst = bool(flags & 0x0004)
	syn = bool(flags & 0x0002)
	fin = bool(flags & 0x0001)
	
	print("\n__________TCP HEADER__________")
	print("[+] Source Port : " + str(src_port))
	print("[+] Destination Port : " + str(dst_port))
	print("[+] Sequence Number : " + str(seq_num))
	print("[+] Acknowledgement Number : " + str(ack_num))
	print("[*] Flags:-")
	print("[+] URG: " + str(urg) + "\t[+] ACK: " + str(ack))
	print("[+] PSH: " + str(psh) + "\t[+] RST: " + str(rst))
	print("[+] SYN: " + str(syn) + "\t[+] FIN: " + str(fin))
	print("[+] Window Size : " + str(window))
	print("[+] Checksum : " + str(checksum))
	
	return Data




def analyse_ip_head(data):

	ip_head = struct.unpack('!6H4s4s', data[:20])												# first split contains the version, ihl and type of service
	ver = ip_head[0] >> 12 																		# get the first split from the ip_head and shift it by 12 bytes to get the version field
	ihl = (ip_head[0] >> 8) & 0x0f																# get the first split from the ip_head and shift it by 8 bytes to get the ihl field & strip off preceeding and trailing bytes
	tos = ip_head[0] & 0x00ff																	# get the remaining part of first split from the ip_head to get the tos field & strip off preceeding and trailing bytes
	total_len = ip_head[1]																		# entire second part of the split
	ip_id = ip_head[2]																			# entire third part of the split
	flags = ip_head[3] >> 13																	# fourth part of the split shifted 13 bytes
	frag_offset = ip_head[3] & 0x1fff															# rest of the fourth part, stripped off of preceeding and trailing bytes
	ip_ttl = ip_head[4] >> 8																	# fifth part shifted 8 bytes
	ip_proto = ip_head[4] & 0x00ff																# rest of fifth part
	checksum = ip_head[5]																		# entire sixth split contains the checksum
	src_addr = sc.inet_ntoa(ip_head[6])															# source IP ; socket.inet_ntoa() converts the packed encoded IP address to its standard representation
	dst_addr = sc.inet_ntoa(ip_head[7])															# destination IP ; 						___________ same as above ____________
	Data = data[20:]
	
	print("\n__________IP HEADER__________")
	print("[+] Version : " + str(ver))
	print("[+] IHL : " + str(ihl))
	print("[+] Type of Service : " + str(tos))
	print("[+] Length : " + str(total_len))
	print("[+] ID : " + str(ip_id))
	print("[+] Flags : " + str(flags))
	print("[+] Offset : " + str(frag_offset))
	print("[+] Time to Live : " + str(ip_ttl))
	print("[+] Checksum : " + str(checksum))
	print("[+] Source IP Address : " + src_addr)
	print("[+] Destination IP Address : " + dst_addr)
	
	if ip_proto == 6:
		tcp_udp = "TCP"
	elif ip_proto == 17:
		tcp_udp = "UDP"
	else:
		tcp_udp = "OTHER"
	print("[+] IP Protocol: " + str(ip_proto) + "(" + tcp_udp + ")")
		
	return Data, tcp_udp



def analyse_ether_head(data):

	ip_bool = False
	
	eth_head = struct.unpack('!6s6sH', data[:14])
	dest_mac = bs.hexlify(eth_head[0]).decode()
	src_mac = bs.hexlify(eth_head[1]).decode()
	proto = eth_head[2] >> 8
	Data = data[14:]																			# first 14 bytes are stripped as the eth_head for extracting necessary info ; rest of the packet is the data transmitted
	
	print("__________ETHERNET HEADER__________")
	print("[+] Destination MAC = " + dest_mac[0:2] + ":" + dest_mac[2:4] + ":" + dest_mac[4:6] + ":" + dest_mac[6:8] + ":" + dest_mac[8:10] + ":" + dest_mac[10:12])
	print("[+] Source MAC = " + src_mac[0:2] + ":" + src_mac[2:4] + ":" + src_mac[4:6] + ":" + src_mac[6:8] + ":" + src_mac[8:10] + ":" + src_mac[10:12])
	print("[+] Protocol = " + str(proto))
	
	if proto == 0x08:
		ip_bool = True
	
	return data, ip_bool



def main():

	global sock_created
	global sniffer_sock
	
	if sock_created == False:
		sniffer_sock = sc.socket(sc.PF_PACKET, sc.SOCK_RAW, sc.htons(0x0003))
		sock_created = True
		
	data_recv = sniffer_sock.recv(2048)
	os.system("clear")
	print(colored("[!] Running the packet sniffer...\n\n", "green"))
	data_recv, ip_bool = analyse_ether_head(data_recv)
	print(data_recv)
	if ip_bool:
		data_recv, tcp_udp = analyse_ip_head(data_recv)
		print(data_recv)
	else:
		return
		
	if tcp_udp == "TCP":
		data_recv = analyse_tcp(data_recv)
	elif tcp_udp == "UDP":
		data_recv = analyse_udp(data_recv)
	else:
		return
	
while True:
	try:
		main()
	except KeyboardInterrupt:
		print(colored("[!] Stopping the packet sniffer...", "red"))
		quit()
