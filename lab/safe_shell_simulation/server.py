#!/usr/bin/env python3
"""
================================================================================
NPC Capstone Project: Malware Analysis Sandbox Using VirtualBox or VMware
Safe Bind-Shell Simulation Server (Educational Laboratory Implementation)
================================================================================
Student Name   : Harshal Bhagwan Harde
PRN Number     : 2125UCSM1001
Course         : Bachelor of Technology (B.Tech)
Department     : Computer Science Engineering
Specialization : Cyber Security
University     : Sanjivani University, Kopargaon
Academic Year  : 2026–2027
Subject        : NPC

SAFETY AND ETHICAL LAB RESTRICTIONS:
- This script is an educational simulation strictly designed for isolated lab environments.
- Binds exclusively to the loopback interface (127.0.0.1) on port 54321.
- Rejects any remote networking, arbitrary command execution, or shell access.
- Does NOT use os.system, subprocess, pty, exec, or eval.
- Only accepts predefined harmless queries: 'STATUS', 'HELP', and 'EXIT'.
================================================================================
"""

import socket
import sys
import signal
import datetime
import time

HOST = "127.0.0.1"
PORT = 54321
BUFFER_SIZE = 1024

BANNER = (
    "======================================================================\n"
    " SAFE BIND-SHELL SIMULATION SERVER - NPC CAPSTONE LAB\n"
    " Student : Harshal Bhagwan Harde (PRN: 2125UCSM1001)\n"
    " Scope   : Isolated Loopback Only (127.0.0.1:54321)\n"
    " Status  : Arbitrary Execution Disabled by Design\n"
    "======================================================================\n"
    "Available Commands: STATUS, HELP, EXIT\n\n"
)

running = True
server_start_time = time.time()


def handle_sigint(signum, frame):
    global running
    print("\n[+] SIGINT (Ctrl+C) received. Initiating graceful shutdown...")
    running = False
    sys.exit(0)


def process_command(raw_command: str, client_address) -> str:
    cmd = raw_command.strip().upper()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    if cmd == "STATUS":
        uptime_sec = int(time.time() - server_start_time)
        return (
            f"[STATUS RESPONSE - {timestamp}]\n"
            f"[*] State             : ACTIVE_SIMULATION_LISTENING\n"
            f"[*] Bound Interface   : {HOST}:{PORT} (Loopback Only)\n"
            f"[*] Active Client     : {client_address[0]}:{client_address[1]}\n"
            f"[*] Server Uptime     : {uptime_sec} seconds\n"
            f"[*] Security Policy   : Strict Allowlist (STATUS, HELP, EXIT)\n"
            f"[*] Arbitrary Exec    : DISABLED (Zero subprocess / Zero shell)\n"
        )
    elif cmd == "HELP":
        return (
            f"[HELP GUIDE - {timestamp}]\n"
            f"  STATUS - Query sandbox simulation daemon status and uptime\n"
            f"  HELP   - Display permitted commands and safety boundaries\n"
            f"  EXIT   - Terminate current simulation connection\n"
        )
    elif cmd == "EXIT":
        return f"[EXIT NOTICE - {timestamp}] Session termination requested. Closing connection.\n"
    else:
        return (
            f"[SECURITY ALERT - {timestamp}]\n"
            f"[-] REJECTED COMMAND: '{raw_command.strip()}'\n"
            f"[-] Reason: Arbitrary command execution is disabled by design.\n"
            f"[-] Allowed commands: STATUS, HELP, EXIT.\n"
        )


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    print("=" * 70)
    print("NPC Capstone: Safe Bind-Shell Simulation Server")
    print(f"Student: Harshal Bhagwan Harde | PRN: 2125UCSM1001")
    print(f"Binding strictly to loopback {HOST}:{PORT}...")
    print("=" * 70)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(5)
            print(f"[+] Server successfully listening on {HOST}:{PORT}")
            print("[+] Waiting for connection from local simulation client...")
            print("[*] Press Ctrl+C at any time to shut down the server safely.\n")

            while running:
                try:
                    conn, addr = s.accept()
                except socket.error as e:
                    if not running:
                        break
                    print(f"[-] Accept error: {e}")
                    continue

                with conn:
                    print(f"[+] Inbound connection accepted from {addr[0]}:{addr[1]}")
                    
                    # Enforce that connections only originate from loopback
                    if addr[0] != "127.0.0.1":
                        print(f"[!] REJECTED: Non-loopback connection attempted from {addr[0]}")
                        conn.sendall(b"Connection rejected: Loopback access only.\n")
                        conn.close()
                        continue

                    conn.sendall(BANNER.encode("utf-8"))

                    while running:
                        conn.sendall(b"SAFE-SANDBOX> ")
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            print(f"[*] Client {addr[0]}:{addr[1]} disconnected.")
                            break

                        command_str = data.decode("utf-8", errors="replace")
                        print(f"[*] Received command from {addr[0]}:{addr[1]}: {command_str.strip()}")
                        
                        response = process_command(command_str, addr)
                        conn.sendall(response.encode("utf-8"))

                        if command_str.strip().upper() == "EXIT":
                            print(f"[*] Client requested EXIT. Closing connection {addr[0]}:{addr[1]}")
                            break

    except OSError as e:
        print(f"[-] Socket error: {e}")
        sys.exit(1)
    finally:
        print("[+] Server shutdown complete. Resources released.")


if __name__ == "__main__":
    main()
