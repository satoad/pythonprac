from cowsay import cowsay, list_cows


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
        print(cowsay(self.dungeon[x][y].phrase, cow=self.dungeon[x][y].name))

    def change_hero_pos(self, pos):
        self.hero.pos[0] = (self.hero.pos[0] + pos[0]) % 10
        self.hero.pos[1] = (self.hero.pos[1] + pos[1]) % 10
        print(f'Moved to (<{self.hero.pos[0]}>, <{self.hero.pos[1]}>)')
        if self.dungeon[self.hero.pos[0]][self.hero.pos[1]] is not None:
            self.encounter(self.hero.pos[0], self.hero.pos[1])


class Hero:
    def __init__(self, pos=[0, 0]):
        self.pos = pos


class Monster:
    def __init__(self, name, pos, phrase, dungeon):
        self.name = name
        self.pos = pos
        self.phrase = phrase
        dungeon.add_mob(self)


def game():
    player = Hero()
    dungeon = Dungeon(player)

    while inp := input():
        inp = inp.split()

        match inp[0]:
            case 'up':
                dungeon.change_hero_pos((0, -1))
            case 'down':
                dungeon.change_hero_pos((0, 1))
            case 'left':
                dungeon.change_hero_pos((-1, 0))
            case 'right':
                dungeon.change_hero_pos((1, 0))
            case 'addmon':
                if len(inp) == 5:
                    if inp[1] in list_cows():
                        Monster(inp[1], [int(inp[2]), int(inp[3])], inp[4], dungeon)
                    else:
                        print('Cannot add unknown monster')
                else:
                    print('Invalid arguments')
            case _:
                print('Invalid command')

            
game()
