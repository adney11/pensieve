traces=$1

for file in "$traces*";
do
    python plot_mahimahi_bandwidth.py $file
done