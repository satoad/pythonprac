import sys
import cmd
import socket
import shlex
from io import StringIO
from cowsay import cowsay, list_cows, read_dot_cow

bat = read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))


def send_recv_serv(msg):
    s.send((msg + '\n').encode())
    ans = s.recv(1024).decode().strip().replace("'", "")

    if len(ans.split("\n")) == 3:
        ans = ans.split("\n")
        print(ans[0])
        if ans[1] == "jgsbat":
            print(cowsay(ans[1], cowfile=bat))
        else:
            print(cowsay(ans[1], cow=ans[2]))
    else:
        print(ans)
    return


class Game(cmd.Cmd):
    def __init__(self, prompt=''):
        super().__init__()
        self.prompt = prompt
        self.use_rawinput = False

    def do_up(self, args):
        send_recv_serv("up")

    def do_down(self, args):
        send_recv_serv("down")

    def do_left(self, args):
        send_recv_serv("left")

    def do_right(self, args):
        send_recv_serv("right")

    def do_addmon(self, args):
        inp = shlex.split(args)
        if len(inp) == 8:
            if inp[0] in list_cows() or inp[0] == "jgsbat":
                msg = "addmon " + args
                send_recv_serv(msg)
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
                    msg = "attack " + inp[0] + " " + str(weapons[inp[2]])
                    send_recv_serv(msg)
                else:
                    print("Unknown weapon")
            else:
                print("Invalid arguments")
        elif len(inp) == 1:
            msg = ' '.join(["attack", inp[0], str(weapons["sword"])])
            send_recv_serv(msg)
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

    def default(self, line: str) -> None:
        print("Invalid command")


def game():
    print(s.recv(1024).decode().strip())
    Game().cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        s.send("Connect\n".encode())
        game()

