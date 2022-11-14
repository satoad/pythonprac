class Undead(Exception): pass
class Zombie(Undead): pass
class Ghoul(Undead): pass
class Skeleton(Undead): pass

def necro(a):
    exc = [Skeleton, Zombie, Ghoul]
    raise exc[a % 3]


x, y = eval(input())
for i in range(x, y):
    try:
        necro(i)
    except Skeleton:
        print('Skeleton')
    except Zombie:
        print('Zombie')
    except Ghoul:
        print('Generic Undead')