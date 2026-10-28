# Static File Identification & Analysis

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Overview of Investigated Artifacts

In this sandbox laboratory experiment, two scripts were developed and investigated under static and dynamic analysis:
1. `lab/safe_shell_simulation/server.py`: The listening simulation server (bind-shell simulation).
2. `lab/safe_shell_simulation/client.py`: The diagnostic client communicating exclusively over loopback.

---

## 2. Detailed File Identification Matrix

| Property | `server.py` | `client.py` |
| :--- | :--- | :--- |
| **Full File Path** | `lab/safe_shell_simulation/server.py` | `lab/safe_shell_simulation/client.py` |
| **MIME Type** | `text/x-python` (ASCII text, with LF line terminators) | `text/x-python` (ASCII text, with LF line terminators) |
| **File Format** | Python 3 source script | Python 3 source script |
| **File Size (Bytes)** | 6,119 bytes | 3,255 bytes |
| **Line Count** | 134 lines | 81 lines |
| **Encoding** | UTF-8 / US-ASCII | UTF-8 / US-ASCII |
| **Interpreter Prerequisite**| Python 3.8+ (`/usr/bin/env python3`) | Python 3.8+ (`/usr/bin/env python3`) |
| **External Dependencies** | None (100% Python Standard Library) | None (100% Python Standard Library) |
| **Standard Library Modules**| `socket`, `sys`, `signal`, `datetime`, `time` | `socket`, `sys` |

---

## 3. Static Code & Capability Review

A rigorous static inspection was performed to verify compliance with laboratory safety constraints:

### 3.1 Prohibited System Call Inspection
- **`os.system`**: ABSENT. Neither script imports `os` nor invokes system commands.
- **`subprocess.Popen` / `subprocess.run`**: ABSENT. No child processes are spawned.
- **`pty` / `tty`**: ABSENT. No pseudo-terminals are allocated.
- **`eval` / `exec`**: ABSENT. Dynamic code evaluation is non-existent.
- **File System Alteration**: Neither script opens files for write operations (`open(..., 'w')` is absent). No persistence files (`/etc/cron.*`, `~/.bashrc`, `/etc/systemd/system`) are modified.

### 3.2 Network Behavior Capabilities
- **Listening Socket**: `server.py` creates an `AF_INET` `SOCK_STREAM` (TCP) socket.
- **Interface Restriction**: Hardcoded to `127.0.0.1` (`HOST = "127.0.0.1"`). It does NOT bind to `0.0.0.0` or external network cards (`eth0`, `ens33`).
- **Access Control Filter**: Implements an explicit check on accepted connections (`if addr[0] != "127.0.0.1": conn.close()`).
- **Command Whitelist**: Pure string comparisons against tokens: `STATUS`, `HELP`, and `EXIT`.
- **Default Action for Unknown Input**: Emits a security alert string over the socket rejecting arbitrary input. No execution occurs.

---

## 4. Linux Utility Verification Commands

To verify file attributes independently inside the Linux VM, the following commands are executed:

```bash
# Verify file type and encoding
file lab/safe_shell_simulation/server.py
file lab/safe_shell_simulation/client.py

# Verify line, word, and character counts
wc lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py

# Verify binary or prohibited symbols (returns empty)
grep -E "os\.system|subprocess|pty|eval|exec" lab/safe_shell_simulation/*.py
```
