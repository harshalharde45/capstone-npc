# NPC Capstone Project Comprehensive Laboratory Report
## Malware Analysis Sandbox Using VirtualBox or VMware

---

### Academic Credential & Project Information

- **Student Full Name**: Harshal Bhagwan Harde
- **Permanent Registration Number (PRN)**: 2125UCSM1001
- **Degree Program**: Bachelor of Technology (B.Tech)
- **Department**: Department of Computer Science Engineering
- **Specialization**: Cyber Security
- **Institution**: Sanjivani University, Kopargaon
- **Academic Year**: 2026–2027
- **Course / Subject**: NPC
- **Project Type**: Capstone Project
- **Project Title**: Malware Analysis Sandbox Using VirtualBox or VMware
- **Repository**: `https://github.com/harshalharde45/capstone-npc.git`

---

## 1. Abstract

Dynamic malware analysis requires an isolated, instrumented, and easily recoverable computing environment to observe suspicious binary behavior without risking host contamination or network propagation. This Capstone Project details the architectural design, deployment, network containment, dynamic monitoring, and snapshot recovery of a dedicated Linux malware analysis sandbox built on Type-2 desktop virtualization (Oracle VM VirtualBox and VMware Workstation Pro). 

To ensure safety and ethical laboratory compliance, a custom, controlled bind-shell simulation was developed. The simulation binds strictly to the loopback interface (`127.0.0.1:54321`), accepts only predefined non-privileged query tokens (`STATUS`, `HELP`, `EXIT`), and explicitly rejects arbitrary operating system commands. System monitoring utilities (`ps`, `top`, `ss`, `lsof`, `stat`) and loopback packet capture (`tcpdump`) were deployed to analyze process states, socket allocations, and transmission frames. Cryptographic hashes (MD5, SHA-1, SHA-256) were computed to establish immutable baselines and cross-referenced against the VirusTotal threat intelligence database. Following analysis, the virtual machine was reverted to its pre-execution clean baseline snapshot (`NPC_Capstone_Clean_State`), and forensic audit commands verified complete eradication of runtime state. This project provides a robust, reproducible methodology for safe threat inspection in academic and operational security environments.

---

## 2. Project Objectives

The primary objectives of this Capstone Project are:
1. **Hypervisor Provisioning & Isolation**: Construct an isolated Linux virtual machine using Oracle VM VirtualBox or VMware Workstation, configured with zero Internet egress and hardened guest-isolation boundaries.
2. **Immutable Baseline Snapshotting**: Establish a golden baseline snapshot designated `NPC_Capstone_Clean_State` on a freshly provisioned, fully updated, uninfected virtual machine.
3. **Safe Simulation Development**: Implement a safe, local-only bind-shell simulation adhering to strict educational constraints (loopback-only binding, absence of `os.system` / `subprocess`, strict command filtering).
4. **Multi-Vector System Auditing**: Monitor the guest operating system during simulation runtime using Linux core utilities (`ss`, `lsof`, `ps`, `top`, `stat`) to identify process structures, socket states, and file descriptors.
5. **Network Packet Inspection**: Intercept and analyze loopback traffic frames using `tcpdump` to dissect the TCP three-way handshake, payload transmission, and teardown sequence.
6. **Cryptographic Identification & Threat Intelligence**: Generate MD5, SHA-1, and SHA-256 digests and perform an ethical hash-based query on VirusTotal, documenting results with academic integrity.
7. **Snapshot-Based Recovery & Forensic Verification**: Revert the virtual machine to `NPC_Capstone_Clean_State` and conduct a multi-point forensic audit proving complete state restoration.

---

## 3. Theoretical Background & Literature Review

### 3.1 Principles of Malware Analysis
Malware analysis is broadly divided into two complementary disciplines:
- **Static Analysis**: The examination of an executable without running it. It involves file header parsing, string extraction, disassembly, and cryptographic hashing. While static analysis is safe and fast, it is frequently impeded by code obfuscation, packing, and encryption.
- **Dynamic Analysis**: The real-time behavioral observation of a program as it executes in an operating system. Dynamic analysis records API calls, network connections, file modifications, and process creation. Because dynamic analysis exposes the execution host to potential harm, it must be performed inside an isolated sandbox.

### 3.2 Desktop Virtualization & Sandboxing Architecture
A sandbox is a tightly controlled security environment wherein untrusted code executes under close surveillance. Modern desktop sandboxes leverage Type-2 hypervisors running on top of a conventional host operating system. The hypervisor presents virtualized hardware (vCPUs, RAM, virtual storage controllers, and virtual network interface cards) to the guest operating system.

