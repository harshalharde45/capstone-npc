# Cryptographic Hash Results & Verification

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Summary of Cryptographic Findings

In digital forensics and malware analysis, cryptographic hashing generates unique, fixed-length alphanumeric strings that mathematically identify files. Comparing cryptographic hashes guarantees data integrity, facilitates detection cross-referencing across threat intelligence feeds, and ensures that evidence files have not been modified.

The following cryptographic hashes were computed directly on the laboratory files using standard cryptographic digests (MD5, SHA-1, and SHA-256):

```
Artifact 1: lab/safe_shell_simulation/server.py
--------------------------------------------------------------------------------
File Size : 6,119 bytes
MD5       : 21199ab7631c9e5980f5ea130066dfc9
SHA-1     : f16d4c237857271467c36b26ebaff73ba56bec78
SHA-256   : 8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f

Artifact 2: lab/safe_shell_simulation/client.py
--------------------------------------------------------------------------------
File Size : 3,255 bytes
MD5       : 8b12014191ba695f2d1668313b4d72df
SHA-1     : a6af278ad686b2e92d468413a918b069e39dd01d
SHA-256   : 6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10
```

---

## 2. Cryptographic Hash Comparison Table

| Artifact Name | Size | MD5 (128-bit) | SHA-1 (160-bit) | SHA-256 (256-bit) |
| :--- | :--- | :--- | :--- | :--- |
| `server.py` | 6,119 B | `21199ab7631c9e5980f5ea130066dfc9` | `f16d4c237857271467c36b26ebaff73ba56bec78` | `8864d0fbd383b5349af04e820133b8e4578581fa26c8e19e518d8a2bb6e3fb5f` |
| `client.py` | 3,255 B | `8b12014191ba695f2d1668313b4d72df` | `a6af278ad686b2e92d468413a918b069e39dd01d` | `6a774332f04f1c69e4ff8e16d2077557c55efb0ba8dcbd499524cb1cf7866d10` |

---

## 3. Hash Verification Methodology

### 3.1 Verification via Linux Command-Line Utilities

Execute the standard GNU coreutils hashing commands inside the terminal:

```bash
# Calculate MD5 hashes
md5sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py

# Calculate SHA-1 hashes
sha1sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py

# Calculate SHA-256 hashes
sha256sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
```

### 3.2 Verification via Python Script

```python
import hashlib

def calculate_hashes(filepath):
    with open(filepath, "rb") as f:
        content = f.read()
    print(f"File: {filepath} ({len(content)} bytes)")
    print(f"MD5   : {hashlib.md5(content).hexdigest()}")
    print(f"SHA1  : {hashlib.sha1(content).hexdigest()}")
    print(f"SHA256: {hashlib.sha256(content).hexdigest()}\n")

calculate_hashes("lab/safe_shell_simulation/server.py")
calculate_hashes("lab/safe_shell_simulation/client.py")
```

Both methods yield identical hash digests, confirming the integrity of the files across platforms.
