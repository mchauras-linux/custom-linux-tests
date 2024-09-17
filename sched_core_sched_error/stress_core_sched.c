#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/prctl.h>

static unsigned long get_cs_cookie(int pid) {
    int ret;

    // Use prctl to set up core scheduling
    ret = prctl(PR_SCHED_CORE, PR_SCHED_CORE_CREATE, pid, 1, 0);
    if (ret) {
        printf("Error: %d\tNot a core scheduling system\n", ret);
        return -1UL;
    }

    return ret;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <duration_in_seconds>\n", argv[0]);
        return 1;
    }

    // Get the duration from the command-line argument
    int duration = atoi(argv[1]);
    if (duration <= 0) {
        printf("Please provide a positive duration in seconds.\n");
        return 1;
    }

    // Get the process ID
    int pid = getpid();

    // Attach the process to core scheduling using prctl
    if (get_cs_cookie(pid) == -1UL) {
        printf("Failed to attach to core scheduling.\n");
        return 1;
    }

    printf("Process attached to core scheduling group.\n");

    time_t start_time, current_time;

    // Get the start time
    start_time = time(NULL);

    // Run the while loop until the specified duration has elapsed
    while (1) {
        // Get the current time
        current_time = time(NULL);

        // Check if the specified duration has passed
        if (difftime(current_time, start_time) >= duration) {
            break;
        }
    }

    printf("Loop ran for %d seconds.\n", duration);
    return 0;
}

