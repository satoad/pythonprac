class Alpha:
    __slots__ = list('abcdefghijklmnopqrstuvwxyz')

    def __init__(self, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __str__(self):
        res = ''
        for i in self.__slots__:
            try:
                res += f"{i}: {getattr(self, i)}, "
            except AttributeError:
                pass

        return res[:-2]

class AlphaQ:

    def __init__(self, **kwargs):
        for i in kwargs:
            if i in 'abcdefghijklmnopqrstuvwxyz' and len(i) == 1:
                self.__dict__[i] = kwargs[i]
            else:
                raise AttributeError

    def __getattr__(self, item):
        if item in 'abcdefghijklmnopqrstuvwxyz' and len(item) == 1:
            return self.__dict__[item]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key in 'abcdefghijklmnopqrstuvwxyz' and len(key) == 1:
            self.__dict__[key] = value
        else:
            raise AttributeError

    def __str__(self):
        res = ''

        for i in sorted(self.__dict__):
            try:
                res += f"{i}: {getattr(self, i)}, "
            except AttributeError:
                pass

        return res[:-2]

import sys
exec(sys.stdin.read())