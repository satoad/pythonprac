def objcount(cls):
    cls.counter = 0

    class newcls(cls):

        def __init__(self, *args, **kwargs):
            cls.counter += 1
            cls.__iinit__(self, *args, **kwargs)

        cls.__iinit__, cls.__init__ = cls.__init__, __init__

        def __del__(self, *args, **kwargs):
            cls.counter -= 1
            cls.__dell__(self, *args, **kwargs)

        if '__del__' in cls.__dict__.keys():
            cls.__dell__ = cls.__del__
        else:
            cls.__dell__ = lambda x : None


    return newcls

import sys
exec(sys.stdin.read())