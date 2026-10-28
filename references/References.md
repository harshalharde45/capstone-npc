# Academic and Technical References

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Academic Textbooks & Industry Manuals

1. **Sikorski, M., & Honig, A.** (2012). *Practical Malware Analysis: The Hands-On Guide to Dissecting Malicious Software*. San Francisco: No Starch Press.  
   *Relevance*: Establishes fundamental methodologies for dynamic analysis, safe sandbox construction, loopback network redirection, and snapshot management.

2. **Ligh, M. H., Case, A., Levy, J., & Walters, A.** (2014). *The Art of Memory Forensics: Detecting Malware and Threats in Windows, Linux, and Mac Memory*. Indianapolis: John Wiley & Sons.  
   *Relevance*: In-depth analysis of volatile memory structures, process descriptors, socket tables, and state alteration during program execution.

3. **Eilam, E.** (2005). *Reversing: Secrets of Reverse Engineering*. Indianapolis: Wiley Publishing.  
   *Relevance*: Foundational principles of binary execution, disassembly, and behavioral inspection of untrusted software.

---

## 2. Standards, Frameworks & Government Guidelines

4. **National Institute of Standards and Technology (NIST)** (2008). *Guide to Integrating Forensic Techniques into Incident Response*. NIST Special Publication (SP) 800-86. Gaithersburg: U.S. Department of Commerce.  
   *Relevance*: Guidelines on digital evidence handling, disk state integrity, cryptographic hash verification, and chain of custody preservation.

5. **National Institute of Standards and Technology (NIST)** (2012). *Computer Security Incident Handling Guide*. NIST Special Publication (SP) 800-61 Rev. 2. Gaithersburg: U.S. Department of Commerce.  
   *Relevance*: Containment strategies, containment via network isolation, and eradication techniques.

6. **MITRE Corporation** (2026). *MITRE ATT&CK® Enterprise Matrix*.  
   - Technique **T1059** (Command and Scripting Interpreter)  
   - Technique **T1071** (Application Layer Protocol)  
   - Technique **T1571** (Non-Standard Port)  
   *Relevance*: Standard taxonomy for classifying command-and-control interactions and shell behaviors.

---

## 3. Internet Engineering Task Force (IETF) RFCs

7. **Braden, R.** (1989). *Requirements for Internet Hosts - Communication Layers*. RFC 1122. Internet Engineering Task Force.  
   *Relevance*: Section 3.2.1.3 defines the loopback network (`127.0.0.0/8`), establishing why packets directed to `127.0.0.1` are strictly internal to the local host and never appear on physical network interfaces.

8. **Postel, J.** (1981). *Transmission Control Protocol*. RFC 793. Internet Engineering Task Force.  
   *Relevance*: Outlines TCP state transitions (LISTEN, SYN-SENT, ESTABLISHED, FIN-WAIT, CLOSE) observed during bind-shell socket operations.

---

## 4. Virtualization & Sandbox Architecture Documentation

9. **Oracle Corporation** (2026). *Oracle VM VirtualBox® User Manual*. Chapter 5: Virtual Storage and Snapshots; Chapter 6: Virtual Networking (Host-Only, Internal, NAT, and Bridged Modes).  
   *Relevance*: Technical specification of copy-on-write snapshot differencing disks and hypervisor virtual network switches.

10. **VMware, Inc.** (2026). *VMware Workstation Pro Documentation*. Managing Virtual Machines: Taking and Reverting Snapshots; Custom Virtual Network Configurations.  
    *Relevance*: Documentation on `.vmdk` snapshot chains, delta files, and isolation mechanisms preventing virtual machine escapes.

11. **VirusTotal / Google Cloud** (2026). *VirusTotal APIv3 and File Intelligence Documentation*.  
    *Relevance*: Procedures for cryptographic hash queries (MD5/SHA-1/SHA-256), multi-engine aggregation, and responsible vulnerability disclosure without uploading sensitive operational artifacts.
