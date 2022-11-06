class Omnibus:
    Namespace = {}

    def __setattr__(self, key, value):
        if key in Omnibus.Namespace:
            Omnibus.Namespace[key] += 1
        else:
            Omnibus.Namespace[key] = 1

        self.__dict__[key] = 1

    def __getattribute__(self, item):
        if item in Omnibus.Namespace:
            return Omnibus.Namespace[item]
        else:
            return object.__getattribute__(self, item)

    def __delattr__(self, item):
        if item in self.__dict__:
            self.__dict__.pop(item)

            if Omnibus.Namespace[item] > 1:
                Omnibus.Namespace[item] -= 1
            else:
                 Omnibus.Namespace.pop(item)


import sys
exec(sys.stdin.read())