### 3.3 Virtual Machine Snapshots & Copy-on-Write (COW) Mechanics
Virtual machine snapshots enable point-in-time state preservation:
1. When the baseline snapshot (`NPC_Capstone_Clean_State`) is captured, the base virtual disk (`.vdi` or `.vmdk`) is locked as read-only.
2. A new differencing disk (delta file) is attached to the virtual machine.
3. All subsequent writes during malware execution are directed to the differencing disk.
4. When reverting to the snapshot, the hypervisor deletes the differencing disk and creates a fresh delta layer pointing back to the immutable base image.

### 3.4 Shell Architectures: Bind Shells vs Reverse Shells
- **Bind Shell**: The payload opens a listening socket on a designated port of the target host and waits for an inbound connection from the attacker.
- **Reverse Shell**: The payload initiates an outbound connection from the target host back to a listening port controlled by the attacker. In real-world attack scenarios, reverse shells are favored because they bypass stateful inbound firewalls and Network Address Translation (NAT). In our isolated laboratory, a local bind-shell simulation is preferred because it requires zero external network infrastructure and operates safely on the loopback interface.

---

## 4. Hardware Architecture & Virtual Machine Configuration

The virtual machine was provisioned with the following parameters:

| Resource Parameter | Allocated Specification | Technical Justification |
| :--- | :--- | :--- |
| **Virtual CPUs** | 2 vCPUs | Supports concurrent monitoring scripts without overwhelming host CPU |
| **System Memory** | 4,096 MB (4.0 GB) | Ample memory for Linux kernel, socket buffers, and caching |
| **Virtual Disk** | 30.0 GB Dynamic VDI/VMDK | Sufficient disk space for OS packages, logs, and snapshot delta trees |
| **Guest OS** | Ubuntu Linux 22.04 LTS (64-bit) | Standardized enterprise distribution with complete diagnostic tools |
| **Network Adapter** | Not Attached / Disconnected | Enforces physical and virtual network air-gapping |
| **Shared Folders** | Disabled | Prevents cross-filesystem contamination and unauthorized file tampering |
| **Shared Clipboard** | Disabled | Prevents clipboard leakage across host-guest boundary |
| **Drag & Drop** | Disabled | Mitigates accidental binary transfer |

---

## 5. Network Isolation Implementation & Verification

### 5.1 The Loopback Security Boundary
Under RFC 1122 Section 3.2.1.3, the IPv4 address block `127.0.0.0/8` is designated as the loopback network. Packets sent to `127.0.0.1` are processed entirely by the local kernel network stack. They are never transmitted over physical network links, external virtual switches, or wireless interfaces. Binding the simulation server strictly to `127.0.0.1` guarantees complete local confinement.

### 5.2 Pre-Flight Isolation Verification Suite
To confirm that the guest machine cannot communicate with external networks, four verification checks were executed:
1. `ip route show` returned no default gateway.
2. `ping -c 3 8.8.8.8` returned `connect: Network is unreachable` (100% loss).
3. `ping -c 3 google.com` returned `Temporary failure in name resolution`.
4. `curl -I https://www.google.com` returned `curl: (6) Could not resolve host`.

---

## 6. Clean Baseline Snapshot: `NPC_Capstone_Clean_State`

Prior to introducing any experimental scripts, the virtual machine was placed into an immutable clean baseline:
- **Designated Snapshot Name**: `NPC_Capstone_Clean_State`
- **Creation Timing**: Generated after OS installation, system updating, and analysis toolchain deployment, with network adapters unattached and temporary directories purged.
- **Role**: Serves as the golden recovery anchor for all subsequent dynamic experiments.

---

## 7. Safe Shell Simulation: Architecture & Implementation

### 7.1 Design Constraints & Safety Boundaries
In accordance with ethical laboratory safeguards:
- **Strict Loopback Binding**: Sockets bind exclusively to `127.0.0.1:54321`.
- **Zero OS Command Execution**: The simulation does not invoke `os.system`, `subprocess`, `pty`, `eval`, or `exec`.
- **Strict Command Allowlisting**: Only three commands are parsed:
  - `STATUS`: Returns server uptime, bound interface, and active security policies.
  - `HELP`: Displays permitted commands.
  - `EXIT`: Closes connection gracefully.
- **Arbitrary Command Rejection**: Any command outside the allowlist (e.g., `whoami`, `cat /etc/passwd`) is rejected with an explicit security alert banner.
- **Signal Handling**: Catches `SIGINT` (Ctrl+C) to release socket bindings cleanly.

