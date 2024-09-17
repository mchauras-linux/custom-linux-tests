#!/bin/bash

# Get the number of physical cores (not counting hyper-threading)
num_cores=$(lscpu | awk '/^Core\(s\) per socket:/ {print $4}' | head -n 1)
num_sockets=$(lscpu | awk '/^Socket\(s\):/ {print $2}' | head -n 1)
num_physical_cores=$((num_cores * num_sockets * 8))

# Array to store the PIDs of stress-ng processes
stress_pids=()

# Launch stress-ng processes for each physical core
for ((i=0; i<num_physical_cores; i++)); do
    # Start stress-ng in the background
    #stress-ng -c 1 -t 300 &\
    ./stress_core_sched 300 &
    # Get the PID of the last background process and store it
    stress_pids+=($!)
done

# Wait for a short moment to ensure all stress-ng processes are started
#sleep 10
#
## Run ./prctrl with each of the collected PIDs
#for pid in "${stress_pids[@]}"; do
#    ./prctrl "$pid"
#done

