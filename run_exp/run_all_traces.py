import os
import time
import json
import urllib.request as url
import subprocess


def dp(msg):
	dbg = os.getenv('DEBUG_MODE')
	if dbg:
		print("DEBUG: " + msg)


TRACE_PATH = './mahimahi_test_traces/' 

with open('./chrome_retry_log', 'a') as f:
	f.write('chrome retry log\n')

os.system('sudo sysctl -w net.ipv4.ip_forward=1')

ip_data = json.loads(url.urlopen("http://ip.jsontest.com/").read())
ip = str(ip_data['ip'])

python_command = '/users/acardoza/venv/bin/python run_traces.py '

ABR_ALGO = 'BB'
PROCESS_ID = 0
command_BB = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'RB'
PROCESS_ID = 1
command_RB = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'FIXED'
PROCESS_ID = 2
command_FIXED = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'FESTIVE'
PROCESS_ID = 3
command_FESTIVE = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'BOLA'
PROCESS_ID = 4
command_BOLA = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'fastMPC'
PROCESS_ID = 5
command_fastMPC = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'robustMPC'
PROCESS_ID = 6
command_robustMPC = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'RL'
PROCESS_ID = 7
command_RL = python_command + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

dp(f"running command: {command_BB}")
proc_BB = subprocess.Popen(command_BB, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
dp(f"running command: {command_RB}")
proc_RB = subprocess.Popen(command_RB, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

dp(f"running command: {command_FIXED}")
proc_FIXED = subprocess.Popen(command_FIXED, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
dp(f"running command: {command_FESTIVE}")
proc_FESTIVE = subprocess.Popen(command_FESTIVE, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
dp(f"running command: {command_BOLA}")
proc_BOLA = subprocess.Popen(command_BOLA, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

dp(f"running command: {command_fastMPC}")
proc_fastMPC = subprocess.Popen(command_fastMPC, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

dp(f"running command: {command_robustMPC}")
proc_robustMPC = subprocess.Popen(command_robustMPC, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

dp(f"running command: {command_RL}")
proc_RL = subprocess.Popen(command_RL, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

proc_BB.wait()
proc_RB.wait()
proc_FIXED.wait()
proc_FESTIVE.wait()
proc_BOLA.wait()
proc_fastMPC.wait()
proc_robustMPC.wait() 
proc_RL.wait()