---

## 8. Cryptographic File Hashing & Identification

Standard cryptographic digests were computed on the simulation scripts:

| File Name | Path | Size | MD5 | SHA-1 | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `server.py` | `lab/safe_shell_simulation/server.py` | 6,119 B | `21199ab7631c9e5980f5ea130066dfc9` | `f16d4c237857271467c36b26ebaff73ba56bec78` | `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f` |
| `client.py` | `lab/safe_shell_simulation/client.py` | 3,255 B | `8b12014191ba695f2d1668313b4d72df` | `a6af278ad686b2e92d468413a918b069e39dd01d` | `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10` |

---

## 9. VirusTotal Threat Intelligence Investigation

In compliance with academic honesty and operational security:
- **Investigation Method**: SHA-256 hash query (`8864d0fbd383...` and `6a774332f04...`).
- **Official Finding**:  
  > **"No existing VirusTotal report was available for the investigated file at the time of analysis."**
- **Analysis**:
  - The files were custom-authored by Harshal Bhagwan Harde for this capstone project.
  - Because they have never been distributed or submitted to multi-scanner repositories, no historical detection signatures or behavioral telemetry exist in VirusTotal.
  - This demonstrates why local sandbox analysis is critical when investigating novel, proprietary, or targeted software.

---

## 10. Dynamic System Monitoring & Traffic Analysis

### 10.1 Socket Inspection (`ss` & `lsof`)
Execution of `ss -tulpn | grep 54321` revealed:
```
tcp  LISTEN  0  5  127.0.0.1:54321  0.0.0.0:*  users:(("python3",pid=14205,fd=3))
```
Execution of `lsof -i TCP:54321` confirmed that file descriptor 3 was allocated to the IPv4 TCP listening socket under user `harshal`.

### 10.2 Process Table Inspection (`ps` & `top`)
`ps -aux | grep server.py` showed process execution under PID 14205 with CPU usage under 0.2% and resident memory under 0.4%, verifying lightweight, non-destructive execution.

### 10.3 Loopback Packet Sniffing (`tcpdump`)
`tcpdump -i lo port 54321 -nn -s0 -w loopback_evidence.pcap` captured:
1. TCP 3-Way Handshake (`SYN`, `SYN-ACK`, `ACK`).
2. Server Welcome Banner transmission (`PSH-ACK`).
3. Interactive command exchanges for `STATUS` and `HELP`.
4. Command rejection alert for unauthorized input.
5. TCP Connection teardown (`FIN-ACK`, `ACK`).

---

## 11. Comprehensive Observation Matrix

| Test Item | Command / Procedure | Expected Result | Observed Finding | Status |
| :--- | :--- | :--- | :--- | :--- |
| **VM Hardware** | VM Settings | 2 vCPUs, 4 GB RAM, 30 GB disk | 2 vCPUs, 4096 MB RAM, 30 GB VDI allocated | **PASSED** |
| **Network Isolation** | `ping 8.8.8.8` / `curl` | Egress blocked; network unreachable | Complete packet loss; unreachable network | **PASSED** |
| **Clean Snapshot** | `VBoxManage snapshot take` | `NPC_Capstone_Clean_State` created | Baseline snapshot established | **PASSED** |
| **Server Startup** | `python3 server.py` | Binds to 127.0.0.1:54321 | Active listening socket created | **PASSED** |
| **Socket Audit** | `ss -tulpn` | LISTEN state on port 54321 | Socket confirmed under python3 PID 14205 | **PASSED** |
| **Process Audit** | `ps -aux` | User-space Python process | Clean process table entry; no privilege escalation | **PASSED** |
| **File Descriptors** | `lsof -i TCP:54321` | Socket bound to FD 3 | Confirmed file descriptor allocation | **PASSED** |
| **Packet Capture** | `tcpdump -i lo` | Captures TCP handshake and payloads | Full 14-frame session captured to PCAP | **PASSED** |
| **Client Interaction**| `python3 client.py` | Connects and executes commands | STATUS and HELP processed correctly | **PASSED** |
| **Security Filter** | Input `whoami` | Rejects arbitrary commands | Returned SECURITY ALERT; zero OS execution | **PASSED** |
| **Cryptographic Hash**| `sha256sum` | Accurate SHA-256 digests | Matched cryptographic baseline digests | **PASSED** |
| **Threat Intelligence**| VirusTotal Hash Query | Accurate report documentation | "No existing VirusTotal report was available" | **PASSED** |
| **Snapshot Restore**| `VBoxManage snapshot restore`| Reverts to clean baseline | VM restored to `NPC_Capstone_Clean_State` | **PASSED** |
| **Post-Restore Audit**| `ss`, `ps`, `stat` | Zero remnant sockets or files | Complete eradication of experimental state | **PASSED** |

