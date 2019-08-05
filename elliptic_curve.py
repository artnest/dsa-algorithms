import collections
import gmpy
import random

import primes


def sqrt(n, q):
    assert n < q

    for i in range(1, q):
        if i * i % q == n:
            return i, q - i

    raise Exception("not found")


Coord = collections.namedtuple("Coord", ["x", "y"])


class EllipticCurve:
    def __init__(self, M):
        self.a = 0
        self.b = 0
        self.M = M

        self.points = []

        self.zero = Coord(0, 0)
        self.elliptic_group()
        self.orders = {}
        self.order()

    def elliptic_group(self):
        while (4 * self.a ** 3 + 27 * self.b ** 2) % self.M == 0:
            # 4a^3 + 27b^2 != 0
            self.a, self.b = (random.sample(range(1, self.M), 2))

        for i in range(self.M):
            # y^2 = x^3 + ax + b
            y_2 = (i ** 3 + self.a * i + self.b) % self.M

            y = 0
            while y ** 2 % self.M != y_2 and y < self.M:
                y += 1

            if y != self.M:
                self.points.append(Coord(i, y))
                if i != 0:
                    self.points.append(Coord(i, (-y) % self.M))
        #         print('new -> x={}, y={}'.format(i, y))
        #         print('new -> x={}, y={}'.format(i, self.M - y))
        # print(len(self.points))

    def is_valid(self, p):
        if p == self.zero:
            return True

        l = p.y ** 2 % self.M
        r = (p.x ** 3 + self.a * p.x + self.b) % self.M

        return l == r

    def at(self, x):
        ysq = (x ** 3 + self.a * x + self.b) % self.M
        y, my = sqrt(ysq, self.M)
        return Coord(x, y), Coord(x, my)

    def neg(self, p):
        return Coord(p.x, -p.y % self.M)

    def add(self, p1, p2):
        if p1 == self.zero:
            return p2
        if p2 == self.zero:
            return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            # p1 + -p1 == 0
            return self.zero

        if p1.x == p2.x:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1.x * p1.x + self.a) * gmpy.invert(2 * p1.y, self.M) % self.M
        else:
            l = (p2.y - p1.y) * gmpy.invert(p2.x - p1.x, self.M) % self.M

        x = (l * l - p1.x - p2.x) % self.M
        y = (l * (p1.x - x) - p1.y) % self.M

        return Coord(x, y)

    def mul(self, p, n):
        r = self.zero
        m2 = p

        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)

            n, m2 = n >> 1, self.add(m2, m2)

        return r

    def order(self):
        for g in self.points:
            i = 2
            while self.mul(g, i) != g:
                i += 1
                self.orders[g] = i - 1

    def prime_order_point(self):
        prime_order_points = [point for point in self.orders
                              if primes.is_prime(self.orders[point])]
        point = max(prime_order_points, key=lambda p: self.orders[p])
        return point
