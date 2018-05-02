import abc
import base64
import utils

from abc import ABCMeta


class Consensus(object):

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def calculate_proof(mining_difficulty, nonce, block_hash):
        pass


class ProofOfWork(Consensus):

    @staticmethod
    def calculate(mining_difficulty, nonce, block_hash):
        check_string = '0' * mining_difficulty

        while True:
            hashed_data = base64.b64encode(utils.to_SHA256(str(nonce), block_hash))

            if hashed_data.startswith(check_string):
                return hashed_data, nonce

            nonce += 1
