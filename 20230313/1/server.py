import asyncio
from cowsay import list_cows
import shlex


class Dungeon:
    def __init__(self, hero):
        self.dungeon = [[None for i in range(10)] for j in range(10)]
        self.hero = hero

    def add_mob(self, mob):
        if self.dungeon[mob.pos[0]][mob.pos[1]] is None:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            return f'Added monster {mob.name} to ({mob.pos[0]}, {mob.pos[1]}) saying {mob.phrase}'
        else:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            return f'Added monster {mob.name} to ({mob.pos[0]}, {mob.pos[1]}) saying {mob.phrase}\n Replaced the old monster'

    def encounter(self, x, y):
        if self.dungeon[x][y].name == "jgsbat":
            return [self.dungeon[x][y].phrase, "jgsbat"]
        else:
            return [self.dungeon[x][y].phrase, self.dungeon[x][y].name]

    def change_hero_pos(self, pos):
        self.hero.pos[0] = (self.hero.pos[0] + pos[0]) % 10
        self.hero.pos[1] = (self.hero.pos[1] + pos[1]) % 10
        msg = [f'Moved to ({self.hero.pos[0]}, {self.hero.pos[1]})']
        if self.dungeon[self.hero.pos[0]][self.hero.pos[1]] is not None:
            msg += self.encounter(self.hero.pos[0], self.hero.pos[1])
        return msg

    def attack(self, pos, name, dmg):
        msg = ["No monster here"]
        if isinstance(self.dungeon[pos[0]][pos[1]], Monster):
            mob = self.dungeon[pos[0]][pos[1]]

            if name == mob.name:
                if mob.hp < dmg:
                    dmg = mob.hp

                mob.hp -= dmg

                msg = [f'Attacked {mob.name}, damage {dmg} hp\n']

                if mob.hp == 0:
                    msg += [f'{mob.name} died']
                    self.dungeon[pos[0]][pos[1]] = None
                else:
                    self.dungeon[pos[0]][pos[1]].hp = mob.hp
                    msg += [f'{mob.name} now has {mob.hp} hp']
                return shlex.join(msg)
            else:
                msg = [f'No {name} here']

        return shlex.join(msg)


class Hero:
    def __init__(self, pos=None):
        if pos is None:
            pos = [0, 0]
        self.pos = pos
        self.weapons = {"sword": 10, "spear": 15, "axe": 20}


class Monster:
    def __init__(self, name, pos, phrase, hp):
        self.name = name
        self.pos = pos
        self.phrase = phrase
        self.hp = hp


async def echo(reader, writer):
    host, port = writer.get_extra_info('peername')
    player = Hero()
    dungeon = Dungeon(player)
    while not reader.at_eof():
        data = (await reader.readline())
        msg = shlex.split(data.decode().strip())
        ans = ''
        match msg:
            case ["up"]:
                ans = "\n".join(dungeon.change_hero_pos((0, -1)))
            case ["down"]:
                ans = "\n".join(dungeon.change_hero_pos((0, 1)))
            case ["left"]:
                ans = "\n".join(dungeon.change_hero_pos((-1, 0)))
            case ["right"]:
                ans = "\n".join(dungeon.change_hero_pos((1, 0)))

            case ['addmon', *args]:
                if len(args) == 8:
                    if args[0] in list_cows() or args[0] == "jgsbat":
                        ans = dungeon.add_mob(Monster(args[0],
                                                [int(args[args.index("coords") + 1]), int(args[args.index("coords") + 2])],
                                                args[args.index("hello") + 1], int(args[args.index("hp") + 1])))

            case ['attack', *args]:
                ans = dungeon.attack(player.pos, args[0], int(args[1]))

            case ['Connect']:
                ans = "<<< Welcome to Python-MUD 0.1 >>>"

            case _:
                ans = "Error"

        writer.write(ans.encode())
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

