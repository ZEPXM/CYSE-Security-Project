# Log File Analysis

We could go through the built-in Linux /var/log/auth.log and look out for SSH login failures, adding user failures, and SSH publickey failures, logging IP addresses and their occurrences.

This could run on a honeypot server, allowing system owners to investigate who is attacking their servers with SSH enabled.

# System Performance Monitoring

Use psutil to get some core metrics (maybe CPU usage, memory usage, disk space) and log those over time, along with logging any warnings if one of the values is too high.

# Alert Generation

We could just do what we did for system performance monitoring and send an email to a hardcoded account if a metric is >90%

# Automating Routine Security Checks

According to the specifications, this includes two things: vulnerability scanning and network traffic monitoring, so it makes sense to have a separate script for each.

## Vulnerability Scanning

We could just have a shorthand to run nmap on all TCP ports to see if there's any open ports that shouldn't be open. Also a good idea to do a service scan to see if any malware-associated services are running on newly open ports.

This would use subprocessing for command running and logging the output.

## Network Traffic Monitoring

We could use scapy to filter out all traffic that's TCP between 2 IP addresses (localhost and another IP) for future analysis.

This could be helpful to see if our clients are connecting to any malicious websites or if malware is CURLing an executable from a malicious domain.
