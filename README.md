Author: x1x

Date: 10/04/14

Description: *** Incomplete project *** This program scans multiple IP addresses with nmap and pretty's up the output.

The user should put a list of target IPs in a text file;  this program then performs Nmap udp and syn scans of those IPs followed by pretty formatting of results which can more easily be integrated into a penetration test report.   The nmap scans run in parallel. The number of processes still running displays on the screen.  If a process or two is not completing, get the pid and kill it with:

sudo ps -A|grep nmap
kill -9 *pid*

Future:  Host discovery may be integrated into this script using tools such as fing.  It'll basically automate the generation of the target IP address file.

Format:

IP Address
999.999.999.999      Ports:  TCP 999,999...999 UDP 999,999,999...999
...
999.999.999.999      Ports:  TCP 999,999...999 UDP 999,999,999...999

Requirements:  Linux / Python

Instructions:  

1. Create a directory.
2. Download format.py to the directory.
3. Within the new directory, create a text file called, target_addresses.txt, containing the IP addresses to be scanned.
4. Ensure the current directory is this newly created directory.
5. Run the following command:  sudo python nmapformat.py
7. The resultant file is nmapformat.txt .

*** The project is incomplete / was just started on 10/4/14 but should be complete within a few days ***
