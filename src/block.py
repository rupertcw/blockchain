import abc
import base64
import logging
import utils

from abc import ABCMeta
from consensus import ProofOfWork
from datetime import date
from hasher import SingleTransactionHasher, MerkleTreeHasher

logger = logging.getLogger(__name__)


class BlockHeader(object):

    def __init__(self, block_number, previous_block_hash, key_store, mining_difficulty):
        self.block_hash = None
        self._block_number = block_number
        self._creation_date = date.today()
        self.previous_block_hash = previous_block_hash
        self.next_block = None
        self.block_signature = None
        self.key_store = key_store
        self.mining_difficulty = mining_difficulty
        self.nonce = 0

    def _key(self):
        return ','.join(map(str, (self._block_number, self._creation_date, self.previous_block_hash)))

    def __eq__(self, other):
        return self._key() == other._key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return '\n'.join([
            'HEADER:',
            'Block Hash: {0}'.format(self.block_hash),
            'Block Number: {0}'.format(self._block_number),
            'Creation Date: {0}'.format(self._creation_date),
            'Previous Block Hash: {0}'.format(self.previous_block_hash),
            'Next Block Hash: {0}'.format(self.next_block.header.block_hash if self.next_block else None),
            'Block Signature: {0}'.format(self.block_signature),
            'Mining difficulty: {0}'.format(self.mining_difficulty),
            'Nonce: {0}'.format(self.nonce),
        ])


class Block(object):

    __metaclass__ = ABCMeta

    def __init__(self, header, transactions):
        self.header = header
        self._txs = transactions
        self.header.block_hash, self.header.nonce = ProofOfWork.calculate(
            self.header.mining_difficulty, self.header.nonce, self.calculate_hash()
        )
        if self.header.key_store:
            self.header.block_signature = self.header.key_store.sign(self.header.block_hash)

    @abc.abstractmethod
    def calculate_hash(self):
        pass

    def is_valid_chain(self, previous_block_hash):
        if not self.header.key_store.verify(self.header.block_hash, self.header.block_signature):
            raise RuntimeError('Block integrity compromised!')

        new_block_hash = base64.b64encode(utils.to_SHA256(str(self.header.nonce), self.calculate_hash()))
        valid_signature = self.header.key_store.verify(new_block_hash, self.header.block_signature)
        logger.info('Valid signature? {0}'.format(valid_signature))
        if not valid_signature:
            raise RuntimeError('Block integrity compromised!')

        if new_block_hash != self.header.block_hash:
            is_valid = False
        else:
            is_valid = self.header.previous_block_hash == previous_block_hash

        if self.header.next_block:
            return self.header.next_block.is_valid_chain(new_block_hash)

        return is_valid

    def __repr__(self):
        return '\n'.join([
            str(self.header),
            '',
            '\n'.join(map(str, self._txs)),
            '',
        ])


class SingleTransactionBlock(Block):

    def calculate_hash(self):
        return SingleTransactionHasher.calculate_hash(self.header, self._txs)


class MultiTransactionBlock(Block):

    def calculate_hash(self):
        return MerkleTreeHasher.calculate_hash(self.header, self._txs)
