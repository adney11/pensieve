import os
import sys
import logging
import numpy as np
import math



logging.basicConfig()
logging.basicConfig(filename='logs/convert_trace_to_mahimahi_format.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)


# [0] - train set, [1] is test set
TRACE_DIRS = ('./cooked_traces/', './cooked_test_traces')
TRACE_NAME = '25_5mbps_real'
TRACE_SUFFIX = '-mahimahi_format.txt'

MEGABITS_PER_SECOND_TO_BYTES_PER_MS = 125.0
MILLISEC_IN_SEC = 1000.0
BYTES_PER_PKT = 1500.0


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


def convert_to_mahimahi(tp, duration, millisec_time, mf):
    if duration < 0:
        LOG.error("measurement duration is negative")
        sys.exit()
                    
    tp = tp * MEGABITS_PER_SECOND_TO_BYTES_PER_MS
    duration = duration * MILLISEC_IN_SEC

    pkt_per_millisec = tp / BYTES_PER_PKT
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
    return millisec_time

target_dir = './'+TRACE_NAME+'/'
for dir in TRACE_DIRS:
    newdir = os.path.join(target_dir, dir[2:-1])
    print(newdir)
    #sys.exit()
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        LOG.debug(f"src file path is: {f}")
        if os.path.isfile(f):
            print(dir, " | ", f, " | ", target_dir)
            with open(os.path.join(newdir, filename+TRACE_SUFFIX), 'w') as mf, open(f, "r") as src_file:
                time_sec = []
                throughput = []
                for line in src_file:
                    parse = line.split()
                    time_sec.append(float(parse[0]))
                    throughput.append(float(parse[1]))

                time_sec = np.array(time_sec)
                throughput = np.array(throughput)

                millisec_time = 0
                mf.write(str(millisec_time) + '\n')

                for i in range(len(throughput) - 1):
                    tp = throughput[i] # in Mbit/s
                    duration = time_sec[i+1] - time_sec[i]
                    millisec_time = convert_to_mahimahi(tp, duration, millisec_time, mf)
                    printProgress(i, len(throughput) - 1)

                tp = throughput[-1]
                duration = time_sec[-1] - time_sec[-2]
                millisec_time = convert_to_mahimahi(tp, duration, millisec_time, mf)
                LOG.debug(f"converted {f}")