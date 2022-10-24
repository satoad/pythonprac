def iter_sub(a, b, Type):
    res = []
    for i in a:
        if i not in b:
            res.append(i)
    return Type(res)

def sub(a, b):
    if type(a) is tuple:
        return iter_sub(a, b, tuple)
    elif type(a) is list:
        return iter_sub(a, b, list)
    else:
        return a - b

a, b = eval(input())
print(sub(a, b))