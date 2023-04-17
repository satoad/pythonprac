import sys
import socket

def sqrootnet(coeffs, s):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect(("localhost", int(s)))
        msg := coeffs:
        s.sendall(msg.encode())
        print(s.recv(1024).decode())
