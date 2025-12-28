import socket
import threading
import csv
from queue import Queue
import sys

# Get target input
target = input("Enter target IP or domain: ")

# 🔴 VALIDATION CHECK
try:
    socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid IP address or domain name")
    sys.exit()

port_queue = Queue()
print_lock = threading.Lock()

def scan_port(port, service):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print(f"[OPEN] Port {port} | Service: {service}")

        sock.close()
    except:
        pass

def worker():
    while not port_queue.empty():
        port, service = port_queue.get()
        scan_port(port, service)
        port_queue.task_done()

# Read dataset
with open("ports_dataset.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        port_queue.put((int(row["port"]), row["service"]))

print("\nScanning ports from dataset...\n")

# Thread count
thread_count = 50
threads = []

for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.daemon = True
    threads.append(t)
    t.start()

port_queue.join()

print("\nScan completed using dataset.")
