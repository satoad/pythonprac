"""MOOD server"""

import os
import time
import copy
import shlex
import locale
import random
import asyncio
import gettext
import threading
from io import StringIO
from cowsay import cowsay, list_cows, read_dot_cow

popath = os.path.join(os.path.dirname(__file__), "po")
ENG = gettext.translation("server", popath, languages=["en"], fallback=True)
RU = gettext.translation("server", popath, languages=["ru"], fallback=True)


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
    """Class representation of player."""

    players = {}
    """Dictionary of connected players."""

    def __init__(self, name, address, writer):
        """Initialization method.

           Args:
               name (str): Player's nickname
               address (str): Player's ip address
               writer (asyncio.streams.StreamWriter): Player's write stream
        """
        
        self.name = name
        self.hero = Hero(name)
        self.address = address
        self.writer = writer
        self.locale = ENG
        Player.players.update({address: self})


class Hero:
    """Class representation of player's hero."""

    def __init__(self, name, pos=None):
        """Initialization method.

            Args:
                name (str): Hero's nickname
                pos (list): Hero's position in dungeon
        """
        
        if pos is None:
            pos = [0, 0]
        self.pos = pos
        self.name = name
        self.weapons = {"sword": 10, "spear": 15, "axe": 20}


class Monster:
    """Class representation of monster."""

    def __init__(self, name, pos, phrase, hp):
        """Initialization method.

            Args:
                name (str): Monster's nickname
                pos (list): Monster's ip address
                phrase (str): Monster's hello phrase
                hp (int): Monster's health points
        """
        
        self.name = name
        self.pos = pos
        self.phrase = phrase
        self.hp = hp


async def broadcast(ans):
    """Broadcast message implementation.

        Args:
            ans (str): Message for players
    """
    
    for i in list(Player.players.values()):
        i.locale.install()
        i.writer.write(ans.encode())


loop = asyncio.get_event_loop()


class Dungeon:
    """Class representation of dungeon."""


    def __init__(self):
        """Initialization method."""

        self.dungeon = [[None for i in range(10)] for j in range(10)]
        self.heroes = {}
        self.mobs = {}

    def add_hero(self, name, hero):
        """Adding new hero to dungeon.

            Args:
                name (str): Hero's name
                hero (Hero): Hero
        """
        
        self.heroes.update({name: hero})
        #print(self.heroes)

    def del_hero(self, name):
        """Deleting hero from dungeon.

            Args:
                name (str): Hero's name
        """
        
        del self.heroes[name]

    def add_mob(self, name, mob):
        """Adding new monster to dungeon.

            Args:
                name (str): Monster's name
                mob (Monster): Monster
        """
        if self.dungeon[mob.pos[0]][mob.pos[1]] is None:
            ans = _("Player {} added monster {} to ({}, {}) saying {}, with {} health points.").format(name, mob.name, mob.pos[0], mob.pos[1], mob.phrase, mob.hp)
        else:
            ans = _("Player {} added monster {} to ({}, {}) saying {}, with {} health points.\nReplaced the old monster").format(name, mob.name, mob.pos[0], mob.pos[1], mob.phrase, mob.hp)
        print("added monster {} to ({}, {}) saying {}, with {} health points.".format(mob.name, mob.pos[0], mob.pos[1], mob.phrase, mob.hp))
        self.dungeon[mob.pos[0]][mob.pos[1]] = mob
        self.mobs.update({tuple(mob.pos): mob})
        return ans

    def encounter(self, x, y):
        """Check for an encounter with a monster.

            Args:
                x (int): abscissa coordinate
                y (int): ordinate coordinate
        """
        
        if self.dungeon[x][y].name == "jgsbat":
            return [cowsay(self.dungeon[x][y].phrase, cowfile=bat)]
        else:
            return [cowsay(self.dungeon[x][y].phrase, cow=self.dungeon[x][y].name)]

    def mob_move(self):
        """Monster straying implementation."""
    
        direction = {(0, 1): "up", (0, -1): "down", (1, 0): "right", (-1, 0): "left"}
        first = True
        while True:
            if self.mobs:
                if first:
                    time.sleep(1)
                    first = False

                flag = True
                while flag:
                    mob = random.choice([i for i in list(self.mobs.values())])
                    vect = list(random.choice([i for i in list(direction.keys())]))
                    pos = copy.copy(mob.pos)

                    mob.pos[0] = (mob.pos[0] + vect[0]) % 10
                    mob.pos[1] = (mob.pos[1] + vect[1]) % 10

                    if self.dungeon[mob.pos[0]][mob.pos[1]] is None:
                        self.dungeon[pos[0]][pos[1]] = None
                        self.dungeon[mob.pos[0]][mob.pos[1]] = mob
                            
                        ans = _("{} moved one cell {}").format(mob.name, direction[tuple(vect)])
                        loop.run_until_complete(broadcast(ans))

                        del self.mobs[tuple(pos)]
                        self.mobs.update({tuple(mob.pos): mob})

                        for i in list(self.heroes.values()):
                            #print(f"mob pos {mob.pos} and hero pos {i.pos}")
                            if mob.pos[0] == i.pos[0] and mob.pos[1] == i.pos[1]:
                                ans = dungeon.encounter(i.pos[0], i.pos[1])

                                for j in [pl for pl in Player.players.values()]:
                                    if j.hero == i:
                                        Player.players[j.address].writer.write("\n".join(ans).encode())

                        flag = False

                time.sleep(10)
            else:
                first = True

    def change_hero_pos(self, name, pos):
        """Hero moves implementation.

            Args:
                name (str): Hero's name
                pos (list): Hero's movement
        """
        
        self.heroes[name].pos[0] = (self.heroes[name].pos[0] + pos[0]) % 10
        self.heroes[name].pos[1] = (self.heroes[name].pos[1] + pos[1]) % 10
        
        msg = [_("Moved to ({}, {})").format(self.heroes[name].pos[0], self.heroes[name].pos[1])]
        #print(msg)
        if self.dungeon[self.heroes[name].pos[0]][self.heroes[name].pos[1]] is not None:
            msg += self.encounter(self.heroes[name].pos[0], self.heroes[name].pos[1])
        return msg

    def attack(self, hero_name, name, weapon):
        """Hero's attack implementation
            
            Args:
                hero_name (str): Hero's name
                name (str): Monster's name
                weapon (str): Type of hero's weapon
        """
        
        hero = self.heroes[hero_name]
        pos = (hero.pos[0], hero.pos[1])
        dmg = hero.weapons[weapon]
        msg = [_("No monster here")]

        broadcast = False
        if isinstance(self.dungeon[pos[0]][pos[1]], Monster):
            mob = self.dungeon[pos[0]][pos[1]]

            if name == mob.name:
                if mob.hp < dmg:
                    dmg = mob.hp

                mob.hp -= dmg

                msg = [_("Player {} attacked {} with {}, damage {} hp").format(hero_name, mob.name, weapon, dmg)]

                if mob.hp == 0:
                    msg += [_("{} died").format(mob.name)]
                    self.dungeon[pos[0]][pos[1]] = None
                else:
                    self.dungeon[pos[0]][pos[1]].hp = mob.hp
                    msg += [_("{} now has {} hp").format(mob.name, mob.hp)]

                broadcast = True
            else:
                msg = [_("No {} here").format(name)]

        return "\n".join(msg), broadcast


