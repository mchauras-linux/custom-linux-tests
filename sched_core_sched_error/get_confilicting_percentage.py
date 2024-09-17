#!/usr/bin/env python3

import re
import sys

# Path to the sched/debug file
SCHED_DEBUG_PATH = "/sys/kernel/debug/sched/debug"

nr_samples = 10000
nr_error = 0
def parse_cpu_data():
    # Dictionaries to store processes by CPU type
    even_cpu_processes = {}
    odd_cpu_processes = {}

    # Check if the file exists and is readable
    try:
        with open(SCHED_DEBUG_PATH, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: Cannot read {SCHED_DEBUG_PATH}. Run as root or ensure the file exists.")
        sys.exit(1)

    current_cpu = None

    for line in lines:
        line = line[:26].strip()  # Get the first 26 characters to match the behavior of `cut -c -26`
        
        # Check if the line indicates a CPU
        if line.startswith('cpu#'):
            # Extract the CPU number
            current_cpu = int(re.search(r'cpu#(\d+)', line).group(1))
        
        # Check for running processes on the CPU
        elif line.startswith('>R'):
            # Extract the process information and PID
            parts = line.split()
            process_name = parts[0]
            pid = parts[1] if len(parts) > 1 else "unknown"

            # Store process information based on CPU type
            if current_cpu is not None:
                if current_cpu % 2 == 0:
                    if current_cpu not in even_cpu_processes:
                        even_cpu_processes[current_cpu] = []
                    even_cpu_processes[current_cpu].append((process_name, pid))
                else:
                    if current_cpu not in odd_cpu_processes:
                        odd_cpu_processes[current_cpu] = []
                    odd_cpu_processes[current_cpu].append((process_name, pid))
    
    return even_cpu_processes, odd_cpu_processes

def check_stress_core_processes(even_cpu_processes, odd_cpu_processes):
    global nr_error
    for cpu, processes in even_cpu_processes.items():
        stress_core_found = any('stress_core' in name for name, _ in processes)
        if stress_core_found:
            if len(even_cpu_processes) > 1:
                nr_error = nr_error + 1
    for cpu, processes in odd_cpu_processes.items():
        stress_core_found = any('stress_core' in name for name, _ in processes)
        if stress_core_found:
            if len(odd_cpu_processes) > 1:
                nr_error = nr_error + 1

if __name__ == "__main__":
    for _ in range(nr_samples):
        even_cpu_processes, odd_cpu_processes = parse_cpu_data()
        check_stress_core_processes(even_cpu_processes, odd_cpu_processes)
    error_percent = (nr_error / nr_samples) * 100
    print(f"Error %: '{error_percent}'")

