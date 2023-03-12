from cowsay import cowsay, list_cows, read_dot_cow
import shlex
from io import StringIO
import cmd

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


class Dungeon:
    def __init__(self, hero):
        self.dungeon = [[None for i in range(10)] for j in range(10)]
        self.hero = hero
        pass

    def add_mob(self, mob):
        if self.dungeon[mob.pos[0]][mob.pos[1]] is None:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            print(f'Added monster <{mob.name}> to (<{mob.pos[0]}>, <{mob.pos[1]}>) saying <{mob.phrase}>')
        else:
            self.dungeon[mob.pos[0]][mob.pos[1]] = mob
            print(f'Added monster {mob.name} to (<{mob.pos[0]}>, <{mob.pos[1]}>) saying <{mob.phrase}>')
            print('Replaced the old monster')

    def encounter(self, x, y):
        if self.dungeon[x][y].name == "jgsbat":
            print(cowsay(self.dungeon[x][y].phrase, cowfile=bat))
        else:
            print(cowsay(self.dungeon[x][y].phrase, cow=self.dungeon[x][y].name))

    def change_hero_pos(self, pos):
        self.hero.pos[0] = (self.hero.pos[0] + pos[0]) % 10
        self.hero.pos[1] = (self.hero.pos[1] + pos[1]) % 10
        print(f'Moved to (<{self.hero.pos[0]}>, <{self.hero.pos[1]}>)')
        if self.dungeon[self.hero.pos[0]][self.hero.pos[1]] is not None:
            self.encounter(self.hero.pos[0], self.hero.pos[1])

    def attack(self, pos):
        if isinstance(self.dungeon[pos[0]][pos[1]], Monster):
            mob = self.dungeon[pos[0]][pos[1]]
            dmg = self.hero.damage
            if mob.hp < dmg:
                dmg = mob.hp

            mob.hp -= dmg

            print(f"Attacked <{mob.name}>,  damage <{dmg}> hp")

            if mob.hp == 0:
                print(f"{mob.name} died")
                self.dungeon[pos[0]][pos[1]] = None
            else:
                self.dungeon[pos[0]][pos[1]].hp = mob.hp
                print(f"{mob.name} now has {mob.hp}")

        else:
            print("No monster here")


class Hero:
    def __init__(self, pos=None):
        if pos is None:
            pos = [0, 0]

        self.pos = pos
        self.damage = 10


class Monster:
    def __init__(self, name, pos, phrase, hp, dungeon):
        self.name = name
        self.pos = pos
        self.phrase = phrase
        self.hp = hp
        dungeon.add_mob(self)


class Game(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = ''
    player = Hero()
    dungeon = Dungeon(player)

    def do_up(self, args):
        self.dungeon.change_hero_pos((0, -1))

    def do_down(self, args):
        self.dungeon.change_hero_pos((0, 1))

    def do_left(self, args):
        self.dungeon.change_hero_pos((-1, 0))

    def do_right(self, args):
        self.dungeon.change_hero_pos((1, 0))

    def do_addmon(self, inp):
        inp = shlex.split(inp)
        if len(inp) == 8:
            if inp[0] in list_cows() or inp[0] == "jgsbat":
                Monster(inp[0], [int(inp[inp.index("coords") + 1]), int(inp[inp.index("coords") + 2])],
                        inp[inp.index("hello") + 1], int(inp[inp.index("hp") + 1]), self.dungeon)
            else:
                print("Cannot add unknown monster")
        else:
            print("Invalid arguments")

    def do_attack(self, args):
        self.dungeon.attack(self.player.pos)

    def default(self, line: str) -> None:
        print("Invalid command")


def game():
    Game().cmdloop()


if __name__ == "__main__":
    game()
