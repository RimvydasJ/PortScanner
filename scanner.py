import subprocess as sp
import socket as s
import threading as t
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

def run_nmap():
    print("Nmap")

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
            
            port_q.task_done()

    
    target_ip = input("Enter target IP address: ")
    print("Starting search...")
    # Check if correct format of ip address

    start = datetime.now()

    for x in range(TOTAL_WORKERS):
        thread = t.Thread(target=scan_ports)
        thread.daemon = True
        thread.start()

    port_q.join();
    end = datetime.now()
    duration = end-start
    print("Duration: " + str(duration))

if __name__ == '__main__':
    try:
        print("-" * 30)
        print("Welcome to port scanner")
        print("-" * 30)
        entry()
    except KeyboardInterrupt:
        print("\n Finished")
        quit()