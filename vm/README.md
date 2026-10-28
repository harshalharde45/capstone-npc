# Virtual Machine Environment & Configuration

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Virtual Machine Specifications

| Parameter | Specification | Purpose / Rationale |
| :--- | :--- | :--- |
| **Hypervisor** | Oracle VM VirtualBox 7.x / VMware Workstation 17.x | Type-2 Desktop Hypervisor |
| **Guest OS** | Ubuntu Linux 22.04 LTS / 24.04 LTS (64-bit) | Stable environment with standard security tools |
| **vCPUs** | 2 Virtual CPUs | Sufficient compute for analysis without starving host |
| **RAM** | 4,096 MB (4 GB) | Ample memory for OS, logging, and monitoring utilities |
| **Storage** | 30.0 GB Dynamically Allocated VDI/VMDK | Sufficient disk space for snapshots and logs |
| **Network Adapter** | Host-Only Adapter / Disconnected (Not Attached) | Enforces total isolation from physical LAN and Internet |
| **Shared Folders** | Disabled | Prevents unintended file system cross-contamination |
| **Guest Additions** | Basic display support only (Shared Clipboard Disabled) | Prevents clipboard leakage across isolation boundaries |

---

## 2. Snapshot Architecture: `NPC_Capstone_Clean_State`

The core integrity mechanism of this sandbox is the baseline snapshot:
- **Snapshot Name**: `NPC_Capstone_Clean_State`
- **Creation Timing**: Generated immediately after clean guest OS installation, software updates, prerequisite installation (`python3`, `tcpdump`, `net-tools`), and full network disconnection.
- **Role**: Serves as the golden immutable baseline. Following any simulation, artifact generation, or behavioral monitoring, the hypervisor reverts the VM back to this exact state, discarding all non-committed disk blocks and runtime changes.

### Snapshot Creation via CLI

**VirtualBox (VBoxManage):**
```bash
# Power off the VM cleanly
VBoxManage controlvm "NPC_Malware_Sandbox" acpipowerbutton

# Create the clean baseline snapshot
VBoxManage snapshot "NPC_Malware_Sandbox" take "NPC_Capstone_Clean_State" \
    --description "Clean baseline snapshot before malware simulation experiments. Network isolated."
```

**VMware Workstation (vmrun):**
```bash
# Take clean snapshot on powered off or suspended VM
vmrun -T ws snapshot "/path/to/NPC_Malware_Sandbox.vmx" "NPC_Capstone_Clean_State"
```

---

## 3. Snapshot Restoration Protocol

Following completion of the analysis phase and log capture:
```bash
# VirtualBox restoration
VBoxManage snapshot "NPC_Malware_Sandbox" restore "NPC_Capstone_Clean_State"

# VMware Workstation restoration
vmrun -T ws revertToSnapshot "/path/to/NPC_Malware_Sandbox.vmx" "NPC_Capstone_Clean_State"
```

Refer to `documentation/Snapshot_Recovery_Guide.md` for post-restoration verification audits.
