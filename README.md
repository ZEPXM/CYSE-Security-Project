# CYSE 130 Project Part 3 - Analysis and Submission Github Repository
Project for CYSE 130 at GMU

## Project Overview

The scripts provided here (under /scripts) automate cybersecurity measures, such as port scanning, resource monitoring, email alerting, and monitoring TCP/IP connections.

The diagrams under /diagrams are UML diagrams for the cyber infrastructure of a theoretical finance management company.

/documentation contains the system requirements for these programs and the planning document we had to design the scripts.

/results contains the logged results for each of the scripts. 

## Installation

```
git clone https://github.com/ZEPXM/CYSE-Security-Project.git
cd CYSE-Security-Project
python3 -m pip install -r requirements.txt
```

After these steps, you should tweak the manual values (how long a program should last, the email username, password, recipient, etc) in each of the scripts in /scripts.

You should also delete the example logs in /results, as some of them would be appended to on future program runs.

It's also important to note that some of the scripts are OS-dependent. They have only been tested on Ubuntu 24.04.1 LTS running the Windows Subsystem for Linux on Windows 10.

## Usage

Assuming you're in the root directory of the repository, run

```
python3 ./scripts/<insert script>.py
```

You can combine this with systemd timers, crontab, or another task scheduler to run a script in the background periodically.

## Team Members
Neil Sharma - Project Manager

Monish Kumar - Systems Modeler

Jose Perez - Systems Modeler

Mayank Bojja - Python Developer

Manpreet Singh - Python Developer

Tony Guiracocha - Data Analyst
