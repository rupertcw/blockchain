import abc
import base64
import hashlib
import hmac
import utils

from abc import ABCMeta
from collections import deque

class TransactionHasher(object):

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def calculate_hash(header, transactions):
        pass


class SingleTransactionHasher(TransactionHasher):

    @staticmethod
    def calculate_hash(header, transactions):
        return base64.b64encode(utils.to_SHA256(transactions[0]._key(), header._key()))


class MerkleTreeHasher(TransactionHasher):

    @staticmethod
    def calculate_hash(header, transactions):
        txs_hashes = deque([tx.__hash__() for tx in transactions])

        while len(txs_hashes) > 1:
            txs_hashes.append(utils.to_SHA256(txs_hashes.popleft(), txs_hashes.popleft()))

        digital_signature = hmac.new(header.key_store.key, digestmod=hashlib.sha256) if header.key_store else hashlib.sha256
        digital_signature.update(txs_hashes[0])
        digital_signature.update(header._key())
        return base64.b64encode(digital_signature.digest())
