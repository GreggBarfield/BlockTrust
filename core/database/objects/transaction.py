from copy import deepcopy


class Transaction:

    def __init__(self, db, row):
        """Transaction constructor.

        Params:
            db: Database object
            row: An 'orders' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)

    def id(self):
        return self._row['id']

    def account(self):
        return self._row['account']

    def amount(self):
        return self._row['amount']

    def type(self):
        return self._row['type']

    def create_timestamp(self):
        return self._row['create_timestamp']
