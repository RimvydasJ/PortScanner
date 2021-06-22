import subprocess as sp
import socket as s
import threading as t
from queue import Queue
from datetime import datetime
import nmap3
import json
import ipaddress
import sys

TOTAL_PORTS = 65535
TOTAL_WORKERS = 200
THREAD_TIMEOUT = 0.20

sp.call('clear', shell=True)

port_q = Queue()
[port_q.put(w) for w in range(TOTAL_PORTS)]

s.setdefaulttimeout(THREAD_TIMEOUT)
t_lock = t.Lock()
ports = []

def run_nmap(target_ip):
    nmap = nmap3.NmapHostDiscovery()
    print("Press enter for default nmap arguments: -sV -A -sC")
    args = input("Or enter your own: ")
    if len(ports) > 0:
        joined_ports = ",".join(ports)
        default_args = "-sV -A -sC"
        if args:
            default_args = args
        port_results = nmap.nmap_portscan_only(target_ip, args="{} -p {}".format(default_args,joined_ports))
        print("-" * 30)
        print(json.dumps(port_results,sort_keys=False, indent=4))

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

    
    target_ip = "127.0.0.1"

    while True:
        try:
            target_ip = input("Enter target IP address: ")
            ipaddress.ip_address(target_ip)
            break
        except ValueError:
            continue
    
    print("Starting scan...")

    start = datetime.now()

    for x in range(TOTAL_WORKERS):
        thread = t.Thread(target=scan_ports)
        thread.daemon = True
        thread.start()

    port_q.join();
    end = datetime.now()
    duration = end-start
    print("-" * 30)
    print("Scan duration: " + str(duration))
    print("-" * 30)
    
    user_selection = "0"
    while user_selection == "0":
        print("1 - Run nmap")
        print("2 - Quit")
        user_selection = input("\nSelection: ")
        print("-" * 30)
        if user_selection == "1":
            run_nmap(target_ip)
        elif user_selection == "2":
            sys.exit()
        else: 
            user_selection = "0"
    


if __name__ == '__main__':
    try:
        print("-" * 30)
        print("Welcome to port scanner")
        print("-" * 30)
        entry()
    except KeyboardInterrupt:
        print("\nFinished")
        quit()