import subprocess
import os
import time
import errno
import array
import re
#
# Author: x1x
#
# Date: 10/04/14
#
# Description: Typically, a penetration test report will
# contain a list of active hosts and ports. In this instance,
# ports of types TCP and UDP will be listed if they are open.
# In addition, Open / Filtered UDP ports have their own
# section to be listed.
#
# A child process will be kicked off for each host being
# scanned, and they will all run in parallel.  Therefore,
# use caution.  Too many processes could cause big problems.
#
# Requirements: Linux OS / Python / nmap
#
# Instructions:
#
# 1. Create a directory.
# 2. Download nmapformat.py to the directory.
# 3. Create a text file called target_addresses.txt containing
# the IP addresses to be scanned, one IP per line.  It should 
# be in the same directory as nmapformat.py.
# 4. Ensure the current directory is this newly created 
# directory by typing pwd.
# 5. Run the following command: sudo python nmapformat.py
# It is necessary to run as superuser since a SYN scan flag
# requires it.
#
# As the program runs, it will display the number of nmap 
# scans still running and update it as processes complete. 
# Since a UDPscan is time-consuming, these processes will 
# take more than just a few seconds to complete. It could
# take half an hour.
#
# 6. The resultant file is final.txt .
#
# Details: This program will start nmap for each IP in the
# target_addresses.txt file. The flags for nmap are:                                                                                                                                                              
#
# -P0 : Host discovery is disabled to save time.
# -sS : Syn scan is optimal for determination of open TCP ports
# -sU : This lengthens the duration of the scan but is necessary
# for a complete penetration test report.
# -oG : This flag specifies an output file format which is
# easier to reformat to more easily integrate with the
# penetration test report.
#
# Please email me with recommendations for improvements.  I
# tailored this program to my specific needs but want to 
# eventually make it as widely useful as possible.
#
# Feel free to modify the source code on your system, such as
# adding and removing flags from the nmap system call.  
#
def process_exists(tst):
    """Check whether pid exists in the current process table."""
    retcode = tst.poll()
    if retcode is None:
       return True
    else:
       return False

#
# The debugf flag essentially displays trace messages to aid in 
# troubleshooting.  It must be 'yes' to show the messages.
#
debugf = 'no'

# All processes are stored in process_array just after they are started.
# This allows for checking if it is still running. We count the number
# of processes in the following variable.                                      
#
running_processes = 0
process_array = []
file = open('target_addresses.txt', 'r')

for line in file:
   filename='nmap'+str(line.strip())+'.txt'
   p = subprocess.Popen(["nmap", "-P0", "-sS", "-sU", "-oG",filename, str(line)],
   stdout=subprocess.PIPE)
   process_array.append(p);
   running_processes += 1

#
# Wait for all nmap processes started above to complete by counting the number of
# nmap processes which have completed and holding until they reach zero.  The array
# process_array contains information about all started processes.   
#
sv_running_processes = 0
                                                                               
while running_processes > 0:
  # Computer the number of processes by looking at all the processes stored in the process_array
  # structure.  The format of that object is defined in the subprocess module.
    running_processes = 0
    for s in process_array:    
        if process_exists(s):
           running_processes = running_processes + 1

    if sv_running_processes != running_processes:
  # If the number of running processes has changed, display the value on the screen.
       print 'Number of running Processes: '+str(running_processes)
       sv_running_processes = running_processes
  # Sleep for awhile so as not to waste too much system resources rechecking.
    time.sleep(5)

#
# All nmap processes are now complete and the results are stored as individual files for
# each IP.  To ease the reformatting process, they will now be recombined.  The resultant                                                                      
# file is called joined_file.txt .  
#
# The format of these files is nmap<ip_address>.txt .  
#
# Example:  nmap192.168.12.121.txt
#
# I pulled this bit of code from bufferoverflow.com .  It's simple and effective. I
# recommend it's reuse.
# 
filenames = os.listdir('.')
content = ''
for f in filenames:
    if f.startswith("nmap") and f.endswith(".txt"):
       content = content + '\n' + open(f).read()
       open('joined_file.txt','wb').write(content)
#
# The file called 'joined_file.txt' is bulk loaded into the array called
# line_work.  This is a good example I found on bufferoverflow.com of
# a really simple and effective file read into an array. All on one line!
#
line_work = [line.strip() for line in open('joined_file.txt')]                 

