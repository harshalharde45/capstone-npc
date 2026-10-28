# Evidence Repository & Experimental Artifacts

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## Directory Overview

This directory stores primary laboratory evidence gathered during the dynamic and static analysis of the safe bind-shell simulation inside the isolated Linux guest environment.

```
evidence/
|-- README.md
|-- screenshots/          # Figure 01 through Figure 16 verification captures
|-- logs/                 # Terminal logs from ps, ss, lsof, and shell interactions
|-- packet_captures/      # Loopback tcpdump captures (loopback_evidence.pcap)
```

## Subdirectory Structure & Purpose

1. **`screenshots/`**:
   Contains PNG captures matching the 16-point checklist detailed in `documentation/Screenshot_Checklist.md`. Each file is named systematically (`Figure_01_Host_Hypervisor_Specs.png` through `Figure_16_Post_Restoration_Verification.png`).
   
2. **`logs/`**:
   Text logs generated during command execution, process tracking, socket checks, and sandbox recovery audits.
   - `server_console.log`: Console logging of `server.py` startup and command processing.
   - `client_session.log`: Interactive session log from `client.py`.
   - `system_monitor_ss.log`: Socket state snapshot (`ss -tulpn`).
   - `process_tree_ps.log`: Process tree and user ownership (`ps -aux | grep python3`).

3. **`packet_captures/`**:
   Network traffic dumps captured exclusively on the loopback interface (`lo` / `127.0.0.1`) using `tcpdump -i lo -nn -s0 -w loopback_evidence.pcap`. Contains the TCP three-way handshake (`SYN`, `SYN-ACK`, `ACK`), command exchange packets, and connection teardown (`FIN-ACK`).

## Chain of Custody & Data Integrity

All files deposited in this evidence folder are hashed using SHA-256 upon generation to preserve forensic integrity and ensure reproducibility across academic evaluations.
