from collections import UserString

class DivStr(UserString):
    def __init__(self, seq=""):
        super().__init__(seq)

    def __floordiv__(self, other):
        trim = len(self) // other
        res = []
        for i in range(other):
            res.append(self[i * trim:(i + 1) * trim])

        return res

    def __mod__(self, other):
        trim = len(self) % other
        return self[-trim:]


import sys
exec(sys.stdin.read())