# NPC Capstone Project: Malware Analysis Sandbox Using VirtualBox or VMware

[![Course](https://img.shields.io/badge/Course-B.Tech%20CSE%20Cyber%20Security-blue.svg)](https://sanjivani.edu.in)
[![PRN](https://img.shields.io/badge/PRN-2125UCSM1001-green.svg)](#student-information)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2026--2027-orange.svg)](#student-information)
[![Report](https://img.shields.io/badge/PDF%20Report-Download%20Report-red.svg)](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf)

---

## Student Information

| Parameter | Academic Detail |
| :--- | :--- |
| **Student Full Name** | **Harshal Bhagwan Harde** |
| **Permanent Registration Number (PRN)** | **2125UCSM1001** |
| **Course / Program** | Bachelor of Technology (B.Tech) |
| **Department** | Department of Computer Science Engineering |
| **Specialization** | Cyber Security |
| **University** | Sanjivani University, Kopargaon |
| **Academic Year** | 2026–2027 |
| **Subject / Module** | NPC |
| **Project Type** | Capstone Project |
| **Project Title** | **Malware Analysis Sandbox Using VirtualBox or VMware** |
| **Repository URL** | [https://github.com/harshalharde45/capstone-npc.git](https://github.com/harshalharde45/capstone-npc.git) |

---

## Primary Deliverables & Quick Links

- 📄 **Comprehensive PDF Report**: [report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf) *(Compiled University Submission)*
- 📝 **Markdown Report Source**: [report/report_source.md](report/report_source.md)
- 🔬 **Safe Bind-Shell Simulation Server**: [lab/safe_shell_simulation/server.py](lab/safe_shell_simulation/server.py)
- 💻 **Diagnostic Simulation Client**: [lab/safe_shell_simulation/client.py](lab/safe_shell_simulation/client.py)
- 🛡️ **Network Isolation Guide**: [documentation/Network_Isolation_Guide.md](documentation/Network_Isolation_Guide.md)
- 📸 **16-Point Screenshot Checklist**: [documentation/Screenshot_Checklist.md](documentation/Screenshot_Checklist.md)
- 🔄 **Snapshot Recovery Guide**: [documentation/Snapshot_Recovery_Guide.md](documentation/Snapshot_Recovery_Guide.md)
- 📊 **Results & Observation Matrix**: [documentation/Results_and_Observations.md](documentation/Results_and_Observations.md)
- 🔍 **VirusTotal Investigation**: [analysis/VirusTotal_Findings.md](analysis/VirusTotal_Findings.md)

---

## 1. Project Overview & Architecture

This Capstone Project provides a comprehensive, technically rigorous, and ethically contained framework for dynamic malware analysis inside an isolated Linux virtual machine using Oracle VM VirtualBox or VMware Workstation Pro. 

```
                                [ PHYSICAL HOST SYSTEM ]
                                           |
    +--------------------------------------+--------------------------------------+
    |                                                                             |
    |   [ Hypervisor Layer: Oracle VM VirtualBox / VMware Workstation Pro ]       |
    |                                                                             |
    |   +---------------------------------------------------------------------+   |
    |   |               GUEST LINUX VM (Ubuntu 22.04 LTS 64-bit)              |   |
    |   |                                                                     |   |
    |   |  Baseline Snapshot: [ NPC_Capstone_Clean_State ]                   |   |
    |   |                                                                     |   |
    |   |  +--------------------+                   +--------------------+    |   |
    |   |  | client.py          |                   | server.py          |    |   |
    |   |  | (Diagnostic Client)|                   | (Safe Bind-Shell)  |    |   |
    |   |  +---------+----------+                   +---------^----------+    |   |
    |   |            |                                        |               |   |
    |   |            +----------> [ Loopback: 127.0.0.1 ] ----+               |   |
    |   |                         (Port: 54321 / TCP)                         |   |
    |   |                                                                     |   |
    |   |  Network Hardware Adapter: [ NOT ATTACHED / FULLY DISCONNECTED ]    |   |
    |   +---------------------------------------------------------------------+   |
    |                                      X                                      |
    |                                      X (Air-Gapped: Zero Outbound Egress)   |
    +--------------------------------------+--------------------------------------+
                                           v
                        [ PHYSICAL LAN / INTERNET (BLOCKED) ]
```

### Safety and Ethical Safeguards
1. **Loopback Confinement**: The simulation daemon binds exclusively to `127.0.0.1:54321`. RFC 1122 Section 3.2.1.3 guarantees loopback traffic is processed entirely within the guest kernel and never transmitted across physical or virtual adapters.
2. **Zero Shell Execution**: The code completely avoids `os.system`, `subprocess`, `pty`, `eval`, or `exec`.
3. **Strict Whitelisting**: Only benign queries (`STATUS`, `HELP`, `EXIT`) are handled. Arbitrary OS commands (e.g., `whoami`, `cat /etc/shadow`) are rejected with security alerts.
4. **Air-Gapped Virtualization**: Network adapters are set to `Not Attached` / `Disconnected`, preventing worm dissemination or C2 communication.
5. **Immutable Snapshot Recovery**: The virtual machine is snapshot-protected under `NPC_Capstone_Clean_State`, enabling total state rollback.

---

## 2. Repository Directory Structure

```
.
|-- .gitignore
|-- README.md
|-- generate_pdf.py
|
|-- report/
|   |-- NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf
|   |-- report_source.md
|
|-- documentation/
|   |-- Lab_Setup_Guide.md
|   |-- Network_Isolation_Guide.md
|   |-- Snapshot_Recovery_Guide.md
|   |-- Monitoring_Guide.md
|   |-- VirusTotal_Analysis_Guide.md
|   |-- Results_and_Observations.md
|   |-- Screenshot_Checklist.md
|
|-- lab/
|   |-- README.md
|   |-- safe_shell_simulation/
|       |-- README.md
|       |-- server.py
|       |-- client.py
|
|-- evidence/
|   |-- README.md
|   |-- screenshots/
|   |-- logs/
|   |-- packet_captures/
|
|-- analysis/
|   |-- File_Identification.md
|   |-- Hash_Results.md
|   |-- VirusTotal_Findings.md
|
|-- references/
|   |-- References.md
|
|-- vm/
|   |-- README.md
```

---

## 3. Cryptographic Hashes & VirusTotal Investigation

| Artifact Name | Size | MD5 | SHA-1 | SHA-256 |
| :--- | :--- | :--- | :--- | :--- |
| `server.py` | 6,119 B | `21199ab7631c9e5980f5ea130066dfc9` | `f16d4c237857271467c36b26ebaff73ba56bec78` | `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f` |
| `client.py` | 3,255 B | `8b12014191ba695f2d1668313b4d72df` | `a6af278ad686b2e92d468413a918b069e39dd01d` | `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10` |

### VirusTotal Investigation Statement
In adherence to strict academic honesty and operational security:
> **Official Finding**:  
> **"No existing VirusTotal report was available for the investigated file at the time of analysis."**

Because these scripts were custom-authored for this capstone project by Harshal Bhagwan Harde and never distributed onto public multi-scanners, no prior detection record or threat telemetry exists. This finding demonstrates why dynamic local sandboxing is essential when analyzing novel or proprietary software.

---

## 4. Quickstart: Step-by-Step Laboratory Execution

### Step 1: Pre-Flight Network Verification
```bash
# Verify external network is completely unreachable
ip route show
ping -c 2 8.8.8.8
curl -I https://www.google.com
```

### Step 2: Establish Clean Baseline Snapshot
```bash
# In VirtualBox (with VM powered off):
VBoxManage snapshot "NPC_Malware_Sandbox" take "NPC_Capstone_Clean_State" --description "Clean baseline snapshot"
```

### Step 3: Run the Safe Bind-Shell Simulation
```bash
# Terminal 1: Launch listening server
python3 lab/safe_shell_simulation/server.py

# Terminal 2: Sniff loopback packets
sudo tcpdump -i lo port 54321 -nn -s0 -w evidence/packet_captures/loopback_evidence.pcap

# Terminal 3: Audit active socket and process
ss -tulpn | grep 54321
ps -aux | grep server.py

# Terminal 4: Connect interactive diagnostic client
python3 lab/safe_shell_simulation/client.py
```

### Step 4: Revert to Clean Snapshot
```bash
# Power off VM and revert
VBoxManage snapshot "NPC_Malware_Sandbox" restore "NPC_Capstone_Clean_State"
```

### Step 5: Post-Restoration Verification Audit
```bash
# Confirm zero remnant sockets or processes
ss -tulpn | grep 54321
ps -aux | grep server.py
```

---

## 5. Generating the PDF Report

The comprehensive university-grade PDF report can be recompiled at any time:
```bash
# Using Python with reportlab and pillow installed:
python generate_pdf.py

# Or using uv:
uv run --python 3.12 --with reportlab generate_pdf.py
```

---

## 6. Academic License & Declaration

This project is submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology (B.Tech) in Computer Science Engineering (Cyber Security) at Sanjivani University, Kopargaon for the academic year 2026–2027. All scripts and documentation are intended solely for educational and research purposes under authorized supervision.
