from math import *

def scale_x(w, a, b, point_num):
    return (b - a) / (w - 1) * point_num + a


def scale_y(h, down, up, point):
    return int((h - 1) / (up - down) * (point - down))


weight, height, left, right, function = input().split()
weight, height, left, right = [int(el) for el in (weight, height, left, right)]
screen = [[' ' for _ in range(weight)] for _ in range(height)]

X = [scale_x(weight, left, right, i) for i in range(weight)]
Y = [eval(function) for x in X]
min_y, max_y = min(Y), max(Y)
scaled_Y = [scale_y(height, min_y, max_y, y) for y in Y]

for i, y in enumerate(scaled_Y):
    screen[y][i] = '*'
for row in screen[::-1]:
    print(*row)