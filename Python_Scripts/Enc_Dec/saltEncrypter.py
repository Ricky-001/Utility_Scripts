#!/usr/bin/python3

import hashlib
import crypt
from urllib.request import urlopen 
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal


word = input("[*] Enter word to encrypt with salt : ")
salt = input("[*] Enter the salt (2 letters) : ")
cryptWord = crypt.crypt(word,salt)

print("[+] The encrypted word is : " + cryptWord)
