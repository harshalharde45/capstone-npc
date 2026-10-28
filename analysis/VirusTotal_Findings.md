# VirusTotal Threat Intelligence Investigation

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Investigation Protocol & Search Methodology

In professional security operations centers (SOC) and incident response teams, threat intelligence services such as VirusTotal aggregate results from over 70 commercial antivirus engines, dynamic analysis sandboxes, and heuristics platforms. 

To evaluate the public threat footprint of our laboratory artifacts without compromising operational confidentiality, the analyst queries VirusTotal using the computed cryptographic hashes rather than uploading raw script contents:

- **Target 1 (`server.py`) SHA-256**: `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f`
- **Target 2 (`client.py`) SHA-256**: `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10`
- **Search Query URLs**:
  - `https://www.virustotal.com/gui/file/8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f`
  - `https://www.virustotal.com/gui/file/6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10`

---

## 2. Investigation Findings & Official Finding Statement

In accordance with strict academic integrity standards:

> **Official Finding**:  
> **"No existing VirusTotal report was available for the investigated file at the time of analysis."**

### Detailed Metric Record

| Field / Parameter | `server.py` Finding | `client.py` Finding |
| :--- | :--- | :--- |
| **Queried Hash (SHA-256)** | `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f` | `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10` |
| **Query Result** | "Item not found" / "No results found" | "Item not found" / "No results found" |
| **Detection Score** | N/A (Unseen by public multi-engines) | N/A (Unseen by public multi-engines) |
| **First-Seen Submission Date** | None (File has never been submitted to public repositories) | None (File has never been submitted to public repositories) |
| **Historical Community Tags** | None | None |
| **Known Malicious Indicators** | None detected / Clean local origin | None detected / Clean local origin |

---

## 3. Technical & Operational Analysis of the Finding

### 3.1 Why No Report Exists
The absence of a VirusTotal record is completely expected and technically coherent:
1. **Custom Authorship**: The simulation files were authored exclusively for this educational capstone project by Harshal Bhagwan Harde.
2. **Fresh Hash Digest**: Because the source files include unique student metadata, comments, and specific formatting, their cryptographic hashes are completely unique and have never been indexed in public threat intelligence databases.
3. **No Prior Upload**: The script has not been previously distributed, infected, or submitted to VirusTotal’s web interface or API.

### 3.2 Operational Security (OPSEC) Considerations
In real-world cybersecurity practice:
- **Hash-First Querying**: Analysts must always search by SHA-256 hash first.
- **Data Leakage Risks**: Uploading an unknown file directly to VirusTotal makes it accessible to premium enterprise subscribers worldwide. If an organization uploads an internal proprietary script, penetration test tool, or document with sensitive tokens, confidentiality is compromised.
- **Sandbox Evaluation Principle**: If a hash query returns "Item not found", the analyst relies on local sandbox behavioral monitoring (`ss`, `ps`, `tcpdump`, memory analysis) to assess capabilities rather than relying on automated cloud telemetry.