# This section limits our parsing only to lines with the word 'Port' in them.
# We will read the array called line_work, populated in the file read above,
# and place the results into the next array: lines.  
#
lines=[]
for r in line_work:
    if re.match("(.*)Port(.*)", r):
       lines.append(r)
       if debugf == 'y':
          print r

#
# The final product is stored in the file called final.txt .  We open
# that file before we read the lines to parse.
#
myfile = open('final.txt', 'w')
#
# One line at a time, we read the lines array and use string functions
# to build the record for final.txt .
#
for s in lines:                                                                
   line = s
   if debugf == 'y':
      print s

#  In the nmap output, each port has a set of fields, including
#  number (field 0) and type (field 2).  This is a working array
#  to be parsed to determine which port type array the port
#  number is to be stored.

   port_fields = []

# TCP port numbers are stored in this array as the line is parsed.

   tcp_ports = []

# UDP port numbers are stored in these arrays as the line is parsed.

   openfiltered_udp_ports = []
   open_udp_ports = []

#
# The IP address is parse and stored for later inclusion in the output
# file at the beginning of the line.  The key part of the search method
# is \(\).  The search string is actually looking for (), but the back-
# slash is necessary as an escape character.  Essentially, we are looking
# for (), which occurs on every line in the line array.  The rest of the 
# line, before and after (\(\)) means there can be a string of characters
# before or after the one for which we are searching.
#
   end_of_ip_address = re.search(r"[^a-zA-Z](\(\))[^a-zA-Z]", line).start()
   ip_addr = line[6:end_of_ip_address]

#
# The following code group strips off extraneous information from the
# left and right of the line, leaving only port information.
#
# Much of this code was derived from examples on bufferoverflow.com . I
# recommend it for learning and copying to reuse.
#

   port_pos = re.search(r"[^a-zA-Z](Ports: )[^a-zA-Z]", line).start()
   line_stripped_left = line[port_pos+8:]

   if debugf == 'y':
      print 'LSL: '+line_stripped_left

   if re.search(r"[^a-zA-Z](Ignored)[^a-zA-Z]",line_stripped_left) is not None:
      right_end_pos = re.search(r"[^a-zA-Z](Ignored)[^a-zA-Z]", line_stripped_left).start()
      line_stripped_lr = line_stripped_left[:right_end_pos-1]                  
   else:
      line_stripped_lr = line_stripped_left
   if debugf == 'y':
      print 'LSLR: '+line_stripped_lr
#
# The line has been stripped of extraneous information and only port information remains.
# Those fields are separated by a space, and can be easily stored in an array.
#

   ports = line_stripped_lr.split(" ")
   if debugf == 'y':
      print ports

#
# The port array populated above is now evaluated, one port at a time, and the UDP and
# TCP port arrays are populated along the way.
#

   for s in ports:
       port_fields_work = s                                                    
       port_fields = port_fields_work.split("/")
       if debugf == 'y':
          print port_fields
       if port_fields[2]=="tcp":
          tcp_ports.append(port_fields[0])
       if port_fields[2]=="udp" :
          if port_fields[1]=='open|filtered':
             openfiltered_udp_ports.append(port_fields[0])
          else:
             open_udp_ports.append(port_fields[0])
           
#
# We have all of the information necessary for the output line: The IP address, and
# TCP and UDP ports.  This code produces a line that has the following format:
#
# 999.999.999 TCP 9999, 9999...9999 UDP: 9999, 9999, .... 9999
#
# Example:
# 192.168.12.300 TCP 80, 8080, UDP: 123
#
# flags determine proper placement of commas and port type headers.            
#

   output_line = ip_addr
   firsttcp = 'yes'
   for t in tcp_ports:
      if firsttcp == 'yes':
         output_line = output_line+' TCP:'                                                                                                                                                                        
         firsttcp = 'no'
      else:
         output_line = output_line+', '
      output_line = output_line+" "+t.strip()

   firstudp = 'yes'
   for u in open_udp_ports:
      if firstudp == 'yes':
         output_line = output_line+' OPEN UDP: '
         firstudp = 'no'
      else:
         output_line = output_line+', '
      output_line = output_line+u.strip()+" "                                  

   firstudp = 'yes'
   for u in openfiltered_udp_ports:
      if firstudp == 'yes':
         output_line = output_line+' OPEN|FILTERED UDP: '
         firstudp = 'no'
      else:
         output_line = output_line+', '
      output_line = output_line+u.strip()+" "

   myfile.write("%s\n" % output_line)

#
# Now that all lines of the input file have been parsed and the results
# written to the output file, we can close the output file.
#

myfile.close()
