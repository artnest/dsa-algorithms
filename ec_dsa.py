import gmpy
import random


class ECDSA:
    def __init__(self, e_curve, point):
        self.ec = e_curve
        self.g = point
        self.q = self.ec.orders[self.g]

    def gen_public(self, private_key):
        # assert 0 < private < self.q

        return self.ec.mul(self.g, private_key)

    def sign(self, hash_function, message, private_key):
        hash_message = int(hash_function(message).hexdigest(), 16)
        k = random.sample(range(1, self.q), 1)

        signature = {}
        r = 0
        s = 0
        while True:
            kG = self.ec.mul(self.g, k[0])
            r = kG.x % self.q
            if r != 0:
                k_ = gmpy.invert(k[0], self.q)
                s = (k_ * (hash_message + private_key * r)) % self.q
                break

        signature['r'] = r
        signature['s'] = s
        signature['message'] = message
        return signature

    def verify(self, hash_function, signature, public):
        hash_message = int(hash_function(signature['message']).hexdigest(), 16)
        # assert 0 < sign['r'] < self.q
        # assert 0 < sign['s'] < self.q

        w = gmpy.invert(signature['s'], self.q)

        u_1 = (hash_message * w) % self.q
        u_2 = (signature['r'] * w) % self.q

        point = self.ec.add(self.ec.mul(self.g, u_1), self.ec.mul(public, u_2))
        r_ = point.x % self.q

        return r_ == signature['r']
