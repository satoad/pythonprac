from collections import UserString

class DivStr(UserString):
    def __init__(self, seq=""):
        super().__init__(seq)

    def __floordiv__(self, other):
        trim = len(self) // other
        res = []
        for i in range(trim):
            res.append(self[i * other:(i + 1) * other])

        return res

    def __mod__(self, other):
        trim = len(self) % other
        return self[-trim:]