# Snapshot Architecture & Recovery Guide

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. The Role of Snapshots in Malware Analysis

Virtual machine snapshots provide the foundational containment and reproducibility mechanism for malware analysis. When a snapshot is taken, the hypervisor freezes the base virtual disk image (`.vdi` or `.vmdk`) into a read-only state and creates a copy-on-write (COW) differencing disk. 

During malware analysis:
- All file creations, registry modifications, deleted files, and process executions write exclusively to the differencing disk.
- Once dynamic observation is complete, reverting to the snapshot instantaneously discards the differencing disk.
- The virtual machine returns to its pristine, uninfected state within seconds.

---

## 2. Snapshot Creation: `NPC_Capstone_Clean_State`

### 2.1 Preparation Checklist Prior to Snapshotting
1. Clean guest OS installed and fully updated.
2. Necessary analysis tools pre-installed: `python3`, `tcpdump`, `lsof`, `net-tools`, `wireshark`.
3. Virtual network adapter unattached / disconnected.
4. Temporary browser history, bash command history, and temporary `/tmp` files cleaned.
5. Virtual machine cleanly powered off (or in a quiescent clean state).

### 2.2 CLI Execution Commands

**VirtualBox (VBoxManage):**
```bash
# Take clean baseline snapshot
VBoxManage snapshot "NPC_Malware_Sandbox" take "NPC_Capstone_Clean_State" \
    --description "Baseline clean snapshot. Network isolated. Ready for NPC capstone simulation."
```

**VMware Workstation (vmrun):**
```bash
vmrun -T ws snapshot "/var/lib/vmware/NPC_Malware_Sandbox/NPC_Malware_Sandbox.vmx" "NPC_Capstone_Clean_State"
```

---

## 3. Snapshot Restoration Protocol

After executing the safe shell simulation, capturing logs, and collecting network PCAP evidence, the analyst restores the virtual machine:

### 3.1 CLI Reversion Commands

**VirtualBox:**
```bash
# Power off the VM if running
VBoxManage controlvm "NPC_Malware_Sandbox" poweroff

# Restore to the clean snapshot
VBoxManage snapshot "NPC_Malware_Sandbox" restore "NPC_Capstone_Clean_State"

# Power on the VM in its restored state
VBoxManage startvm "NPC_Malware_Sandbox" --type gui
```

**VMware Workstation:**
```bash
# Stop and revert VM
vmrun -T ws revertToSnapshot "/var/lib/vmware/NPC_Malware_Sandbox/NPC_Malware_Sandbox.vmx" "NPC_Capstone_Clean_State"

# Start the clean VM
vmrun -T ws start "/var/lib/vmware/NPC_Malware_Sandbox/NPC_Malware_Sandbox.vmx"
```

---

## 4. Post-Recovery Forensic Audit Checklist

To verify that the system has returned to its clean baseline without residual artifacts, execute this 5-point verification suite inside the guest VM:

```bash
# 1. Audit Listening Sockets (Port 54321 must NOT appear)
ss -tulpn | grep 54321

# 2. Audit Active Processes (server.py or python3 shell processes must NOT exist)
ps -aux | grep "server.py" | grep -v grep

# 3. Audit Temporary Directory for Injected Files
ls -la /tmp/ /var/tmp/

# 4. Audit File Timestamps and Inodes
stat /etc/passwd /etc/hosts

# 5. Audit Critical System Binary Hashes
sha256sum /bin/bash /usr/bin/python3
```

*Criteria for Successful Restoration*:
- Port 54321 returns no listeners.
- No `server.py` or rogue processes appear in `ps`.
- No experimental log files or temporary scripts exist outside the snapshot baseline.
- Core system binary hashes match the baseline catalog exactly.

---

## 5. Forensic Limitations of Hypervisor Snapshots

While snapshots are essential, security engineers must understand their technical limitations:

1. **Shared Folders Non-Reversion**:  
   If shared folders are enabled between host and guest, any file written, modified, or deleted inside the shared folder resides directly on the host file system. **Reverting a VM snapshot does NOT revert changes made to host shared folders.** For this reason, shared folders must always be disabled in malware sandboxes.

2. **Hypervisor Escape Vulnerabilities**:  
   Advanced nation-state malware or sandbox-aware exploits (e.g., VENOM, VM-escape bugs in SVGA drivers or virtualization extensions) could compromise the hypervisor process on the host. A VM snapshot provides zero protection against a host-level escape.

3. **Live Snapshots vs Powered-Off Snapshots**:  
   A live snapshot saves volatile RAM state (`.vmsn` / `.sav`), allowing immediate resumption. However, if the live snapshot was taken while hidden rootkits or malware artifacts were already dormant in memory buffers, the "clean" state is tainted. Powered-off clean snapshots are forensically preferred for immutable baselines.
