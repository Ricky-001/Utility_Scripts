#!/bin/bash

# This script resets the network card for regular use
# by turning off monitor mode and putting into managed mode
# and resetting the MAC address of the card to its original one

# Run this script as Root!!!

if [ $# != 1 ]
then
	echo "[-] Please specify one wireless interface to normalise"
else
	ifconfig $1 down
	iwconfig $1 mode managed	# Changed to managed mode (from monitor mode)
	sleep 1
	macchanger -p $1		# permanent (original) MAC address initiated
	ifconfig $1 up
	iwconfig $1 | grep Mode
	service network-manager restart	# network-manager is restarted for enabling regular use
fi
