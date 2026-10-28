# 16-Point Laboratory Screenshot Checklist & Verification Guide

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Overview & Verification Standard

This checklist details the 16 evidentiary figures required to document the complete sandbox lifecycle, from initial hypervisor provisioning to dynamic monitoring, packet capture, and snapshot recovery. 

For each figure, this guide provides the exact terminal command or GUI navigation path, the expected visual state, and the forensic rationale.

---

## 2. Detailed 16-Point Screenshot Specification

### Figure 01: Hypervisor Specifications & Hardware Allocation
- **Target File**: `evidence/screenshots/Figure_01_Host_Hypervisor_Specs.png`
- **Navigation**: VirtualBox / VMware VM Settings -> System & Processor tab.
- **Visual Proof**: Displays VM Name (`NPC_Malware_Sandbox`), Base Memory (4096 MB RAM), and Processors (2 vCPUs).
- **Forensic Rationale**: Verifies resource constraints and prevents host starvation during analysis.

### Figure 02: Network Isolation Setting (Disconnected / Not Attached)
- **Target File**: `evidence/screenshots/Figure_02_Network_Adapter_Isolation.png`
- **Navigation**: VM Settings -> Network tab.
- **Visual Proof**: Shows Network Adapter 1 set to `Not Attached` or `Disconnected`.
- **Forensic Rationale**: Proves the virtual machine has no physical or virtual network path to the LAN or Internet.

### Figure 03: Guest Isolation & Hardening Settings
- **Target File**: `evidence/screenshots/Figure_03_Guest_Hardening_Isolation.png`
- **Navigation**: VM Settings -> General -> Advanced (Shared Clipboard & Drag'n'Drop disabled) AND Shared Folders (None).
- **Visual Proof**: Shared Folders table is empty; clipboard and drag-and-drop are set to `Disabled`.
- **Forensic Rationale**: Verifies elimination of host-guest shared file pathways and clipboard leakage vectors.

### Figure 04: Pre-Flight Network Isolation Verification
- **Target File**: `evidence/screenshots/Figure_04_Preflight_Network_Isolation.png`
- **Command**:
  ```bash
  ip route show; ping -c 2 8.8.8.8; curl -I https://www.google.com
  ```
- **Visual Proof**: Terminal displays `connect: Network is unreachable` and `Could not resolve host`.
- **Forensic Rationale**: Concrete runtime proof that guest OS cannot communicate with external networks.

### Figure 05: Clean Baseline Snapshot Creation (`NPC_Capstone_Clean_State`)
- **Target File**: `evidence/screenshots/Figure_05_Clean_Snapshot_Creation.png`
- **Navigation / Command**: Hypervisor Snapshots pane showing `NPC_Capstone_Clean_State` created on clean baseline.
  ```bash
  VBoxManage snapshot "NPC_Malware_Sandbox" list
  ```
- **Visual Proof**: Snapshot tree displays `NPC_Capstone_Clean_State` with creation timestamp.
- **Forensic Rationale**: Establishes the immutable baseline prior to running any untrusted simulation code.

### Figure 06: Static File Identification & Code Inspection
- **Target File**: `evidence/screenshots/Figure_06_Static_File_Identification.png`
- **Command**:
  ```bash
  file lab/safe_shell_simulation/*.py; wc lab/safe_shell_simulation/*.py
  ```
- **Visual Proof**: Shows Python 3 text script format, line counts (134 and 81 lines), and byte sizes.
- **Forensic Rationale**: Documents static file characteristics before runtime invocation.

### Figure 07: Cryptographic Hash Generation
- **Target File**: `evidence/screenshots/Figure_07_Cryptographic_Hashing.png`
- **Command**:
  ```bash
  sha256sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
  ```
- **Visual Proof**: Terminal displays SHA-256 hashes:
  - `server.py`: `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f`
  - `client.py`: `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10`
- **Forensic Rationale**: Generates unambiguous cryptographic fingerprints for threat intelligence cross-referencing.

### Figure 08: VirusTotal Threat Intelligence Hash Investigation
- **Target File**: `evidence/screenshots/Figure_08_VirusTotal_Hash_Lookup.png`
- **Navigation**: Web browser at `virustotal.com/gui/file/<sha256>`.
- **Visual Proof**: Search bar contains SHA-256 hash; UI displays "No results found" or "Item not found".
- **Forensic Rationale**: Documents public threat status honestly without fabricating scores or uploading code.

