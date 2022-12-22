import os
import numpy as np
import sys


IN_FILE = './cooked_traces/'
OUT_FILE = './mahimahi_traces/'
FILE_SIZE = 2000
BYTES_PER_PKT = 1500.0
MILLISEC_IN_SEC = 1000.0
EXP_LEN = 5000.0  # millisecond
MBITPS_TO_BPMS = 125.0


def main():
    if len(sys.argv) == 2:
        IN_FILE = sys.argv[1]
        if not os.path.exists(IN_FILE):
            print("provide valid path")
            sys.exit()
        if IN_FILE[-1] != '/':
            print("provide path name with /")
            sys.exit()
        OUT_FILE = f"{IN_FILE[:-1]}_mahimahi/"
    else:
        print("provide cooked trace dir")
        sys.exit()
        
    if not os.path.exists(OUT_FILE):
        os.mkdir(OUT_FILE)
        
    files = os.listdir(IN_FILE)
    for trace_file in files:
        print(f"trace file: {trace_file}")
        if os.stat(IN_FILE + trace_file).st_size >= FILE_SIZE:
            with open(IN_FILE + trace_file, 'r') as f, open(OUT_FILE + trace_file, 'w') as mf:
                print(f"OUT_FILE = {OUT_FILE + trace_file}")
                t_secs = []
                throughputs = []
                for line in f:
                    t_sec, throughput = line.split()
                    t_secs.append(float(t_sec))
                    throughputs.append(float(throughput))
                t_secs = np.array(t_secs)
                throughputs = np.array(throughputs)
                print(f"finished parsing: with ({len(t_secs)}, {len(throughputs)}) records")
                if len(t_secs) < 5 or len(throughputs) < 5:
                    print(f"check {trace_file}, got only {len(t_secs)} records")
                    sys.exit()
                millisec_time = 0
                mf.write(str(millisec_time) + '\n')
                for i in range(len(throughputs) - 1):
                    start_ms = t_secs[i] * MILLISEC_IN_SEC
                    end_ms = t_secs[i+1] * MILLISEC_IN_SEC
                    duration = end_ms - start_ms
                    this_throughput = throughputs[i] * MBITPS_TO_BPMS
                    pkt_per_millisec = (this_throughput) / (BYTES_PER_PKT)
                    
                    print(f"duration: {duration}, this_tp: {this_throughput} pkt_per_mil: {pkt_per_millisec}")
                    millisec_count = 0
                    pkt_count = 0
                    while millisec_count < duration:
                        millisec_count += 1
                        millisec_time += 1
                        to_send = (millisec_count * pkt_per_millisec) - pkt_count
                        to_send = np.floor(to_send)
                        #print(f"millisec_count: {millisec_count} to_send: {to_send}")
                        for i in range(int(to_send)):
                            mf.write(str(millisec_time) + '\n')

                        pkt_count += to_send
                    
                    
                    
                    
                    



if __name__ == '__main__':
    main()
