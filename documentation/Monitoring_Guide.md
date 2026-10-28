# System Monitoring & Dynamic Behavioral Analysis Guide

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Introduction to Dynamic Behavioral Monitoring

Dynamic malware analysis observes the behavior of an untrusted artifact in a controlled execution environment. While static analysis inspects source code, headers, and binary strings, dynamic analysis captures live system interactions, including:
- Process spawning and parent-child process hierarchies.
- Network socket allocation, binding, and listening states.
- File descriptor allocation and open file handles.
- Memory and processor resource consumption.
- File system modifications and timestamp alterations.

---

## 2. Core Linux Analysis Utilities & Command Guide

### 2.1 Process Table Inspection: `ps` & `top`

Malicious shells frequently hide within existing processes, disguise themselves under system daemon names (e.g., `kworker`, `systemd-resolved`), or spawn detached background daemons.

```bash
# Capture full process tree with command-line arguments and user context
ps -auxf | grep -E "server\.py|python3"

# Monitor real-time processor and memory utilization
top -b -n 1 | head -n 25
```

**Key Forensic Metrics Observed:**
- **PID / PPID**: Identifies process ID and parent process ID (verifying execution origin).
- **USER**: Verifies least privilege (ensuring simulation does not run as `root`).
- **%CPU / %MEM**: Tracks abnormal resource spikes (identifying cryptominers or runaway loops).
- **STAT**: Process execution state (`S` for interruptible sleep waiting on network socket, `R` for running).

---

### 2.2 Socket & Network Table Inspection: `ss` & `netstat`

Backdoors and bind shells open listening ports to receive remote connections. In modern Linux distributions, `ss` (Socket Statistics) interfaces directly with the Linux kernel's `sock_diag` netlink subsystem, providing faster and more detailed socket dumps than legacy `netstat`.

```bash
# List all listening TCP sockets with associated process names and PIDs
ss -tulpn

# Filter specifically for the simulation port
ss -tulpn | grep 54321

# Inspect active established connections in real time
ss -tan state established
```

**Output Fields Analyzed:**
- **Netid**: Protocol family (`tcp`).
- **State**: TCP state (`LISTEN` when waiting for client; `ESTAB` during interactive exchange).
- **Local Address:Port**: `127.0.0.1:54321` (confirming loopback isolation).
- **Peer Address:Port**: Destination socket (e.g., `127.0.0.1:48212`).
- **Process**: Kernel process association: `users:(("python3",pid=14205,fd=3))`.

---

### 2.3 Open File Descriptors & Sockets: `lsof`

In Unix, "everything is a file." Network sockets, pipes, device drivers, and disk files are managed via file descriptors. The `lsof` utility reveals every resource held open by the suspicious process.

```bash
# List all files, libraries, and network sockets opened by the simulation server
lsof -p $(pgrep -f "server.py")

# Filter exclusively for network file descriptors opened by Python
lsof -i TCP:54321
```

**Sample Forensic Output:**
```
COMMAND     PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3   14205 harshal  cwd    DIR    8,1     4096 1315 /home/harshal/lab
python3   14205 harshal  rtd    DIR    8,1     4096    2 /
python3   14205 harshal  txt    REG    8,1  5487848  912 /usr/bin/python3.10
python3   14205 harshal    3u  IPv4  38492      0t0  TCP 127.0.0.1:54321 (LISTEN)
```

---

### 2.4 File System Inode & Timestamp Inspection: `stat`

Malware often modifies system files or engages in "timestomping" (altering access or modification timestamps to blend in with legitimate system binaries). The `stat` utility reveals exact filesystem metadata:

```bash
# Inspect file attributes, permissions, and timestamps
stat lab/safe_shell_simulation/server.py
```

**Attributes Verified:**
- **Size & Blocks**: Accurate disk footprint.
- **Access / Modify / Change / Birth (MACB)**: Exact forensic timestamps down to the nanosecond.
- **Inode Number**: Confirms whether a file was modified in place or replaced by an attacker.

---

### 2.5 Cryptographic Verification: `sha256sum`

Cryptographic integrity must be verified before and after execution to ensure no self-modifying code or on-disk tampering occurred:

```bash
sha256sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
```
