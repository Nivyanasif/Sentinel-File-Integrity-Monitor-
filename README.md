# Sentinel File Integrity Monitor (FIM)

## Overview
Sentinel is a lightweight, Python-based File Integrity Monitor. It utilizes SHA-512 cryptographic hashing to establish a known-good baseline of a directory and continuously monitors for unauthorized changes. 

In enterprise environments, FIM is a critical security control (NIST SP 800-53 SI-7) used to detect ransomware, unauthorized configuration changes, and insider threats.

## Features
- **SHA-512 Hashing:** Uses strong cryptographic algorithms to ensure file integrity.
- **Baseline Generation:** Creates a JSON-based snapshot of the directory's secure state.
- **Continuous Monitoring:** Detects and alerts on:
  - File modifications (Hash mismatches)
  - Newly dropped files
  - Deleted files

## How to Run It
1. Clone this repository.
2. Ensure you have Python 3 installed. No external libraries are required.
3. Run the script: `python sentinel_fim.py`
4. Select `1` to generate a baseline.
5. Select `2` to begin monitoring.
6. Open the `target_folder` and create, modify, or delete text files to see the real-time security alerts in your terminal.

## Use Case in Cyber Operations
Security Operations Center (SOC) analysts and system administrators use tools like this to monitor critical system files (like `/etc/shadow` on Linux or `System32` on Windows). If a threat actor breaches a server and alters a configuration file to establish persistence, the FIM instantly flags the **anomalous** [deviating from what is standard or normal] behavior so the defense team can **remediate** [to fix or cure something] the threat.
