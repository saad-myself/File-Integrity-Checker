# 🛡️ File Integrity Checker (FIC)

A lightweight, custom Host-based Intrusion Detection System (HIDS) built in Python. This tool monitors a target directory and uses cryptographic hashing to detect unauthorized file creations, modifications, and deletions in real-time.

## 🚀 Features
* **SHA-256 Fingerprinting:** Detects even a 1-bit change in file contents.
* **Memory Efficient:** Processes large files using 4KB chunking to prevent RAM overload.
* **Live Monitoring:** Continuous active scanning loop with terminal-based color-coded alerts.
* **Zero Dependencies:** Built entirely using Python's standard libraries (`hashlib`, `os`, `json`).

## 🛠️ Usage (Kali Linux)

**1. Clone the repository**
```bash
git clone [https://github.com/mdunaisk/File-Integrity-Checker.git](https://github.com/mdunaisk/File-Integrity-Checker.git)
cd File-Integrity-Checker
```

**2. Run the tool**
```bash
python3 fic.py
```

**3. Operation Modes**
* **Option 1 (Baseline):** Scans the target directory and generates a `baseline.json` database of known-good hashes.
* **Option 2 (Monitor):** Actively compares the live directory against the baseline, flagging any anomalies (New, Modified, or Deleted files).

## 📝 Academic Integrity
This project was developed as a college capstone project to demonstrate applied cryptography, operating system I/O, and secure state management without the use of pre-existing security wrappers.

