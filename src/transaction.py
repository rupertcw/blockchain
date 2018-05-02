import utils


class Transaction(object):

    def __init__(self, claim_number, settlement_amount, settlement_date, registration_plate, mileage, claim_type):
        self._claim_number = claim_number
        self._settlement_amount = settlement_amount
        self._settlement_date = settlement_date
        self._registration_plate = registration_plate
        self._mileage = mileage
        self._claim_type = claim_type

    def _key(self):
        return ','.join(map(str, (self._claim_number, self._settlement_amount, self._settlement_date, self._registration_plate, self._mileage, self._claim_type)))

    def __eq__(self, other):
        return self._key() == other._key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return utils.to_SHA256(self._key())

    def __repr__(self):
        return '\n'.join([
            'TX:',
            'Claim Number: {0}'.format(self._claim_number),
            'Settlement Amount: {0}'.format(self._settlement_amount),
            'Settlement Date: {0}'.format(self._settlement_date),
            'Registration Plate: {0}'.format(self._registration_plate),
            'Mileage: {0}'.format(self._mileage),
            'Claim Type: {0}'.format(self._claim_type),
        ])
