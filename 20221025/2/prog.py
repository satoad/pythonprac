from itertools import tee
from itertools import islice

def slide(seq, n):
    it1, it2 = tee(seq)
    step = 0
    while step != None:
        it1, it2 = tee(it1)
        a = islice(it2, n)
        yield from a
        step = next(it1, None)

import sys
exec(sys.stdin.read())