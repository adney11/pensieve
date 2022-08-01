import sys
import os
import subprocess
import numpy as np


RUN_SCRIPT = 'run_video.py'
RANDOM_SEED = 42
RUN_TIME = 320  # sec
MM_DELAY = 10   # millisec

run_count = os.getenv('RUN_COUNT')


import logging
logging.basicConfig(filename='logs/run_traces.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)

def dp(msg):
	LOG.debug(msg)

def main():
	trace_path = sys.argv[1]
	abr_algo = sys.argv[2]
	process_id = sys.argv[3]
	ip = sys.argv[4]

	sleep_vec = [i for i in range(1, 10)]  # random sleep second

	files = os.listdir(trace_path)
	global run_count
	if run_count == None:
		run_count = len(files)
	else:
		run_count = int(run_count)
	cnt = 0
	for f in files:
		if cnt >= run_count:
			break
		cnt += 1
		while True:

			np.random.shuffle(sleep_vec)
			sleep_time = sleep_vec[int(process_id)]
			
			command = 'mm-delay ' + str(MM_DELAY) + \
					  ' mm-link 12mbps ' + trace_path + f + ' ' +	\
					  'python ' + RUN_SCRIPT + ' ' + ip + ' ' + \
					  abr_algo + ' ' + str(RUN_TIME) + ' ' + \
					  process_id + ' ' + f + ' ' + str(sleep_time)

			dp(f"running command: {command}")
			proc = subprocess.Popen(command,
					  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			(out, err) = proc.communicate()
			dp(f"type(out) = {type(out)} out.decode = {out.decode('utf-8')}")
			if out.decode('utf-8') == 'done\n':
				break
			else:
				with open('./chrome_retry_log', 'a') as log:
					log.write(abr_algo + '_' + f + '\n')
					log.write("out: " + out.decode('utf-8') + '\n')
					log.flush()



if __name__ == '__main__':
	main()
