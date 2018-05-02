import config
import verification

from datetime import date
from Queue import Queue
from transaction import Transaction


claim_numbers = range(config.BLOCKCHAIN_LENGTH)
settlement_amount = 10.0
settlement_date = date.today()
registration_plate = 'RR1001RR'
mileage = 1000.1
claim_type = 'Total Loss'


def populate_transaction_pool(tx_pool):
    for block_number in xrange(config.BLOCKCHAIN_LENGTH):
        tx_pool.put(
            Transaction(
                claim_numbers[block_number],
                settlement_amount,
                settlement_date,
                registration_plate,
                mileage,
                claim_type
            )
        )

tx_pool = Queue(config.BLOCKCHAIN_LENGTH)
populate_transaction_pool(tx_pool)

if config.VERIFICATION_TYPE == 'SBST':
    verification.verify_single_block_single_transaction_blockchain(tx_pool)
else:
    verification.verify_single_block_multi_transaction_blockchain(tx_pool)

