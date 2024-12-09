## Running an nmap scan on localhost automatically with every script run

import subprocess # Executing a console command (nmap)
import os # For changing the current working directory

log_filename = "../results/AutomatingRoutineSecurityChecks.log"
log_file = open(log_filename, 'a')

# Before running the script, set current working directory to
# where the script is running, so it will output into the results folder

absolute_path = os.path.abspath(__file__)
directory = os.path.dirname(absolute_path)

os.chdir(directory)

# Nmap scan a target and output it to file
def run_nmap(target, log_file):
	# Run nmap command (environment variables are weird in Jupyter notebooks)
	# Scans TCP ports 0-65535 and gets the services of them
	# Can be used to see if any ports are open that shouldn't be open
	result = subprocess.run(['nmap', '-sV', '-p0-65535', target], capture_output=True, text=True)
	print(result.stdout)
	print(result.stdout, file = log_file)

# Run it on localhost to see if the local computer has any weird ports open
run_nmap("127.0.0.1", log_file)