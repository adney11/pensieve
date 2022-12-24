#!/bin/bash -x

# setup stuff to match orca settings
sudo sysctl -q net.ipv4.tcp_wmem="4096 32768 4194304" #Doubling the default value from 16384 to 32768
sudo sysctl -w -q net.ipv4.tcp_low_latency=1
sudo sysctl -w -q net.ipv4.tcp_autocorking=0
sudo sysctl -w -q net.ipv4.tcp_no_metrics_save=1
sudo sysctl -w -q net.ipv4.ip_forward=1
#Mahimahi Issue: it couldn't make enough interfaces
#Solution: increase max of inotify
sudo sysctl -w -q fs.inotify.max_user_watches=524288
sudo sysctl -w -q fs.inotify.max_user_instances=524288

# inputs

port=$1
abr_algo=$2
trace_dir=$3
trace=$4
scheme=$5
result_dir=$6

down=$trace
up="wired6"
latency=10
qsize=30
log="custom-$scheme-$down-$up-$latency-${period}-$qsize-$abr_algo"

sudo killall -s15 python customizable_http_server Xvfb chrome chromedriver
./customizable_http_server $port $trace_dir $scheme 0 $down $up $latency $result_dir $log $qsize $abr_algo

# wait and clean up
sleep 5
sudo killall -s15 python customizable_http_server Xvfb chrome chromedriver

echo "[$0]: Doing Mahimahi log analysis for trace $trace"
out="sum-${log}.tr"
sudo echo $log >> $result_dir/log/$out
sudo perl $result_dir/mm-thr 500 $result_dir/log/down-${log} 1>$result_dir/plots/plot-${log}.svg 2>res_tmp
sudo cat res_tmp >>$result_dir/log/$out
sudo echo "------------------------------" >> $result_dir/log/$out
rm *tmp

echo "[$0]: Done"
