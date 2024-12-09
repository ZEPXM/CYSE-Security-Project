## Monitor network packets
## For a 60-second duration, gets all TCP/IP packets and outputs them to scapy.log
## Along with the time in seconds relative to the start time

from scapy.all import * # For monitoring network packets
import time # For time keeping
import os # For changing the current working directory

log_filename = "../results/MonitorNetworkPackets.log"
duration = 60

# Formats packets from programmatic format to a text file column
def monitor_packet(start_time, packet, log_file):
	if packet.haslayer('TCP') and packet.haslayer('IP'): # If the packet's TCP or IP
		# Pretty print the time, source_ip, then dest_ip
		print(f"{round(packet.time - start_time, 1):>4}	{packet['IP'].src:<18}{packet['IP'].dst}", file = log_file, flush = True)

# Before running the script, set current working directory to
# where the script is running, so it will output into the results folder

absolute_path = os.path.abspath(__file__)
directory = os.path.dirname(absolute_path)

os.chdir(directory)

print(f"Monitoring for {duration} seconds, outputting to {log_filename}.")
start_time = time.time()

with open(log_filename, 'w') as scapy_log_file:
	print("Time	Src IP            Dest IP", file = scapy_log_file, flush = True) # Headers
	while time.time() - start_time < duration: # While we're still in the monitoring period
		packets = sniff(count = 10) # Get 10 packets
		
		# Loop and pretty-print packets
		for packet in packets:
			monitor_packet(start_time, packet, scapy_log_file)

print("Monitoring complete!")