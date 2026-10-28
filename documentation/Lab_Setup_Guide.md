# Laboratory Setup & Virtualization Guide

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Hardware & Virtualization Architecture

Building an isolated sandbox for malware analysis requires establishing strict operational containment at the hypervisor boundary. The sandbox executes inside a Type-2 desktop hypervisor (Oracle VM VirtualBox or VMware Workstation Pro) on a dedicated host machine.

### 1.1 Virtual Machine Specifications

| Hardware Component | Allocated Resource | Security & Performance Rationale |
| :--- | :--- | :--- |
| **Virtual CPUs (vCPUs)** | 2 Cores | Sufficient for multi-threaded OS monitoring while leaving host responsive |
| **Random Access Memory (RAM)** | 4,096 MB (4.0 GB) | Provides ample headroom for Linux kernel, memory buffers, and capture utilities |
| **Virtual Storage** | 30.0 GB (VDI / VMDK) | Dynamically allocated disk storage for OS installation and snapshot trees |
| **Guest Operating System** | Ubuntu 22.04 LTS (64-bit) | Standardized, modern Linux distribution with complete auditing toolchains |
| **Display Memory** | 128 MB (3D Accel Disabled) | Disabling 3D acceleration mitigates potential hypervisor graphics driver exploits |
| **Shared Folders** | **DISABLED** | Mandatory safeguard: Prevents host file system tampering or inadvertent traversal |
| **Shared Clipboard** | **DISABLED** | Prevents host-to-guest and guest-to-host data leakage |
| **Drag & Drop** | **DISABLED** | Eliminates accidental transfer of untrusted binaries or host files |

---

## 2. Hypervisor Network Adapter Modes: Comparative Analysis

Choosing the correct virtual network architecture is the single most critical security decision in sandbox deployment. Below is a comparative analysis of the five primary network modes:

| Network Mode | Host Communication | LAN Access | Internet Access | Suitability for Malware Sandbox |
| :--- | :--- | :--- | :--- | :--- |
| **Bridged Adapter** | Yes | Yes (Direct) | Yes (Direct) | **PROHIBITED**: Severe risk. Worms and C2 beacons can infect physical LAN. |
| **NAT (Network Address Translation)** | Host-managed | Outbound only | Yes (Outbound) | **PROHIBITED**: Outbound C2 traffic can reach external criminal infrastructure. |
| **Host-Only Adapter** | Yes (Isolated Subnet)| No | **NO** | **APPROVED**: Enables controlled host-guest communications if required. |
| **Internal Network** | No (VM-to-VM only) | No | **NO** | **APPROVED**: Perfect for multi-VM attack/defense simulations without host link. |
| **Not Attached / Disconnected** | **NO** | **NO** | **NO** | **OPTIMAL / MANDATORY**: Total isolation. Zero external network egress. |

> **Mandatory Policy for NPC Capstone Experiment**:  
> The virtual machine network adapter MUST be configured to **"Not Attached"** (VirtualBox) or **"Disconnected" / "Host-Only with Host Virtual Adapter Disabled"** (VMware) to ensure complete Internet isolation.

---

## 3. Step-by-Step VM Configuration Instructions

### 3.1 Oracle VM VirtualBox Configuration
1. **VM Creation**:
   - Open Oracle VM VirtualBox.
   - Click **New**. Set Name: `NPC_Malware_Sandbox`, Type: `Linux`, Version: `Ubuntu (64-bit)`.
   - Allocate **4096 MB RAM** and **2 vCPUs**.
   - Create a Virtual Hard Disk of **30.0 GB** (VDI, Dynamically allocated).
2. **Network Isolation**:
   - Navigate to **Settings -> Network -> Adapter 1**.
   - Uncheck **Enable Network Adapter** OR set **Attached to: Not Attached**.
3. **Hardening**:
   - Navigate to **General -> Advanced**: Set **Shared Clipboard** to `Disabled`, **Drag'n'Drop** to `Disabled`.
   - Navigate to **Shared Folders**: Ensure no host directories are shared.
4. **OS Installation**:
   - Attach Ubuntu Desktop/Server ISO, complete base installation.
   - Install required tools: `sudo apt update && sudo apt install -y python3 net-tools tcpdump lsof`.
   - Power off VM cleanly before creating the baseline snapshot.

### 3.2 VMware Workstation Configuration
1. **VM Creation**:
   - Open VMware Workstation. Click **Create a New Virtual Machine (Custom/Advanced)**.
   - Choose Linux -> Ubuntu 64-bit. Assign 2 processor cores and 4096 MB RAM.
   - Create a 30 GB virtual disk split into multiple files or single file (VMDK).
2. **Network Isolation**:
   - In Virtual Machine Settings -> **Network Adapter**, choose **Custom: Specific virtual network** -> select a private VMnet with no host or DHCP connection, OR uncheck **Connected** and **Connect at power on**.
3. **Hardening**:
   - In **Options -> Guest Isolation**, uncheck **Enable drag and drop** and **Enable copy and paste**.
   - In **Options -> Shared Folders**, select **Disabled**.
