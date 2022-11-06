from math import log
from math import ceil

class Grange:

    def __init__(self, *other):
        self.b0 = other[0]
        self.q = other[1]
        self.bn = other[2]

    def __repr__(self):
        return f'grange({self.b0}, {self.q}, {self.bn})'

    def __str__(self):
        return f'grange({self.b0}, {self.q}, {self.bn})'

    def __iter__(self):
        return iter(list(self.b0 * self.q ** i for i in range(len(self))))

    def __len__(self):
        return ceil(log(self.bn / self.b0, self.q))

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step 
            if step == None:
                step = self.q
            else:
                step = self.q ** step

            return Grange(start, step, stop)

        elif isinstance(item, int):
            return self.b0 * self.q ** item



import sys
exec(sys.stdin.read())
