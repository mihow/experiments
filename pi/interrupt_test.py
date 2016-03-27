from __future__ import print_function

import os
import sys
import signal
import datetime as dt


n = 0
starttime = dt.datetime.now()

def show_results(*args, **kwargs):
        # print(args, kwargs)
        result = "{:,d}".format(n)
        elapsed_time = dt.datetime.now() - starttime
        print("\n\nCounted to: {}".format(result))
        print("In {:,.2f} seconds".format(
            elapsed_time.total_seconds()))
        print("That's {:,.0f} per second".format(
            n / elapsed_time.total_seconds()))

signal.signal(signal.SIGUSR1, show_results)
signal.signal(signal.SIGINFO, show_results)
# Stop / Start counter with signals without exiting>

print("PID: {}".format(os.getpid()))
print("Show current count with: `kill -INFO {}`".format(os.getpid()))

while True:
    try:
        n = n + 1
    except KeyboardInterrupt:
        show_results()
        sys.exit(0)
        # raise
