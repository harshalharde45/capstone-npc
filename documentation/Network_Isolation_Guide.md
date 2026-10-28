# Network Isolation & Traffic Analysis Guide

**Project**: Malware Analysis Sandbox Using VirtualBox or VMware  
**Student**: Harshal Bhagwan Harde  
**PRN**: 2125UCSM1001  
**Department**: Computer Science Engineering (Cyber Security)  
**University**: Sanjivani University, Kopargaon  
**Academic Year**: 2026–2027  

---

## 1. Network Architecture: Loopback vs External Interfaces

### 1.1 The Loopback Interface (`lo` / `127.0.0.1`)
In Unix-like operating systems and the TCP/IP suite (defined in RFC 1122), the loopback interface (`lo`) is a virtual network interface implemented purely in software by the operating system kernel:
- **Address Space**: `127.0.0.0/8` (typically `127.0.0.1`).
- **Internal Routing**: Packets addressed to `127.0.0.1` are processed entirely within the operating system's network stack. The kernel routes egress packets directly to the ingress socket buffer.
- **Physical Boundary**: Loopback packets **never touch a physical Network Interface Card (NIC)** or virtual hardware adapter. They cannot be transmitted across a local area network, hypervisor virtual switch, or the public Internet.
- **Security Boundary**: Binding our safe shell simulation exclusively to `127.0.0.1` guarantees that even if a host virtual adapter were accidentally enabled, no external machine could initiate a connection or receive data from the server.

### 1.2 External Interfaces (`ens33` / `eth0`)
Physical and virtual ethernet adapters facilitate communication between the host OS, other virtual machines, and external gateways. In our malware sandbox, all external interfaces are unconfigured, disabled, or disconnected from the hypervisor.

```
       +--------------------------------------------------------+
       |                  GUEST LINUX VM                        |
       |                                                        |
       |   [ client.py ]                     [ server.py ]      |
       |        |                                  ^            |
       |        +------> [ Kernel TCP/IP ] --------+            |
       |                 (lo: 127.0.0.1)                        |
       |                                                        |
       |   [ ens33 / eth0 ] (DISCONNECTED / NOT ATTACHED)       |
       +--------------------------------------------------------+
                                   X
                                   X (No Traffic Allowed)
                                   v
             [ Physical Host / LAN / Public Internet ]
```

---

## 2. Pre-Flight Isolation Verification Protocol

Before initiating any simulation or executing untrusted files, the analyst MUST run the following pre-flight network checks inside the guest terminal. All external connection attempts must fail decisively:

### Test 1: Route Inspection
```bash
ip route show
```
*Expected Result*: Empty output or no default gateway configured (`default via ...` must NOT appear).

### Test 2: ICMP Ping by IP Address (Bypassing DNS)
```bash
ping -c 3 8.8.8.8
```
*Expected Result*: `ping: connect: Network is unreachable` or `100% packet loss`.

### Test 3: ICMP Ping by Hostname (Testing DNS Resolution)
```bash
ping -c 3 google.com
```
*Expected Result*: `ping: google.com: Temporary failure in name resolution` or `Name or service not known`.

### Test 4: HTTP/HTTPS Egress Probe
```bash
curl -I --connect-timeout 5 https://www.google.com
```
*Expected Result*: `curl: (6) Could not resolve host: www.google.com` or `curl: (7) Failed to connect to www.google.com port 443: Network is unreachable`.

---

## 3. Loopback Traffic Capture with `tcpdump`

Because the bind-shell operates on the loopback interface, network activity is monitored locally using `tcpdump`.

### 3.1 Packet Capture Command Syntax
```bash
sudo tcpdump -i lo port 54321 -nn -vv -s0 -w evidence/packet_captures/loopback_evidence.pcap
```

**Parameter Breakdown:**
- `-i lo`: Restricts packet inspection exclusively to the loopback interface.
- `port 54321`: Captures only traffic matching the simulation daemon port.
- `-nn`: Prevents protocol and port name resolution (speeds capture and preserves numeric IP/port fidelity).
- `-vv`: Enables verbose output.
- `-s0`: Sets snaplen to unlimited (captures full packet payload).
- `-w <filename>`: Writes raw PCAP frames directly to disk for analysis in Wireshark.

### 3.2 Observed Network Transaction Sequence
When `client.py` connects and exchanges data with `server.py`, the following TCP sequence is captured:
1. **Three-Way Handshake**:
   - `Client -> Server [SYN]` (Seq=0)
   - `Server -> Client [SYN, ACK]` (Seq=0, Ack=1)
   - `Client -> Server [ACK]` (Seq=1, Ack=1)
2. **Data Transfer**:
   - `Server -> Client [PSH, ACK]` (Transmitting initial Welcome Banner)
   - `Client -> Server [PSH, ACK]` (Transmitting command string `STATUS\n`)
   - `Server -> Client [PSH, ACK]` (Transmitting status response payload)
3. **Session Teardown**:
   - `Client -> Server [PSH, ACK]` (`EXIT\n`)
   - `Client -> Server [FIN, ACK]`
   - `Server -> Client [ACK]`
   - `Server -> Client [FIN, ACK]`
   - `Client -> Server [ACK]`