---

## 12. Snapshot Restoration & Post-Recovery Audit

Following completion of data capture:
1. The virtual machine was restored to `NPC_Capstone_Clean_State`.
2. Post-restoration verification commands confirmed:
   - `ss -tulpn | grep 54321` returned **empty** (no active listening port).
   - `ps -aux | grep server.py` returned **empty** (no residual process).
   - `/tmp` directory inspection showed zero leftover simulation artifacts.
   - Core binary hashes (`/bin/bash`, `/usr/bin/python3`) remained unchanged.

---

## 13. Forensic Limitations of Virtualization & Snapshots

1. **Shared Folders**: Reverting a snapshot does not restore files modified inside shared host directories.
2. **Hypervisor Escapes**: Flaws in hypervisor virtualization extensions can theoretically allow advanced malware to break containment.
3. **Live RAM Snapshots**: Restoring live memory snapshots can retain rootkits if the snapshot was taken while malware was dormant in RAM.

---

## 14. Real-World Applications in Cyber Security

- **Automated Sandbox Pipelines**: Foundation for enterprise systems like Cuckoo Sandbox, CAPEv2, and Joe Sandbox.
- **Incident Response**: Rapid triage of unknown attachments without risking enterprise networks.
- **Vulnerability Research**: Observing crash states and exploit payloads in contained environments.

---

## 15. Conclusion

This Capstone Project successfully demonstrated the design, containment, dynamic behavioral analysis, and snapshot recovery of a Linux malware analysis sandbox. By combining hypervisor isolation with an ethically engineered simulation, complete operational visibility was achieved while strictly upholding safety protocols. The snapshot recovery mechanism proved 100% effective in returning the system to its baseline state, establishing a rigorous framework for future cybersecurity research.

---

## 16. Academic References

1. Sikorski, M., & Honig, A. (2012). *Practical Malware Analysis*. No Starch Press.
2. Ligh, M. H., et al. (2014). *The Art of Memory Forensics*. John Wiley & Sons.
3. NIST SP 800-86 (2008). *Guide to Integrating Forensic Techniques into Incident Response*.
4. NIST SP 800-61 Rev. 2 (2012). *Computer Security Incident Handling Guide*.
5. MITRE ATT&CK Enterprise Matrix (2026). Techniques T1059, T1071, T1571.
6. RFC 1122 (1989). *Requirements for Internet Hosts - Communication Layers*.
7. Oracle VM VirtualBox User Manual & VMware Workstation Pro Documentation (2026).

---

## 17. Appendices: 16-Point Evidentiary Figures

- **Figure 01**: Host Hypervisor Specifications & Hardware Allocation
- **Figure 02**: Network Adapter Configuration (Disconnected / Not Attached)
- **Figure 03**: Guest OS Hardening Settings (Shared Folders & Clipboard Disabled)
- **Figure 04**: Pre-Flight Network Isolation Verification (`ping` & `curl` failure tests)
- **Figure 05**: Clean Baseline Snapshot Creation (`NPC_Capstone_Clean_State`)
- **Figure 06**: Static File Identification & Code Inspection (`file`, `wc`, `grep`)
- **Figure 07**: Cryptographic Hash Generation (`md5sum`, `sha1sum`, `sha256sum`)
- **Figure 08**: VirusTotal Threat Intelligence Hash Investigation
- **Figure 09**: Safe Bind-Shell Simulation Server Startup (`server.py` console banner)
- **Figure 10**: Listening Socket Verification (`ss -tulpn` & `lsof -i TCP:54321`)
- **Figure 11**: Active Process Inspection & Resource Monitoring (`ps -aux` & `top`)
- **Figure 12**: Loopback Packet Capture Initialization (`tcpdump -i lo port 54321`)
- **Figure 13**: Interactive Client Connection & Permitted Commands (`STATUS`, `HELP`)
- **Figure 14**: Security Boundary Enforcement (Arbitrary Command Rejection Alert)
- **Figure 15**: Snapshot Restoration Execution (`VBoxManage snapshot restore`)
- **Figure 16**: Post-Restoration System State Audit (Zero listening ports, clean process table)
