def form(a, b):
    return a[0] * a[1] - b[0] * b[1]

class Triangle:

    def __init__(self, *other):
        self.p1 = other[0]
        self.p2 = other[1]
        self.p3 = other[2]

    def __abs__(self):
        if self.p1[0] * (self.p2[1] - self.p3[1]) + self.p2[0] * (self.p3[1] - self.p1[1]) + self.p3[0] * (self.p1[1] - self.p2[1]) == 0.0:
            return 0.0
        else:
            return 0.5 * abs((self.p2[0] - self.p1[0]) * (self.p3[1] - self.p1[1]) - (self.p3[0] - self.p1[0]) * (self.p2[1] - self.p1[1]))

    def __bool__(self):
        return self.__abs__() != 0.0

    def __lt__(self, other):
        return self.__abs__() < other.__abs__()

    def __eq__(self, other):
        return self.__abs__() == other.__abs__()

    def inside(self, other):
        cr1 = form((self.p1[0] - other[0], self.p2[1] - self.p1[1]), (self.p2[0] - self.p1[0], self.p1[1] - other[1]))
        cr2 = form((self.p2[0] - other[0], self.p3[1] - self.p2[1]), (self.p3[0] - self.p2[0], self.p2[1] - other[1]))
        cr3 = form((self.p3[0] - other[0], self.p1[1] - self.p3[1]), (self.p1[0] - self.p3[0], self.p3[1] - other[1]))

        return (cr1 > 0 and cr2 > 0 and cr3 > 0) or (cr1 < 0 and cr2 < 0 and cr3 < 0)

    def __contains__(self, item):
        if not item.__bool__() or (item.p1 == self.p1 and item.p2 == self.p2 and item.p3 == self.p3):
            return True

        return self.inside(item.p1) and self.inside(item.p2) and self.inside(item.p3)

    def line_intersect(self, p1, p2, p3, p4):
        det = form((p4[1] - p3[1], p2[0] - p1[0]), (p4[0] - p3[0], p2[1] - p1[1]))
        if det == 0:
            return None

        A = form((p4[0] - p3[0], p1[1] - p3[1]), (p4[1] - p3[1], p1[0] - p3[0])) / det
        B = form((p2[0] - p1[0], p1[1] - p3[1]), (p2[1] - p1[1], p1[0] - p3[0])) / det

        if not (0 <= A <= 1 and 0 <= B <= 1):
            return None
        
        x = p1[0] + A * (p2[0] - p1[0])
        y = p1[1] + A * (p2[1] - p1[1])

        return (x, y)

    def __and__(self, other):
        if not self.__bool__():
            return False

        #дальше кринж, не надо туда смотреть


        p = self.line_intersect(self.p1, self.p2, other.p1, other.p2)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p1, self.p2, other.p1, other.p3)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p1, self.p2, other.p2, other.p3)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p2, self.p3, other.p1, other.p2)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p2, self.p3, other.p1, other.p3)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p2, self.p3, other.p2, other.p3)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p1, self.p3, other.p1, other.p2)
        if p is not None and other.inside(p):
            return True

        p = self.line_intersect(self.p1, self.p3, other.p1, other.p3)
        if p is not None and other.inside(p):

            return True

        p = self.line_intersect(self.p1, self.p3, other.p2, other.p3)
        if p is not None and other.inside(p):
            return True

        return False
