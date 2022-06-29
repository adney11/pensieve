import os
import numpy as np

import logging
import math

FILE_PATH = '../cooked_test_traces/'
OUTPUT_PATH = './mahimahi_test_traces/'
BYTES_PER_PKT = 1500.0
MILLISEC_IN_SEC = 1000.0
BITS_IN_BYTE = 8.0
BYTES_IN_MEGABYTES = 1000.0
MEGABITS_PER_SECOND_TO_BYTES_PER_MS = 125.0

logging.basicConfig()
logging.basicConfig(filename='logs/convert_mahimahi_format.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def printProgress(curr, total):
	bar = '#'
	space = '-'
	period = '.'
	num_periods = 3
	progress_bar_length = 50
	done = math.ceil((curr / total) * progress_bar_length)
	pc = math.ceil((curr / total) * 100)
	remaining = progress_bar_length - done
	print(f"\r Progress: | {bar * done}{space * remaining } | {pc} % complete{period * (curr % num_periods)}", end = "\r")

def main():
	files = os.listdir(FILE_PATH)
	for trace_file in files:
		with open(FILE_PATH + trace_file, 'r') as f, open(OUTPUT_PATH + trace_file, 'w') as mf:
			time_ms = []
			throughput_all = []
			
			for line in f:
				parse = line.split()
				time_ms.append(float(parse[0]))
				throughput_all.append(float(parse[1]))
				

			time_ms = np.array(time_ms)
			throughput_all = np.array(throughput_all)

			millisec_time = 0
			mf.write(str(millisec_time) + '\n')

			for i in range(len(throughput_all) - 1):

				throughput = throughput_all[i]  # in Mbits/s
				duration =  time_ms[i+1] - time_ms[i]  # in seconds
				if duration < 0:
					LOG.error("measurement duration is negative")
					return
				
				throughput = throughput * MEGABITS_PER_SECOND_TO_BYTES_PER_MS # in bytes / ms
				duration = duration * MILLISEC_IN_SEC # in milliseconds
				
				pkt_per_millisec = throughput / BYTES_PER_PKT 

				millisec_count = 0
				pkt_count = 0

				while True:
					millisec_count += 1
					millisec_time += 1
					to_send = (millisec_count * pkt_per_millisec) - pkt_count
					to_send = np.floor(to_send)

					for i in range(int(to_send)):
						mf.write(str(millisec_time) + '\n')

					pkt_count += to_send

					if millisec_count >= duration:
						break
				printProgress(i, len(throughput_all) - 1)

if __name__ == '__main__':
	main()
