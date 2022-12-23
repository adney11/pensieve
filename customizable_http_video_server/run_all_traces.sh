#!/bin/bash -x

abrs=("RL")
traces=$1
scheme=$2
all_traces=$3
donelog="./"


for abr in ${abrs[@]}
do
    for trace in $traces*
    do
        tracename=$(basename $trace)
        echo "./run_trace.sh 44444 $abr $all_traces $tracename $scheme ."
        ./run_trace.sh 44444 $abr $all_traces $tracename $scheme .
        mv $trace /newhome/Orca/fcc_traces_done/
        sleep 5
    done

done

# Run using following command
# ./run_all_traces.sh /newhome/Orca/fcc_traces/ bbr /newhome/Orca/traces/