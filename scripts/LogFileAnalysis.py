## Given a UNIX auth.log (one sourced from Ubuntu works)
## Gets the counts, IPs (if applicable), and logs where:
## Failed to add user
## Failed to authenticate with public key over SSH
## Failed to authenticate with password over SSH
## All of these count as suspicious, so they will be filtered in accordingly

# Imports
import os # For changing the current working directory

# Variables to keep track of
failed_adding_user_count = 0
failed_publickeys = {} # Format: {ip: number of times their public key failed}
failed_passwords = {} # Format: {ip: number of times their password failed}
suspicious_logs = [] # Every time something gets caught, the full log is added here
summary_filename = "../results/LogFileAnalysis.log"

# Before running the script, set current working directory to
# where the script is running, so it will output into the results folder

absolute_path = os.path.abspath(__file__)
directory = os.path.dirname(absolute_path)

os.chdir(directory)

with open('/var/log/auth.log', 'r') as log_file:
	while (log_entry := log_file.readline()): # Run as long as the nextline is not empty (and set log_entry to the next line)
		if log_entry.split(": ")[1].startswith("Failed password for"): # If "failed password for" is after the first ": "
			ip_address = log_entry.split()[log_entry.split().index("from") + 1] # Get ip address (log processing)
			
			# Check if IP address already in dictionary
			if ip_address not in failed_passwords.keys():
				failed_passwords[ip_address] = 1 # If not then set it to 1
			else:
				failed_passwords[ip_address] += 1 # If so then increment it
			
			suspicious_logs.append(log_entry)
			continue # Don't waste time, a single log line can't have multiple of what we're checking for
		
		# Same algorithm but for pubkeys instead of passwords
		if log_entry.split(": ")[1].startswith("Failed publickey for"):
			ip_address = log_entry.split()[log_entry.split().index("from") + 1]
			if ip_address not in failed_publickeys.keys():
				failed_publickeys[ip_address] = 1
			else:
				failed_publickeys[ip_address] += 1
			
			suspicious_logs.append(log_entry)
			continue

		if "failed adding user" in log_entry:
			failed_adding_user_count += 1
			suspicious_logs.append(log_entry)

	print(f"Failed adding user count: {failed_adding_user_count}")
	print(f"Failed SSH publickey count: {sum(failed_publickeys.values())}")
	print(f"Failed SSH password attempts: {sum(failed_passwords.values())}\n")

	print(f"Writing a more detailed summary to {summary_filename}...")

	with open(summary_filename, 'w') as summary_file:
		print(f"Failed adding user count: {failed_adding_user_count}", file = summary_file)
		print(f"Failed SSH publickey count: {sum(failed_publickeys.values())}", file = summary_file)
		print(f"Failed SSH password attempts: {sum(failed_passwords.values())}\n", file = summary_file)

		print("Failed password attempts by IP (greatest to least):", file = summary_file)
		
		# This algorithm works by making a iterator containing tuples of the attempts and ip addresses
		# Then sorting it descending (because sorted() works on the first element of the tuple)
		# Then prettyprinting it to the summary file back in ip_address: attempts form
		for attempts, ip_address in sorted(((attempts, ip_address) for ip_address, attempts in failed_passwords.items()), reverse = True):
			print(f"{ip_address}: {attempts}", file = summary_file)

		print("\nFailed publickeys by IP (greatest to least):", file = summary_file)

		# Same algorithm, just for pubkeys instead of passwords
		for attempts, ip_address in sorted(((attempts, ip_address) for ip_address, attempts in failed_publickeys.items()), reverse = True):
			print(f"{ip_address}: {attempts}", file = summary_file)

		print(f"\nSuspicious logs:\n{"".join(suspicious_logs)}", file = summary_file)
	
	print("Done!")