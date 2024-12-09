## Logs CPU, Memory, and Disk Usage over time 
## and writes alerts depending on how severe one of the usages is

# Imports
import psutil # For tracking usage data
import time # For time keeping
from datetime import datetime # For datetime objects (formatting timestamps in date-time pairs)
import os # For changing the current working directory

duration = 60 # Scan over 60 seconds
start_time = time.time()
log_filename = "../results/SystemPerformanceMonitoring.log"

# Before running the script, set current working directory to
# where the script is running, so it will output into the results folder

absolute_path = os.path.abspath(__file__)
directory = os.path.dirname(absolute_path)

os.chdir(directory)

print(f"Writing to log file {log_filename} over a {duration} second period...")

with open(log_filename, 'a') as log_file:

	# Write header to log file
	print(f"Start time: {str(datetime.fromtimestamp(time.time()))}\n\nTime	CPU	    Memory  Disk", file = log_file, flush = True)

	while time.time() - start_time < duration: # While the monitoring period hasn't expired
		# Collect usage data
		cpu_usage = psutil.cpu_percent(interval=1)
		memory_usage = psutil.virtual_memory().percent
		disk_usage = psutil.disk_usage('/').percent

		# This formats all the values for human readability to the log file (relative time (seconds), memory, cpu, disk)
		print(f"{round(time.time() - start_time, 1):>4}	{str(memory_usage) + '%':<8}{str(cpu_usage) + '%':<8}{str(disk_usage) + '%'}", file = log_file, flush = True)

		# Alerting
		if cpu_usage >= 90:
			print("ALERT: CPU usage at high levels.", file = log_file)
			print("ALERT: CPU usage at high levels.")
		if memory_usage >= 90:
			print("ALERT: Memory usage at high levels.", file = log_file)
			print("ALERT: Memory usage at high levels.")
		if disk_usage >= 90:
			print("ALERT: Disk is almost full.", file = log_file)
			print("ALERT: Disk is almost full.")

		time.sleep(0.9) # Don't log way too much, wait a little (.9 seconds + however long it takes to run the other commands)
	
	print(file = log_file) # Newline to separate future log entries

print("Done!")