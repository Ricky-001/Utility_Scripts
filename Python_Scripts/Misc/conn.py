#!/usr/bin/python

import socket as sc

#ip = (raw_input('IP: '))
#port = int(raw_input('Port: '))

sock = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

try:
#	sock.connect((ip,port))
	sock.connect(('0.tcp.ngrok.io',18352))
	print 'Connection secceeded!'
except Exception as e:
	print e
	print 'Connection failed!'
