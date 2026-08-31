import hashlib
import os
import json
import time

# Configuration
MONITOR_FOLDER = "./target_folder"
BASELINE_FILE = "baseline.json"

def calculate_sha512(filepath):
    """Calculates the SHA-512 hash of a file to verify its integrity."""
    hasher = hashlib.sha512()
    try:
        with open(filepath, 'rb') as file:
            # Read in chunks to handle large files efficiently
            buffer = file.read(65536)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        print(f"[-] Error reading {filepath}: {e}")
        return None

def create_baseline():
    """Scans the directory and saves the initial state (baseline)."""
    print("[+] Calculating initial file hashes. Please wait...")
    baseline_data = {}
    
    if not os.path.exists(MONITOR_FOLDER):
        os.makedirs(MONITOR_FOLDER)
        print(f"[!] Created {MONITOR_FOLDER}. Add files here to monitor them.")

    for filename in os.listdir(MONITOR_FOLDER):
        filepath = os.path.join(MONITOR_FOLDER, filename)
        if os.path.isfile(filepath):
            file_hash = calculate_sha512(filepath)
            if file_hash:
                baseline_data[filepath] = file_hash

    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline_data, f, indent=4)
    print(f"[+] Baseline successfully created at {BASELINE_FILE}")

def monitor_integrity():
    """Continuously checks current files against the saved baseline."""
    print("[+] Monitoring started. Press Ctrl+C to stop.")
    
    if not os.path.exists(BASELINE_FILE):
        print("[-] No baseline found. Please run baseline creation first.")
        return

    with open(BASELINE_FILE, 'r') as f:
        saved_baseline = json.load(f)

    try:
        while True:
            time.sleep(2) # Pause for 2 seconds before checking again
            current_files = []
            
            # Check for modified or new files
            for filename in os.listdir(MONITOR_FOLDER):
                filepath = os.path.join(MONITOR_FOLDER, filename)
                if os.path.isfile(filepath):
                    current_files.append(filepath)
                    current_hash = calculate_sha512(filepath)
                    
                    if filepath not in saved_baseline:
                        print(f"\n[ALERT] New file detected: {filepath}")
                        saved_baseline[filepath] = current_hash # Add to memory to prevent spam
                    elif saved_baseline[filepath] != current_hash:
                        print(f"\n[ALERT] File modified (Hash mismatch): {filepath}")
                        saved_baseline[filepath] = current_hash
            
            # Check for deleted files
            for saved_file in list(saved_baseline.keys()):
                if saved_file not in current_files:
                    print(f"\n[ALERT] File deleted: {saved_file}")
                    del saved_baseline[saved_file]
                    
    except KeyboardInterrupt:
        print("\n[+] Monitoring stopped by user.")

if __name__ == "__main__":
    print("Sentinel File Integrity Monitor")
    print("1. Create new baseline")
    print("2. Monitor files against baseline")
    
    choice = input("Select an option (1 or 2): ")
    
    if choice == '1':
        create_baseline()
    elif choice == '2':
        monitor_integrity()
    else:
        print("[-] Invalid choice.")
