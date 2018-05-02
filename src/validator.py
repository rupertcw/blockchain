import abc
import Crypto

from abc import ABCMeta
from Crypto.PublicKey import RSA

RSA_BITS = 2048


def long_to_byte(n):
    ba = bytearray()
    while n:
        ba.append(n & 0xFF)
        n >>= 8
    return ba


def str_to_long(n):
    b = bytearray(n)
    return sum((1 << (bi*8)) * bb for (bi, bb) in enumerate(b))


class Validator(object):

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def assign_new_key(self):
        pass

    @abc.abstractmethod
    def sign(self, data_hash_to_sign):
        pass

    @abc.abstractmethod
    def verify(self, block_hash, signature):
        pass

class RSAValidator(Validator):

    def __init__(self):
        self._rsa = None

    def assign_new_key(self):
        rng = Crypto.Random.new().read
        self._rsa = RSA.generate(RSA_BITS, rng)

    def sign(self, data_hash_to_sign):
        return long_to_byte(self._rsa.sign(data_hash_to_sign, 1)[0])

    def verify(self, block_hash, signature):
        return self._rsa.verify(block_hash, (str_to_long(signature), None))
