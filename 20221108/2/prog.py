class BadTriangle(Exception): pass
class InvalidInput(BadTriangle): pass


def triangle_square(a):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(a)
    except Exception:
        raise InvalidInput

    if x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2) == 0.0:
        raise BadTriangle
    else:
        s = 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        if s == 0.0:
            raise BadTriangle
        else:
            return s
while True:
    a = input()

    try:
        sq = triangle_square(a)
    except InvalidInput:
        print('Invalid input')
    except BadTriangle:
        print('Not a triangle')
    else:
        print(f'{sq:.2f}')
        break