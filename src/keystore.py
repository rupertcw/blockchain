import base64
import os

from validator import RSAValidator


class KeyStore(object):

    def __init__(self):
        self.key = os.urandom(2)
        self._validator = RSAValidator()
        self._validator.assign_new_key()

    def sign(self, block_hash):
        return base64.b64encode(self._validator.sign(base64.b64decode(block_hash)))

    def verify(self, block_hash, signature):
        return self._validator.verify(base64.b64decode(block_hash), base64.b64decode(signature))
