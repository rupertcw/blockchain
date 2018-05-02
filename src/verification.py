import config
import logging

from block import BlockHeader, SingleTransactionBlock, MultiTransactionBlock
from blockchain import Blockchain
from keystore import KeyStore


logger = logging.getLogger(__name__)


def verify_single_block_single_transaction_blockchain(tx_pool):
    blockchain = Blockchain()
    key_store = KeyStore()

    for block_number in xrange(config.BLOCKCHAIN_LENGTH):
        previous_block_hash = blockchain.current_block.header.block_hash if not blockchain.is_empty() else None
        header = BlockHeader(block_number, previous_block_hash, key_store, config.MINING_DIFFICULTY)
        txs = [tx_pool.get()]
        block = SingleTransactionBlock(header, txs)

        if previous_block_hash:
            blockchain.current_block.header.next_block = block

        blockchain.accept_block(block)

    for block in blockchain:
        print block
        logger.info(block)

    blockchain.verify_chain()


def verify_single_block_multi_transaction_blockchain(tx_pool):
    blockchain = Blockchain()
    key_store = KeyStore()

    block_number = 0
    previous_block_hash = blockchain.current_block.block_hash if not blockchain.is_empty() else None
    header = BlockHeader(block_number, previous_block_hash, key_store, config.MINING_DIFFICULTY)
    txs = [tx_pool.get() for i in xrange(config.BLOCKCHAIN_LENGTH)]
    block = MultiTransactionBlock(header, txs)

    if previous_block_hash:
        blockchain.current_block.header.next_block = block

    blockchain.accept_block(block)

    print block
    logger.info(block)

    blockchain.verify_chain()
