#!/bin/bash

# This script sets up the network card for attacks
# by enabling monitor mode and packet injection
# along with changing the MAC address of the network card

# Run this script as Root!!!

if [ $# != 1 ]
then
	echo "[-] Please specify one wireless interface to setup"
else
	ifconfig $1 down
	sleep 1
	iwconfig $1 mode managed	# MAC Changer doesn't work with monitor mode
	macchanger -A $1		# MAC address changed
	airmon-ng check kill		# kill potential processes that interferes with monitor mode
	iwconfig $1 mode monitor	# monitor mode enabled
	ifconfig $1 up
	iwconfig $1 | grep Mode		# Output of the network card mode
fi
