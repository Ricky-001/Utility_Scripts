#!/usr/bin/python3

# ADVANCED PORT SCANNER
# USAGE :-
# portScan_Adv.py -H <TARGET_HOST> -P <TARGET_PORTS>[COMMA SEPARATED LIST]

# SCANS FOR ALL THE PORTS MENTIONED IN THE <TARGET_PORTS>
# OF A HOST PROVIDED BY THE USER

# IF NO. OF PORTS IS NOT PROVIDED, SCANS FOR ALL POSSIBLE PORTS (UPTO 100,000)
# SCANNING IS SUPPOSED TO BE SLOW IN SUCH CASE



from socket import * 			# socket handles the port scan and connect functions
import optparse as op			# handles all the -h -o <OPTION> command line option parsing used in the Linux environment
from threading import *			# handles threads to speed up operations
import sys						# sys (system) module is used to handle the command line arguments
from termcolor import colored	# use colored text output on the terminal



# PERFORMS SIMPLE SCAN OF 1 PORT OF A HOST AT A TIME
# USING CONNECTION REQUEST TO THE SPECIFIED PORT



# Function to scan the ports using the connect() function
# scans one port at a time for a host
# args (str tHost , int tPort)

def Scan(tHost, tPort):
	
	try:													# tries to make a connection request
		sock = socket(AF_INET, SOCK_STREAM)					
		sock.connect((tHost, tPort))						# connect to the tPort of tHost
		print(colored("[+] %d/tcp\tOpen" %tPort, "green"))
	except:													# failed connection (port is closed)
		print (colored("[-] %d/tcp\tClosed" %tPort, "red"))

	finally:												# close the socket
		sock.close()



# This function is called to scan for all the ports (100,000)
# and not just the user specified ports
# Shows only the opne ports
# args (str tHost , int tPort)

def massScan(tHost, tPort):
	
	try:													# tries to make a connection request
		sock = socket(AF_INET, SOCK_STREAM)					
		sock.connect((tHost, tPort))						# connect to the tPort of tHost
		print(colored("[+] %d/tcp\tOpen" %tPort, "green"))
	except:													# failed connection (port is closed)
		pass

	finally:												# close the socket
		sock.close()




# INVOKED WHEN NO PORT IS SPECIFIED TO SCAN 		[ NO -P PARAMETER PASSED WHILE RUNNING THE SCRIPT]
# THIS FUNCTION SCANS FOR ALL (UP TO 100,000) PORTS
# AND INVOKES THE massScan() FUNCTION
# TAKES ONLY THE TARGET HOST AS A STRING ARGUMENT
# ALSO RESOLVES THE HOST TO ITS IP IF NEEDED

def AllPortScan(tHost):
	
	try:
		tIP = gethostbyname(tHost)						# try to resolve IP address from the given hostname
	except:
		print("Unknown host %s" %tHost)				# unable to resolve
		
	try:
		tName = gethostbyaddr(tIP)						# get host name from IP (generated above)
		print("[+] Scan results for " + tName[0] + "\n     PORT\tSTATE")
	except:												# unable to get host name, IP is shown
		print("[+] Scan results for " + tIP + "\n     PORT\tSTATE")
		
	setdefaulttimeout(5)			# default timeout to wait for n seconds before connection request is closed
	
	for tPort in range(1,100001):
		massScan(tHost,tPort)
		#t = Thread (target=Scan, args=(tHost, int(tPort)))		# create threads and call the Scan() function using args argument list
		#t.start()



# STARTS THE PORT SCANNING PROCESS AND CREATES n NO. OF THREADS
# WHERE n IS THE NO. OF PORTS ASSIGNED TO SCAN
# CALLS Scan() FOR EACH PORT NEEDS TO BE SCANNED
# TAKES ONLY THE TARGET HOST AS A STRING ARGUMENT
# ALSO RESOLVES THE HOST TO ITS IP IF NEEDED

def PortScan(tHost, tPorts):
	
	try:
		tIP = gethostbyname(tHost)					# try to resolve IP address from the given hostname
	except:
		print("Unknown host %s" %tHost)				# unable to resolve
		
	try:
		tName = gethostbyaddr(tIP)						# get host name from IP (generated above)
		print("[+] Scan results for " + tName[0] + "\n     PORT\tSTATE")
	except:												# unable to get host name, IP is shown
		print("[+] Scan results for " + tIP + "\n     PORT\tSTATE")
		
	setdefaulttimeout(5)			# default timeout to wait for n seconds before connection request is closed
	
	for tPort in tPorts:
		t = Thread (target=Scan, args=(tHost, int(tPort)))		# create threads and call the Scan() function using args argument list
		t.start()



# The main() function determines the looks and feel of the UI

def main():
	
	parser = op.OptionParser('Usage of program :- \n' + 'portScan_Adv.py -H <TARGET_HOST> -P(optional) <TARGET_PORTS>')					# show user how to use the program [syntax to use]
	parser.add_option('-H', dest='tHost', type='string', help='Specify target Host')						# adds option to the parser ('<TRIGGER>' , dest='VARIABLE_NAME' , type='VAR_TYPE' , help = 'SHOW HELP MESSAGE')
	parser.add_option('-P', dest='tPort', type='string', help='Specify target Ports [comma separated]')
	(options, args) = parser.parse_args()																	# parse arguments given through command line
	
	tHost = options.tHost						# defining the variables
	tPorts = str(options.tPort).split(',')		# simple string.split to separate comma separated input

	if (tHost == None) or ((len(sys.argv) < 5) and (len(sys.argv) != 3)):
		print(parser.usage)
		exit()
	elif (tPorts[0] == 'None'):
		AllPortScan(tHost)
	else:
		PortScan(tHost, tPorts)

if __name__ == '__main__':
	main()

