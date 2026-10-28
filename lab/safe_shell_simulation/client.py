#!/usr/bin/env python3
"""
================================================================================
NPC Capstone Project: Malware Analysis Sandbox Using VirtualBox or VMware
Safe Bind-Shell Simulation Client (Educational Laboratory Implementation)
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
- Connects exclusively to the local loopback interface (127.0.0.1:54321).
- Intended strictly for local sandbox observation and process monitoring.
- Sends testing commands (STATUS, HELP, EXIT) to demonstrate socket behavior.
================================================================================
"""

import socket
import sys

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 54321
BUFFER_SIZE = 2048


def main():
    print("=" * 70)
    print("NPC Capstone: Safe Bind-Shell Simulation Client")
    print("Student : Harshal Bhagwan Harde | PRN: 2125UCSM1001")
    print(f"Target  : {TARGET_HOST}:{TARGET_PORT} (Loopback Only)")
    print("=" * 70)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            client_sock.settimeout(10.0)
            print(f"[+] Connecting to safe simulation server at {TARGET_HOST}:{TARGET_PORT}...")
            client_sock.connect((TARGET_HOST, TARGET_PORT))
            print("[+] Connection established successfully!\n")

            # Receive initial banner
            initial_banner = client_sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
            print(initial_banner, end="")

            while True:
                prompt_data = client_sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
                print(prompt_data, end="", flush=True)

                try:
                    user_input = input()
                except (EOFError, KeyboardInterrupt):
                    print("\n[*] Exiting client...")
                    try:
                        client_sock.sendall(b"EXIT\n")
                    except Exception:
                        pass
                    break

                if not user_input.strip():
                    continue

                client_sock.sendall((user_input.strip() + "\n").encode("utf-8"))

                resp_data = client_sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
                print(resp_data)

                if user_input.strip().upper() == "EXIT":
                    print("[+] Session closed. Disconnecting.")
                    break

    except ConnectionRefusedError:
        print(f"[-] Connection failed: No server listening on {TARGET_HOST}:{TARGET_PORT}.")
        print("[-] Ensure server.py is running inside the isolated test environment.")
        sys.exit(1)
    except socket.timeout:
        print("[-] Socket operation timed out.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
