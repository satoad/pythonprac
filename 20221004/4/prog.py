from math import *

def Calc(s, t, u):
    def func(x):
        x = eval(s)
        y = eval(t)
        return eval(u)
    return func

F = Calc(*eval(input()))
print(F(eval(input())))