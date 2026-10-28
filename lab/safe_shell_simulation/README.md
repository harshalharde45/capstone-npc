# Safe Bind-Shell Simulation Specification

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Author**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  
**Component**: Educational Controlled Simulation Module  

---

## 1. Executive Summary & Purpose

In traditional malware analysis education, demonstrating backdoor behavior (such as reverse shells or bind shells) is essential for understanding process creation, listening sockets, and command-and-control (C2) paradigms. However, real-world shells execute arbitrary shell commands via system calls (`/bin/sh`, `execve`, `cmd.exe`), posing significant security risks if mishandled.

To satisfy the **NPC Capstone Project** requirements with absolute safety, this module provides an **educational bind-shell simulation**:
1. It creates an active TCP listening socket that can be detected by system monitoring tools (`ss`, `netstat`, `lsof`).
2. It accepts local TCP connections, allowing network inspection (`tcpdump`, `Wireshark`).
3. It spawns an active user-space process (`server.py`), allowing process tree analysis (`ps`, `top`).
4. **Safety Boundary**: It completely excludes arbitrary operating system command execution. It possesses no capability to run shell commands, access file system binaries, or alter system state.

---

## 2. Cryptographic Hashes & File Attributes

| Attribute | `server.py` | `client.py` |
| :--- | :--- | :--- |
| **File Type** | Python 3 script (ASCII text) | Python 3 script (ASCII text) |
| **File Size** | 6,119 bytes | 3,255 bytes |
| **MD5** | `21199ab7631c9e5980f5ea130066dfc9` | `8b12014191ba695f2d1668313b4d72df` |
| **SHA-1** | `f16d4c237857271467c36b26ebaff73ba56bec78` | `a6af278ad686b2e92d468413a918b069e39dd01d` |
| **SHA-256** | `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f` | `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10` |

---

## 3. Architecture & Functional Specification

### 3.1 Network Binding Rules
- **Interface**: Strictly bound to `127.0.0.1` (IPv4 loopback).
- **Port**: Non-privileged high port `54321`.
- **Packet Scope**: Packets never touch physical or virtual network adapters connected to outside networks.
- **Access Control**: Rejects any incoming packets if the client IP address is not `127.0.0.1`.

### 3.2 Command Processing Matrix

```
Client Input ------> [ Command Validator ]
                           |
            +--------------+--------------+
            |              |              |
         STATUS          HELP           EXIT      ANY OTHER STRING
            |              |              |              |
      [Uptime/State] [Usage Info]  [Graceful Quit]   [REJECT ALERT]
            |              |              |          (No OS Exec)
            +--------------+--------------+--------------+
                           |
                    Client Socket
```

- **`STATUS`**: Returns formatted JSON/text string reporting uptime, listening socket coordinates, and safety constraints.
- **`HELP`**: Outputs the educational command reference.
- **`EXIT`**: Initiates a graceful socket closure and session termination.
- **Arbitrary Strings (e.g., `whoami`, `cat /etc/passwd`, `rm -rf /`)**: Evaluated purely as text tokens; no execution takes place. Returned message explicitly warns: `REJECTED: Arbitrary command execution is disabled by design.`

---

## 4. Execution & Verification Guide

### Step 1: Start the Server (Terminal 1)
```bash
python3 server.py
```
*Expected Output:*
```
======================================================================
NPC Capstone: Safe Bind-Shell Simulation Server
Student: Harshal Bhagwan Harde | PRN: 2125UCSM1001
Binding strictly to loopback 127.0.0.1:54321...
======================================================================
[+] Server successfully listening on 127.0.0.1:54321
[+] Waiting for connection from local simulation client...
[*] Press Ctrl+C at any time to shut down the server safely.
```

### Step 2: Start Packet Capture (Terminal 2)
```bash
sudo tcpdump -i lo port 54321 -nn -s0 -w evidence/packet_captures/loopback_evidence.pcap
```

### Step 3: Run the Client (Terminal 3)
```bash
python3 client.py
```
*Sample Interactive Session:*
```
SAFE-SANDBOX> HELP
[HELP GUIDE]
  STATUS - Query sandbox simulation daemon status and uptime
  HELP   - Display permitted commands and safety boundaries
  EXIT   - Terminate current simulation connection

SAFE-SANDBOX> STATUS
[STATUS RESPONSE]
[*] State             : ACTIVE_SIMULATION_LISTENING
[*] Bound Interface   : 127.0.0.1:54321 (Loopback Only)
[*] Active Client     : 127.0.0.1:48212
[*] Server Uptime     : 14 seconds
[*] Security Policy   : Strict Allowlist (STATUS, HELP, EXIT)
[*] Arbitrary Exec    : DISABLED (Zero subprocess / Zero shell)

SAFE-SANDBOX> whoami
[SECURITY ALERT]
[-] REJECTED COMMAND: 'whoami'
[-] Reason: Arbitrary command execution is disabled by design.
[-] Allowed commands: STATUS, HELP, EXIT.

SAFE-SANDBOX> EXIT
[EXIT NOTICE] Session termination requested. Closing connection.
```

### Step 4: Stop Server
Press `Ctrl+C` in Terminal 1. The server catches `SIGINT`, unbinds the port, and exits cleanly.
