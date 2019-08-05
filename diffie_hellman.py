class DiffieHellman:
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.q = self.ec.orders[self.g]

    def gen_public(self, private_key):
        # assert 0 < private_key < self.q

        return self.ec.mul(self.g, private_key)

    def gen_secret(self, private, public):
        # assert self.ec.is_valid(public)
        # assert self.ec.mul(public, self.q) == self.ec.zero

        return self.ec.mul(public, private)
