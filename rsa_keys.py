import rsa
import primes
import gmpy


def generate_rsa_keys(length):
    p = primes.generate_prime_number(length)
    q = primes.generate_prime_number(length)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    d = int(gmpy.invert(e, phi_n))

    public_key = rsa.PublicKey(n, e)
    private_key = rsa.PrivateKey(n, e, d, p, q)

    return {'e': e, 'd': d, 'n': n}
