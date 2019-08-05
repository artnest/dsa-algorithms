import rsa_keys
from elliptic_curve import EllipticCurve
from ec_dsa import ECDSA
from sha1 import SHA1
from diffie_hellman import DiffieHellman
from rsa_dsa import RSADSA

# RSA DSA
keys = rsa_keys.generate_rsa_keys(256)

rsa_dsa = RSADSA(keys['n'])

sign = rsa_dsa.sign(SHA1, 'ARTYOM', keys['d'])
print(rsa_dsa.verify(SHA1, sign, keys['e']))

curve = EllipticCurve(67)

# Diffie-Hellman
dh = DiffieHellman(curve, curve.points[3])

a_private = 7
a_public = dh.gen_public(a_private)

b_private = 13
b_public = dh.gen_public(b_private)

secret = dh.gen_secret(a_private, b_public)
print(dh.gen_secret(a_private, b_public) == dh.gen_secret(b_private, a_public))

# EC DSA
point = curve.prime_order_point()
ec_dsa = ECDSA(curve, point)

private = 4
public = ec_dsa.gen_public(private)

sign = ec_dsa.sign(SHA1, 'ARTYOM', private)
print(ec_dsa.verify(SHA1, sign, public))
