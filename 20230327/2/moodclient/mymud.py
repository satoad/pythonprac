import sys
import cmd
import socket
import shlex
import readline
import threading
from cowsay import list_cows


def recv(cmdline):
    while True:
        ans = s.recv(2048).decode()
        if ans:
            if ans.strip() == "Disconnect":
                break

            print(f"\n{ans}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


class Game(cmd.Cmd):
    def __init__(self, prompt=''):
        super().__init__()
        self.prompt = prompt
        self.use_rawinput = False

    def do_login(self, args):
        s.send(("login " + args + '\n').encode())

    def do_who(self, args):
        s.send(("who\n").encode())

    def do_up(self, args):
        s.send(("up\n").encode())

    def do_down(self, args):
        s.send(("down\n").encode())

    def do_left(self, args):
        s.send(("left\n").encode())

    def do_right(self, args):
        s.send(("right\n").encode())
        
    def do_sayall(self, args):
        s.send(("sayall " + args + '\n').encode())

    def do_addmon(self, args):
        inp = shlex.split(args)
        if len(inp) == 8:
            if inp[0] in list_cows() or inp[0] == "jgsbat":
                msg = "addmon " + args
                s.send((msg + '\n').encode())
            else:
                print("Cannot add unknown monster")
        else:
            print("Invalid arguments")

    def do_attack(self, args):
        weapons = {"sword": 10, "spear": 15, "axe": 20}

        inp = shlex.split(args)
        if len(inp) == 3:
            if inp[1] == "with":
                if inp[2] in weapons:
                    msg = "attack " + inp[0] + " " + inp[2]
                    s.send((msg + '\n').encode())
                else:
                    print("Unknown weapon")
            else:
                print("Invalid arguments")
        elif len(inp) == 1:
            msg = ' '.join(["attack", inp[0], "sword"])
            s.send((msg + '\n').encode())
        else:
            print("Invalid arguments")

    def complete_attack(self, prefix, line, start, end):
        complete_name = list_cows() + ["jgsbat"]
        complete_weapon = ["sword", "spear", "axe"]

        line = shlex.split(line)
        if prefix and len(line) == 2:
            return [
                comp for comp in complete_name
                if comp.startswith(prefix)
            ]
        elif len(line) == 1 and not prefix:
            return complete_name
        elif len(line) == 2:
            if not prefix:
                return ["with"]
            else:
                return [
                    comp for comp in ["with"]
                    if comp.startswith(prefix)
                ]
        elif len(line) == 3:
            if not prefix:
                return complete_weapon
            else:
                return [
                    comp for comp in complete_weapon
                    if comp.startswith(prefix)
                ]

    def do_quit(self, args):
        s.send("quit\n".encode())
        sys.exit()

    def default(self, line: str) -> None:
        print("Invalid command")


def game():
    print(s.recv(1024).decode().strip())

    cmdline = Game()
    gm = threading.Thread(target=recv, args=(cmdline,))
    gm.start()
    Game().cmdloop()

def main():
    global s
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 1337))
        s.send(f"login {sys.argv[1]}\n".encode())

