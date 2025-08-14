#!/usr/bin/env python3
"""
===============================================================================
Project: Optimized Multi-threaded IP Range Ping Scanner
Author: Dr. Burak BAYSAN - burak@baysan.tr
GitHub: https://github.com/drburakbaysan
Version: 3.0
Date: 2025-08-14

Description:
This script scans large IP ranges efficiently by dynamically optimizing the number
of threads based on range size. It supports Windows, Linux, MacOS and optionally
saves results to CSV. Live progress and detailed status (ONLINE/OFFLINE) are displayed.

Features:
- Dynamic thread count optimization for large IP ranges
- Live progress percentage
- Optional CSV output
- Platform-independent ping
- Detailed English comments
===============================================================================
"""

import subprocess
import platform
import threading
from queue import Queue
import csv

# ---------------------------------------------------------------------------
# ---------------------- CONFIGURATION --------------------------------------
# ---------------------------------------------------------------------------

MAX_THREADS = 200       # Maximum threads for very large networks
MIN_THREADS = 10        # Minimum threads for small networks

# ---------------------------------------------------------------------------
# ---------------------- PING FUNCTION -------------------------------------
# ---------------------------------------------------------------------------

def ping_ip(ip_address):
    """
    Ping a single IP to check if it's alive.
    """
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', ip_address] if platform.system().lower()=='windows' else ['ping', param, '1', '-W', '1', ip_address]
    try:
        response = subprocess.run(command, capture_output=True, text=True)
        return response.returncode == 0
    except Exception as e:
        print(f"[ERROR] Ping failed for {ip_address}: {e}")
        return False

# ---------------------------------------------------------------------------
# ---------------------- IP RANGE FUNCTIONS --------------------------------
# ---------------------------------------------------------------------------

def ip_to_int(ip):
    """Convert IP string to integer"""
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

def int_to_ip(ip_int):
    """Convert integer to IP string"""
    return f"{(ip_int>>24)&255}.{(ip_int>>16)&255}.{(ip_int>>8)&255}.{ip_int&255}"

# ---------------------------------------------------------------------------
# ---------------------- WORKER FUNCTION -----------------------------------
# ---------------------------------------------------------------------------

def worker():
    """Worker thread to process IPs from queue"""
    while True:
        ip_int = q.get()
        if ip_int is None:
            break
        ip_str = int_to_ip(ip_int)
        online = ping_ip(ip_str)
        status = "ONLINE ✅" if online else "OFFLINE ❌"

        with lock:
            results.append([ip_str, status])
            global scanned
            scanned += 1
            percent = (scanned / total_ips) * 100
            print(f"{ip_str}: {status} | Progress: {percent:.1f}%", end='\r', flush=True)

        q.task_done()

# ---------------------------------------------------------------------------
# ---------------------- MAIN SCRIPT ---------------------------------------
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("🔹 Optimized IP Range Ping Scanner - Dr. Burak BAYSAN 🔹")
    print("Enter IP range to scan (e.g., 192.168.1.1 192.168.1.254)")

    start_ip = input("Start IP: ").strip()
    end_ip = input("End IP: ").strip()

    if not start_ip or not end_ip:
        print("[ERROR] Invalid IP input.")
        exit(1)

    # Optional CSV output
    save_csv = input("Save results to CSV? (y/n): ").strip().lower() == 'y'

    start_int = ip_to_int(start_ip)
    end_int = ip_to_int(end_ip)
    total_ips = end_int - start_int + 1
    scanned = 0
    results = []
    lock = threading.Lock()

    # Dynamic thread count optimization
    thread_count = min(MAX_THREADS, max(MIN_THREADS, total_ips//5))

    # Queue preparation
    q = Queue()
    for ip_int in range(start_int, end_int + 1):
        q.put(ip_int)

    # Start threads
    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    q.join()  # Wait for completion

    # Stop threads
    for i in range(len(threads)):
        q.put(None)
    for t in threads:
        t.join()

    print("\n"+"-"*60)
    print("Scan complete.")

    # Save CSV if requested
    if save_csv:
        csv_filename = "ping_results.csv"
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Status"])
            writer.writerows(results)
        print(f"Results saved to {csv_filename}")
