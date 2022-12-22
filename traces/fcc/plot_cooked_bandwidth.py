import numpy as np
import matplotlib.pyplot as plt
import sys
import os

PACKET_SIZE = 1500.0  # bytes
TIME_INTERVAL = 5.0
BITS_IN_BYTE = 8.0
MBITS_IN_BITS = 1000000.0
MILLISECONDS_IN_SECONDS = 1000.0
N = 100
if len(sys.argv) < 2:
    print("provide trace file")
    sys.exit()
LINK_FILE = sys.argv[1]

time_all = []
bandwidth_all = []

with open(LINK_FILE, 'r') as f:
    for line in f:
        time, throughput = line.split()
        time_all.append(float(time))
        bandwidth_all.append(float(throughput))

bandwidth_all = np.array(bandwidth_all)
bandwidth_all = bandwidth_all * BITS_IN_BYTE

time_all = np.array(time_all)
plt.plot(time_all, bandwidth_all)
plt.xlabel('Time (second)')
plt.ylabel('Throughput (Mbit/sec)')
#plt.show()
if not os.path.exists("plots"):
    os.mkdir("plots")
plt.savefig(f"plots/{LINK_FILE.split('/')[1]}.png")
