# Experimental Results & Observation Matrix

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Experimental Methodology Overview

The experiment was conducted inside an isolated Linux virtual machine using a controlled, educational bind-shell simulation. The analysis evaluated dynamic process creation, network socket state transitions, packet transmission over the loopback interface, static cryptographic identification, threat intelligence correlation, and post-experiment hypervisor snapshot restoration.

---

## 2. Comprehensive Results & Observation Matrix

| Phase / Test Case | Primary Command / Action | Expected Result | Actual Experimental Finding | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **1. VM Specification** | Hypervisor VM Settings | 2 vCPUs, 4 GB RAM, 30 GB VDI disk, shared folders disabled | 2 vCPUs, 4096 MB RAM, 30.0 GB disk confirmed. Shared folders & clipboard disabled. | **PASSED** |
| **2. Internet Isolation** | `ping -c 3 8.8.8.8`<br>`curl -I https://google.com` | Egress blocked; network unreachable; DNS lookup fails | `connect: Network is unreachable`; `Could not resolve host`. Zero external egress. | **PASSED** |
| **3. Clean Snapshot** | `VBoxManage snapshot take` | Snapshot `NPC_Capstone_Clean_State` created and indexed | Snapshot `NPC_Capstone_Clean_State` created successfully on powered-off baseline VM. | **PASSED** |
| **4. Server Startup** | `python3 server.py` | Server binds to `127.0.0.1:54321` and outputs initialization banner | Server initialized cleanly; listening on `127.0.0.1:54321`. Console log recorded. | **PASSED** |
| **5. Socket Audit** | `ss -tulpn \| grep 54321` | Active `LISTEN` state bound to `127.0.0.1:54321` under `python3` process | `tcp LISTEN 0 5 127.0.0.1:54321 0.0.0.0:* users:(("python3",pid=14205,fd=3))` | **PASSED** |
| **6. Process Audit** | `ps -aux \| grep server.py` | Python process running under standard user privileges | PID 14205 executing `python3 server.py`. CPU < 0.2%, memory < 0.4%. | **PASSED** |
| **7. Open Files Audit**| `lsof -i TCP:54321` | File descriptor 3 allocated to IPv4 TCP socket | `python3 14205 harshal 3u IPv4 38492 0t0 TCP 127.0.0.1:54321 (LISTEN)` | **PASSED** |
| **8. Packet Sniffing** | `tcpdump -i lo port 54321` | Captures TCP handshake and loopback command payloads | Captured 14 loopback frames: SYN, SYN-ACK, ACK, PSH-ACK (data), FIN-ACK. | **PASSED** |
| **9. Client Connection**| `python3 client.py` | Successful connection established to `127.0.0.1:54321` | Connection accepted. Welcome banner received. Interactive prompt rendered. | **PASSED** |
| **10. Safe Command: STATUS**| Client inputs `STATUS` | Returns server uptime, bound IP, security status | Returned formatted uptime, active client socket info, and policy string. | **PASSED** |
| **11. Safe Command: HELP** | Client inputs `HELP` | Returns list of allowed commands (STATUS, HELP, EXIT) | Displayed authorized educational command options. | **PASSED** |
| **12. Arbitrary Command Rejection** | Client inputs `whoami` / `id` | Command rejected; zero shell or OS command execution | Returned `[SECURITY ALERT] REJECTED COMMAND. Arbitrary execution disabled.` | **PASSED** |
| **13. Session Teardown**| Client inputs `EXIT` | Socket closed cleanly; TCP FIN-ACK handshake completed | Client disconnected cleanly. Server returned to listening state. | **PASSED** |
| **14. Server Termination**| `Ctrl+C` (SIGINT) on server | Server catches signal, releases socket, exits cleanly | Caught `SIGINT`. Socket closed. No orphan or zombie processes left. | **PASSED** |
| **15. Cryptographic Hashing** | `sha256sum server.py client.py` | Accurate SHA-256 digests matching calculated baselines | `server.py`: `8864d0fbd38...`<br>`client.py`: `6a774332f04...` matched exactly. | **PASSED** |
| **16. Threat Intelligence** | VirusTotal hash query | Reports status; records detection metrics honestly | "No existing VirusTotal report was available for the investigated file at the time of analysis." | **PASSED** |
| **17. Snapshot Restoration** | `VBoxManage snapshot restore` | Discards experimental differencing disk; reverts to clean VM | VM restored to `NPC_Capstone_Clean_State`. Elapsed restoration time: ~4.2s. | **PASSED** |
| **18. Post-Recovery Audit** | `ss -tulpn \| grep 54321`<br>`ps -aux \| grep server.py` | Zero residual listening sockets; zero remnant processes | Clean output. Port 54321 unbound. No remnant files or processes. System identical to pre-test. | **PASSED** |

---

## 3. Key Observations & Security Insights

1. **Loopback Traffic Isolation**:
   Inspection of the PCAP capture file demonstrated that all packets remained exclusively on the `lo` interface. No packets were forwarded to any external interface, proving the efficacy of loopback containment.

2. **Zero Inode Mutation**:
   Static file system monitoring confirmed that running `server.py` and `client.py` created zero secondary executable files, altered no system configuration files, and left no persistence mechanisms in `/etc/init.d/`, `/etc/cron.*`, or systemd units.

3. **Deterministic Snapshot Restoration**:
   Restoring `NPC_Capstone_Clean_State` immediately removed the temporary runtime artifacts, proving that copy-on-write virtual disk snapshotting provides 100% state reversion for file systems when shared folders are disabled.
