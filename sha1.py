import bitarray
import constants


def lshift(bits, n):
    temp = bits[0:n]
    bits = bits[n:len(bits)]
    bits.extend(temp)
    return bits


def get_bits_array(data):
    ba = bitarray.bitarray()
    ba.frombytes(data.encode(constants.ENCODING))
    return ba


def get_bits_from_int(number):
    num = format(number, "b")
    if len(num) % 8 != 0:
        num = "0" * (8 - len(num) % 8) + num

    num = "".join([num[i - 8: i] for i in range(len(num), 0, -8)])

    result = []
    for el in num:
        if el == '1':
            result.append(1)
        if el == '0':
            result.append(0)

    a = get_bits_array("")
    a.extend(result)
    return a


def get_int_from_bits(bits):
    i = 0
    for bit in bits:
        i = (i << 1) | bit

    return i


def parse_data_to_block(data):
    bits = get_bits_array(data)

    dest = len(bits) % constants.BLOCK_SIZE

    bits.append(1)

    if dest <= constants.SMALL_BLOCK_SIZE:
        zero = [0 for _ in range(constants.SMALL_BLOCK_SIZE - dest - 1)]
    else:
        zero = [0 for _ in range(constants.BLOCK_SIZE - dest + constants.SMALL_BLOCK_SIZE - 1)]

    bits.extend(zero)

    length = get_bits_from_int(len(data))

    result = [0 for _ in range(64 - len(length))]
    bits.extend(result)

    bits.extend(length)

    result = []
    for i in range(0, len(bits), constants.BLOCK_SIZE):
        result.append(bits[i:i + constants.BLOCK_SIZE])

    return result


def parse_data_to_w(block):
    w = []
    for i in range(0, len(block), 32):
        w.append(block[i: i + 32])
    return w


class SHA1:
    def __init__(self, message) -> None:
        self.hex = 0
        self.hash_res = self.hash(message)

    def hexdigest(self):
        return hex(self.hex)

    def hash(self, data):
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        data = parse_data_to_block(data)
        for block in data:
            w = parse_data_to_w(block)
            for i in range(16, 80):
                res = w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]

                w.append(lshift(res, 1))

            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            for i in range(0, 80):
                k = 0
                f = 0
                if 0 <= i <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                a_ = get_bits_array("")
                a_.extend(lshift(get_bits_from_int(a), 5))
                temp = ((get_int_from_bits(a_)) + f + e + k + get_int_from_bits(w[i])) % 2 ** 32
                e = d
                d = c
                c = get_int_from_bits(lshift(get_bits_from_int(b), 30))
                b = a
                a = temp

            h0 = h0 + a
            h1 = h1 + b
            h2 = h2 + c
            h3 = h3 + d
            h4 = h4 + e

        self.hex = h0 + h1 + h2 + h3 + h4

        return str(hex(h0).split('x')[-1]) + \
               str(hex(h1).split('x')[-1]) + \
               str(hex(h2).split('x')[-1]) + \
               str(hex(h3).split('x')[-1]) + \
               str(hex(h4).split('x')[-1])
