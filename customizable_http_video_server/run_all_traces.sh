#!/bin/bash -x

abrs=("RL")
traces='/newhome/Orca/below6mbps_test_mahimahi/' #$1
scheme=$1
all_traces='/newhome/Orca/traces/' #$3
donedir='/newhome/Orca/below6mbps_test_mahimahi_done/'
limit=10


for abr in ${abrs[@]}
do
    count=0
    for trace in $traces*
    do
        tracename=$(basename $trace)
        echo "./run_trace.sh 44444 $abr $all_traces $tracename $scheme ."
        ./run_trace.sh 44444 $abr $all_traces $tracename $scheme .
        mv $trace $donedir
        count=$((count + 1))
        if [[ "$count" -eq $limit ]];
        then
            echo "finished $limit traces"
            break
        fi
        sleep 5
    done

done
echo "finished run_all_traces.sh"

# Run using following command
# ./run_all_traces.sh /newhome/Orca/fcc_traces/ bbr /newhome/Orca/traces/