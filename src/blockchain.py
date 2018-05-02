import logging

from collections import Iterable

logger = logging.getLogger(__name__)

class Blockchain(Iterable):

    def __init__(self):
        self._head_block = None
        self.current_block = None
        self._blocks = []

    def __iter__(self):
        for block in self._blocks:
            yield block

    def is_empty(self):
        return not self._head_block

    def accept_block(self, block):
        if not self._head_block:
            self._head_block = block

        self.current_block = block
        self._blocks.append(block)

    def verify_chain(self):
        if not self._head_block:
            raise RuntimeError('No genesis block!')

        is_valid = self._head_block.is_valid_chain(None)

        if is_valid:
            print 'Valid blockchain!'
            logger.info('Valid blockchain!')
        else:
            print 'Invalid blockchain!'
            logger.error('Invalid blockchain!')
