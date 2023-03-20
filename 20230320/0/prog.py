import cmd
import sys
import time
import socket
import readline
import threading


globalsock = None

class simple(cmd.Cmd):

    def do_echo(self, arg):
        globalsock.sendall(arg.strip().encode())


def receiver(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        globalsock.connect((host, port))
        while msg := sys.stdin.readline():
            globalsock.sendall(msg.strip().encode())
            print(globalsock.recv(1024).decode())


cmdline = simple()
timer = threading.Thread(target=spam, args=(cmdline, 3, 10))
timer.start()
cmdline.cmdloop()
