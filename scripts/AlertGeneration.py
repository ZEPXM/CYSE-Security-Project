## Send test email, then alert if one of CPU, RAM, or disk usage is >= 90%

# Imports
import smtplib # Library for sending emails
import time # For time keeping
from email.message import EmailMessage # Email message types to get it in the right format
from datetime import datetime # Datetime object to convert timestamp into a readable date-time pair
import os # For changing the current working directory
import psutil # For tracking CPU, Memory, and Disk usage

# Constants needed for sending an email
from_email = "bot799297@gmail.com"
to_email = "neiladityasharma@gmail.com"
password = "<REDACTED>" # passkey set in a custom panel, not my actual google password (still redacted it though)

# Time for monitoring in seconds (realistically it'd be infinite but here, just for demonstration purposes, it's 60)
duration = 60

log_filename = "../results/AlertGeneration.log"

# Send an email given a subject and a body and the constants at the top
def send_alert(subject, body):
	# Email message in the right format
	msg = EmailMessage()

	# Set information about the email
	msg.set_content(body)
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = to_email

	# Connect to GMail's SMTP server, login, and send email
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		try:
			smtp.login(from_email, password)
		except smtplib.SMTPAuthenticationError as error:
			print(f"{str(datetime.fromtimestamp(time.time()))}: Ran into authentication error: {error}", file = log_file)
		print(f"Successfully logged into {from_email}!")
		smtp.send_message(msg)
		print(f"Sent message with subject: {subject}")

# Before running the script, set current working directory to
# where the script is running, so it will output into the results folder

absolute_path = os.path.abspath(__file__)
directory = os.path.dirname(absolute_path)

os.chdir(directory)

log_file = open(log_filename, 'a')
print(f"{str(datetime.fromtimestamp(time.time()))}: Logging started.", file = log_file)
print(f"{str(datetime.fromtimestamp(time.time()))}: Attempting to send test email.", file = log_file)

# Test message, better to have an error now than when you actually need to get alerted
send_alert("Test Message", "This is a test message, just to ensure connectivity")

print(f"{str(datetime.fromtimestamp(time.time()))}: Test email succeeded.", file = log_file)
print(f"Monitoring for {duration} seconds, starting from {str(datetime.fromtimestamp(time.time()))}.")
print(f"{str(datetime.fromtimestamp(time.time()))}: Monitoring starting.", file = log_file)

start_time = time.time()

while time.time() - start_time < duration:
	# Get information
	cpu_usage = psutil.cpu_percent(interval=1)
	memory_usage = psutil.virtual_memory().percent
	disk_usage = psutil.disk_usage('/').percent

	if any(metric > 90 for metric in (cpu_usage, memory_usage, disk_usage)): # If any of cpu_usage, memory_usage, or disk_usage is above 90%
		send_alert(
			"ALERT: Urgent system alert",
			f"""
An alert has set off for the system based rules set for the below statistics.
Current statistics:
	CPU: {cpu_usage},
	Memory: {memory_usage},
	Disk: {disk_usage}
			""".strip()
		)
		print(f"{str(datetime.fromtimestamp(time.time()))}: Critical alert sent.", file = log_file)

	time.sleep(0.9)

print(f"{str(datetime.fromtimestamp(time.time()))}: Monitoring, logging ended.", file = log_file)
log_file.close()