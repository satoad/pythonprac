import asyncio
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


users = {}


class Player:
    players = {}

    def __init__(self, name, address):
        self.name = name
        self.hero = Hero(name)
        self.address = address
        Player.players.update({address : self})


class Hero:
    def __init__(self, name, pos=None):
        if pos is None:
            pos = [0, 0]
        self.pos = pos
        self.name = name
        self.weapons = {"sword": 10, "spear": 15, "axe": 20}


class Monster:
    def __init__(self, name, pos, phrase, hp):
        self.name = name
        self.pos = pos
        self.phrase = phrase
        self.hp = hp


class Dungeon:
    def __init__(self):
        self.dungeon = [[None for i in range(10)] for j in range(10)]
        self.heroes = {}

    def add_hero(self, name, hero):
        self.heroes.update({name:hero})
        print(self.heroes)

    def del_hero(self, name):
        del self.heroes[name]

    def add_mob(self, name, mob):
        if self.dungeon[mob.pos[0]][mob.pos[1]] is None:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            return f'Player {name} added monster {mob.name} to ({mob.pos[0]}, {mob.pos[1]}) saying {mob.phrase}, ' \
                   f'with {mob.hp} health points.'
        else:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            return f'Player {name} added monster {mob.name} to ({mob.pos[0]}, {mob.pos[1]}) saying {mob.phrase}, ' \
                   f'with {mob.hp} health points.\n Replaced the old monster'

    def encounter(self, x, y):
        if self.dungeon[x][y].name == "jgsbat":
            return [cowsay(self.dungeon[x][y].phrase, cowfile=bat)]
        else:
            return [cowsay(self.dungeon[x][y].phrase, cow=self.dungeon[x][y].name)]

    def change_hero_pos(self, name, pos):
        print(name)
        self.heroes[name].pos[0] = (self.heroes[name].pos[0] + pos[0]) % 10
        self.heroes[name].pos[1] = (self.heroes[name].pos[1] + pos[1]) % 10

        msg = [f'Moved to ({self.heroes[name].pos[0]}, {self.heroes[name].pos[1]})']

        if self.dungeon[self.heroes[name].pos[0]][self.heroes[name].pos[1]] is not None:
            msg += self.encounter(self.heroes[name].pos[0], self.heroes[name].pos[1])
        return msg


    def attack(self, hero_name, name, weapon):
        hero = self.heroes[hero_name]
        pos = (hero.pos[0], hero.pos[1])
        dmg = hero.weapons[weapon]
        msg = ["No monster here"]

        broadcast = False
        if isinstance(self.dungeon[pos[0]][pos[1]], Monster):
            mob = self.dungeon[pos[0]][pos[1]]

            if name == mob.name:
                if mob.hp < dmg:
                    dmg = mob.hp

                mob.hp -= dmg

                msg = [f'Player {hero_name} attacked {mob.name} with {weapon}, damage {dmg} hp']

                if mob.hp == 0:
                    msg += [f'{mob.name} died']
                    self.dungeon[pos[0]][pos[1]] = None
                else:
                    self.dungeon[pos[0]][pos[1]].hp = mob.hp
                    msg += [f'{mob.name} now has {mob.hp} hp']

                broadcast = True
            else:
                msg = [f'No {name} here']

        return ("\n".join(msg), broadcast)


async def echo(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    users[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(users[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
       # print(list(Player.players.values()))
        names = [i.name for i in list(Player.players.values())]

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                message = shlex.split(q.result().decode().strip())
                match message:
                    case ["login", nickname]:
                        if me in Player.players:
                            await Player.players[me].put("You are already logged in.")

                        elif nickname in names:
                            await users[me].put("This nickname is already taken.\n"
                                                "Try 'who', to check already used nicknames")
                        else:
                            cl = Player(nickname, me)

                            dungeon.add_hero(cl.name, cl.hero)

                            for i in list(Player.players.values()):
                                await users[i.address].put(f"{nickname} joined the server!")
                            await users[me].put(f"<<< Welcome to Python-MUD 0.1 >>>")

                    case ["who"]:
                        await users[me].put("\n".join(names))

                    case ["up"]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (0, -1))))

                    case ["down"]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (0, 1))))

                    case ["left"]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (-1, 0))))

                    case ["right"]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (1, 0))))

                    case ['addmon', *args]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            if len(args) == 8:
                                if args[0] in list_cows() or args[0] == "jgsbat":
                                    ans = dungeon.add_mob(Player.players[me].name, Monster(args[0],
                                                                  [int(args[args.index("coords") + 1]),
                                                                   int(args[args.index("coords") + 2])],
                                                                  args[args.index("hello") + 1],
                                                                  int(args[args.index("hp") + 1])))

                                    for i in list(Player.players.values()):
                                        await users[i.address].put(ans)

                    case ['attack', *args]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            ans = dungeon.attack(Player.players[me].name, args[0], args[1])

                            if not ans[1]:
                                await users[me].put(ans[0])
                            else:
                                for i in list(Player.players.values()):
                                    await users[i.address].put(ans[0])
                    
                    case ['sayall', *args]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            ans = f"{Player.players[me].name}: {args[0]}"
                            for i in list(Player.players.values()):
                                await users[i.address].put(ans)
                            
                    case ["quit"]:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.")
                        else:
                            receive.cancel()
                            dungeon.del_hero(Player.players[me].name)
                            del Player.players[me], users[me]
                            writer.write("Disconnect".encode())
                            writer.close()
                
                            await writer.wait_closed()

                    case _:
                        if me not in Player.players:
                            await users[me].put("You are not logged in.\n")
                        else:
                            await users[me].put("Invalid command.")
            elif q is receive:
                receive = asyncio.create_task(users[me].get())
                writer.write(f"{q.result()}\n".encode())

                await writer.drain()

    receive.cancel()
    dungeon.del_hero(Player.players[me].name)
    del Player.players[me], users[me]
    writer.write("Disconnect".encode())
    writer.close()

    await writer.wait_closed()



async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

dungeon = Dungeon()

