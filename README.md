# 🔹 Python IP Ping Scanner 🔹

**Author:** Dr. Burak BAYSAN - burak@baysan.tr  
**GitHub:** [drburakbaysan](https://github.com/drburakbaysan)  
**Version:** 3.0  
**Date:** 2025-08-14  

---

## 🌐 Overview
Python IP Ping Scanner is a multi-threaded, high-performance network scanning tool designed for large IP ranges.  
It dynamically optimizes thread count based on range size, ensuring rapid scanning without overloading system resources.  
Supports Windows, Linux, and MacOS platforms with consistent performance.

---

## ⚡ Features
- Multi-threaded scanning for speed and efficiency  
- Dynamic thread optimization based on IP range size  
- LIVE progress percentage indicator for real-time monitoring  
- ONLINE/OFFLINE status per IP with clear visual feedback  
- Optional CSV export for saving results (`ping_results.csv`)  
- Platform-independent (Windows/Linux/MacOS)  
- Fully documented with detailed English comments for clarity  

---

## 🛠 Technical Details
- Uses `subprocess` to ping each IP individually  
- IPs converted to integers for efficient iteration  
- Multi-threaded workers pull from a `Queue` to process IPs concurrently  
- Thread count dynamically adjusted: `min(MAX_THREADS, max(MIN_THREADS, total_ips//5))`  
- CSV export writes IP and status columns if enabled  
- Progress updated in-place using `end='\r'` and flush to terminal  
- Handles exceptions and invalid IP inputs gracefully  

---

## 💾 CSV Output
- Optional and configurable  
- Columns: `IP Address`, `Status`  
- Saves to `ping_results.csv` in the project directory  
- Compatible with Excel, Google Sheets, and other CSV viewers  

---

## 🚀 Usage Notes
- Designed to handle small to very large IP ranges  
- Efficiently manages system resources with thread optimization  
- Real-time progress provides instant insight into scan completion  
- Thread and queue management ensures stability even under large loads  
- Fully commented code facilitates customization or integration into other projects  

---

## 📌 Key Advantages
- Scalability: Handles ranges from single IPs to thousands seamlessly  
- Accuracy: Each IP is pinged reliably using platform-appropriate commands  
- Transparency: Clear status output and optional CSV log for audit  
- Cross-platform: Works consistently across major operating systems  
- Extensibility: Code structured for easy enhancement (GUI, network analysis, etc.)  

---

## 🔗 Author & Contact
**Dr. Burak BAYSAN**  
Email: burak@baysan.tr  
GitHub: [drburakbaysan](https://github.com/drburakbaysan)  
LinkedIn: [linkedin.com/in/drburakbaysan](https://www.linkedin.com/in/drburakbaysan)  

---

> This tool is designed for network administrators, IT professionals, and cybersecurity enthusiasts who need rapid and reliable IP reachability scanning across large networks.
