#!/usr/bin/python3

import socket as sc
import json
import os, sys
import base64
from optparse import OptionParser

ip = None
ports = None

usage = "Usage: %prog host [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--port", action="store", dest="port", help="Connect to the particular port")
parser.add_option("-t", "--top", action="store_true", dest="top", help="Scan top 1024 well-known ports", default=False)
parser.add_option("-f", "--fast", action="store_true", dest="fast", help="Scan common ports from the 1024 well-known ports (faster than '--top'", default=False)
parser.add_option("-a", "--all", action="store_true", dest="all", help="Default: Scan all 65535 ports (can be slow)", default=True)

(options, args) = parser.parse_args()

if len(args) != 1:
	if len(args) < 1:
		print('[!] Please provide a HOST address\n')
	parser.parse_args(['-h'])	

ip = args[0]

if options.top or options.fast or options.port:
	options.all = False

if options.all:
	ports = [x for x in range(65536)]

elif options.top:
	ports = [x for x in range(1025)]

elif options.fast:
	ports = [7,20,21,22,23,25,42,43,45,49,
			53,67,68,69,70,79,80,88,102,110,
			113,119,123,135,137,138,139,143,
			161,162,179,201,264,381,382,383,
			389,411,412,443,445,464,465,500,
			513,514,520,521,554,546,547,587,
			631,636,691,860,902,989,990,993,
			995,1025,1026,1027,1028,1029,1080,
			1194,1241,1433,1434,1701,1723,1725,
			1755,1863,2100,2222,2302,2483,2484,
			3074,3124,3128,3306,3689,5000,5432,
			6665,6666,6667,6668,6669,6881,6999,
			6891,6901,8000,8080,8086,8087,8200,
			8767,14567,27015,28960,8443,8053]

elif options.port:
	if len(options.port.strip('-').split('-')) >= 2:
		portL = int(options.port.strip('-').split('-')[0])
		portH = int(options.port.strip('-').split('-')[1])
		
		if portL > portH:
			portL, portH = portH, portL
		
		ports = [x for x in range(portL,portH+1)]
	else:
		ports = [int(options.port.strip('-'))]

def Recv():

	data = ""
	while True:
		try:
			data += sock.recv(1024)
		except ValueError:
			pass
		finally:
			return data


sock = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

for port in ports:
	sock = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
	sock.settimeout(3)
	try:
		sock.connect((ip,port))
		print('[+]', ip, ':', port, '\t-\tCONNECTED')
		data = Recv()
		print(data)
	except Exception as e:
		if options.port:
			print ('Port:',port,' - ',e)
		else:
			pass

