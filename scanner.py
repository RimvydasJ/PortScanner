import sys
import subprocess as sp
import sys
import signal
import os
import socket as s
import time
import threading as t
import concurrent.futures

from queue import Queue
from datetime import datetime

TOTAL_PORTS = 65536
TOTAL_WORKERS = 200
THREAD_TIMEOUT = 0.20

sp.call('clear', shell=True)

port_q = Queue()
[port_q.put(w) for w in range(TOTAL_PORTS)]

s.setdefaulttimeout(THREAD_TIMEOUT)
t_lock = t.Lock()
ports = []

def entry():
    def scan_ports():
        while True:
            port = port_q.get();
            soc = s.socket(s.AF_INET, s.SOCK_STREAM)

            try:
                conn = soc.connect((target_ip, port))
                with t_lock:
                    ports.append(str(port))
                    print("{} is open".format(port))
            except:
                pass
    
    target_ip = input("Enter target IP address: ")
    # Check if correct format of ip address

    start = datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=TOTAL_WORKERS) as executor:
        executor.map(scan_ports, range(TOTAL_WORKERS))

    port_q.join();
    end = datetime.now()
    duration = end-start
    print("Completed: " + str(duration))

if __name__ == '__main__':
    try:
        print("-" * 30)
        print("Welcome to port scanner")
        print("-" * 30)
        entry()
    except KeyboardInterrupt:
        print("\n Finished")
        quit()