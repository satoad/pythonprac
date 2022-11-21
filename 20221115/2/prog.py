class Num:

    def __get__(self, obj, new_obj):
        return getattr(obj, 'value', 0)

    def __set__(self, obj, new_obj):
        if 'real' in type(new_obj).__dict__:
            obj.value = new_obj
        elif '__len__' in type(new_obj).__dict__:
            obj.value = len(new_obj)

import sys
exec(sys.stdin.read())