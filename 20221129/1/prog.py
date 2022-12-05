import types


def dec(fun):
    def new_f(*args, **kwargs):
        print(f'{fun.__name__}: {args[1:]}, {kwargs}')
        return fun(*args, **kwargs)
    return new_f


class dump(type):
    def __new__(cls, clsname, bases, attrs, **kwds):
        new_attrs = {}
        for attr, v in attrs.items():
            if not isinstance(v, types.FunctionType):
                new_attrs[attr] = v
            else:
                new_attrs[attr] = dec(v)
        return type(clsname, bases, new_attrs)