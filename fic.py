# File Integrity Checker (FIC)

import hashlib
import json
import os
import sys
import time

DB_FILE = "baseline.json"

def get_hash(filepath):
    # Using sha256 to hash the files in chunks so we don't blow up the RAM
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def setup_baseline(directory):
    print(f"\n[+] Building baseline for: {directory}")
    state = {}

    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.abspath(os.path.join(root, name))
            
            # Don't hash the database itself
            if os.path.basename(path) == DB_FILE:
                continue
                
            file_hash = get_hash(path)
            if file_hash:
                state[path] = file_hash

    with open(DB_FILE, "w") as f:
        json.dump(state, f, indent=4)
        
    print(f"[+] Saved {len(state)} files to {DB_FILE}.\n")

def run_monitor(directory):
    if not os.path.exists(DB_FILE):
        print(f"[-] Missing {DB_FILE}. Please run option 1 first.")
        return

    print(f"[*] Loading baseline...")
    with open(DB_FILE, "r") as f:
        baseline = json.load(f)

    print(f"[*] Monitoring {directory}...")
    print("[*] Hit Ctrl+C to quit.\n")

    try:
        while True:
            current_state = {}
            
            # Scan current files
            for root, dirs, files in os.walk(directory):
                for name in files:
                    path = os.path.abspath(os.path.join(root, name))
                    
                    if os.path.basename(path) == DB_FILE:
                        continue
                    
                    file_hash = get_hash(path)
                    if file_hash:
                        current_state[path] = file_hash

            # Check for changes or new files
            for path, current_hash in current_state.items():
                if path not in baseline:
                    print(f"\033[92m[+] NEW FILE: {path}\033[0m")
                    baseline[path] = current_hash 
                elif baseline[path] != current_hash:
                    print(f"\033[91m[!] MODIFIED: {path}\033[0m")
                    baseline[path] = current_hash

            # Check for deletions
            deleted = [p for p in baseline if p not in current_state]
            for path in deleted:
                print(f"\033[93m[-] DELETED: {path}\033[0m")
                del baseline[path]

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[*] Exiting monitor mode.")

if __name__ == "__main__":
    print("=== File Integrity Monitor ===")
    print("1. Create Baseline")
    print("2. Start Monitoring")
    
    choice = input("\nSelect (1/2): ").strip()
    target = os.getcwd() 
    
    if choice == "1":
        setup_baseline(target)
    elif choice == "2":
        run_monitor(target)
    else:
        print("[-] Invalid input. Exiting.")
