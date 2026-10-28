# Laboratory Implementations & Simulations

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## Directory Scope

The `lab/` directory contains the controlled software components developed for dynamic behavioral analysis within the virtual machine sandbox:

```
lab/
|-- README.md
|-- safe_shell_simulation/
    |-- README.md
    |-- server.py
    |-- client.py
```

## Safety Architecture

In strict compliance with academic cybersecurity ethics and the official capstone laboratory instructions:
- **Zero Remote Exposure**: All sockets bind exclusively to `127.0.0.1`.
- **Zero Code Execution**: Neither `subprocess`, `os.system`, nor shell interpreters are invoked.
- **Strict Command Filtering**: Only three deterministic testing tokens are accepted: `STATUS`, `HELP`, and `EXIT`.
- **Isolated Target**: Intended solely for execution inside the isolated guest VM (`NPC_Capstone_Clean_State`).

For execution instructions, architecture details, and cryptographic verification, refer to `lab/safe_shell_simulation/README.md`.