dungeon = Dungeon()
gm = threading.Thread(target=dungeon.mob_move)
gm.start()


async def echo(reader, writer):
    """Server implementation."""

    me = "{}:{}".format(*writer.get_extra_info('peername'))
    # print(me)
    #print(type(writer), writer)

    users[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(users[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        names = [i.name for i in list(Player.players.values())]

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                message = shlex.split(q.result().decode().strip())
                #print(message)
                if me not in Player.players and message[0] != "login" and message[0] != "who":
                    await users[me].put("You are not logged in.")
                else:
                    match message:
                        case ["login", nickname]:
                            if me in Player.players:
                                await Player.players[me].put("You are already logged in.")

                            elif nickname in names:
                                await users[me].put("This nickname is already taken.\n"
                                                    "Try 'who', to check already used nicknames")
                            else:
                                cl = Player(nickname, me, writer)

                                dungeon.add_hero(cl.name, cl.hero)

                                for i in list(Player.players.values()):
                                    await users[i.address].put(f"{nickname} joined the server!")
                                await users[me].put(f"<<< Welcome to Python-MUD 0.1 >>>")

                        case ["who"]:
                            await users[me].put("\n".join(names))

                        case ["up"]:
                            Player.players[me].locale.install()
                            await users[me].put(
                                "\n".join(dungeon.change_hero_pos(Player.players[me].name, (0, -1))))

                        case ["down"]:
                            Player.players[me].locale.install()
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (0, 1))))

                        case ["left"]:
                            Player.players[me].locale.install()
                            await users[me].put(
                                "\n".join(dungeon.change_hero_pos(Player.players[me].name, (-1, 0))))

                        case ["right"]:
                            Player.players[me].locale.install()
                            await users[me].put("\n".join(dungeon.change_hero_pos(Player.players[me].name, (1, 0))))

                        case ['addmon', *args]:
                            if len(args) == 8:
                                if args[0] in list_cows() or args[0] == "jgsbat":
                                    ans = dungeon.add_mob(Player.players[me].name, Monster(args[0],
                                                                                           [int(args[args.index(
                                                                                               "coords") + 1]),
                                                                                            int(args[args.index(
                                                                                                "coords") + 2])],
                                                                                           args[
                                                                                               args.index(
                                                                                                   "hello") + 1],
                                                                                           int(args[args.index(
                                                                                               "hp") + 1])))

                                    for i in list(Player.players.values()):
                                        await users[i.address].put(ans)

                        case ['attack', *args]:
                            ans = dungeon.attack(Player.players[me].name, args[0], args[1])

                            if not ans[1]:
                                await users[me].put(ans[0])
                            else:
                                loop.run_until_complete(broadcast(ans))

                        case ['sayall', *args]:
                            ans = f"{Player.players[me].name}: {args[0]}"
                            loop.run_until_complete(broadcast(ans))
                        
                        case ['locale', *args]:
                            if args[0] == 'ru_RU.UTF8':
                                Player.players[me].locale = RU
                            else:
                                Player.players[me].locale = ENG
                            
                            Player.players[me].locale.install()
                            await users[me].put(_("Set up locale: {}").format(args[0]))

                        case ["quit"]:
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

def start_server():
    asyncio.run(main())