### Figure 09: Safe Bind-Shell Simulation Server Startup
- **Target File**: `evidence/screenshots/Figure_09_Simulation_Server_Startup.png`
- **Command**:
  ```bash
  python3 lab/safe_shell_simulation/server.py
  ```
- **Visual Proof**: Terminal displays initialization banner, student name (Harshal Bhagwan Harde), PRN (2125UCSM1001), and listening notice on `127.0.0.1:54321`.
- **Forensic Rationale**: Proves simulation server process initialized cleanly within sandbox memory.

### Figure 10: Listening Socket Verification
- **Target File**: `evidence/screenshots/Figure_10_Listening_Socket_Audit.png`
- **Command**:
  ```bash
  ss -tulpn | grep 54321; sudo lsof -i TCP:54321
  ```
- **Visual Proof**: Displays `tcp LISTEN 127.0.0.1:54321` under process `python3` with PID and file descriptor 3.
- **Forensic Rationale**: Confirms socket is bound strictly to loopback and listening for connections.

### Figure 11: Active Process Inspection & Resource Monitoring
- **Target File**: `evidence/screenshots/Figure_11_Process_Resource_Monitoring.png`
- **Command**:
  ```bash
  ps -aux | grep server.py | grep -v grep; top -b -n 1 | head -n 15
  ```
- **Visual Proof**: Displays process ID, memory/CPU consumption, user ownership (`harshal`), and execution state.
- **Forensic Rationale**: Verifies absence of runaway processes, unauthorized root privileges, or daemon masquerading.

### Figure 12: Loopback Packet Capture Initialization
- **Target File**: `evidence/screenshots/Figure_12_Loopback_Packet_Capture.png`
- **Command**:
  ```bash
  sudo tcpdump -i lo port 54321 -nn -v
  ```
- **Visual Proof**: Terminal displays `tcpdump: listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes`.
- **Forensic Rationale**: Validates network sniffer is actively intercepting loopback traffic for behavioral PCAP logging.

### Figure 13: Interactive Client Connection & Permitted Commands
- **Target File**: `evidence/screenshots/Figure_13_Client_Allowed_Commands.png`
- **Command**:
  ```bash
  python3 lab/safe_shell_simulation/client.py
  ```
- **Visual Proof**: Client connects to `127.0.0.1:54321`; executes `HELP` and `STATUS`; displays server uptime and state.
- **Forensic Rationale**: Demonstrates legitimate socket communication without arbitrary execution.

### Figure 14: Security Boundary Enforcement (Arbitrary Command Rejection)
- **Target File**: `evidence/screenshots/Figure_14_Security_Boundary_Rejection.png`
- **Command**: Client attempts `whoami`, `cat /etc/shadow`, or `uname -a`.
- **Visual Proof**: Client receives explicit `[SECURITY ALERT] REJECTED COMMAND` banner. No shell executed.
- **Forensic Rationale**: Validates sandbox safety policy: arbitrary OS commands are completely rejected.

### Figure 15: Snapshot Restoration Execution
- **Target File**: `evidence/screenshots/Figure_15_Snapshot_Restoration.png`
- **Navigation / Command**: VirtualBox UI clicking **Restore Snapshot** on `NPC_Capstone_Clean_State`, OR:
  ```bash
  VBoxManage snapshot "NPC_Malware_Sandbox" restore "NPC_Capstone_Clean_State"
  ```
- **Visual Proof**: Hypervisor modal or terminal confirming restoration of virtual machine to clean baseline.
- **Forensic Rationale**: Documents the technical eradication of experimental state and differencing disk rollback.

### Figure 16: Post-Restoration System State Audit
- **Target File**: `evidence/screenshots/Figure_16_Post_Restoration_Verification.png`
- **Command**:
  ```bash
  ss -tulpn | grep 54321; ps -aux | grep server.py | grep -v grep
  ```
- **Visual Proof**: Terminal returns empty output (no listening ports, no running simulation processes).
- **Forensic Rationale**: Provides definitive proof that all runtime artifacts have been eradicated by snapshot recovery.
