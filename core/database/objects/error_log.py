from copy import deepcopy

class ErrorLog:

    def __init__(self, db, row):
        """Error Log constructor.

        Params:
            db: Database object
            row: A 'Error Log' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)

    def id(self):
        return self._row['id']

    def component(self):
        return self._row['component']

    def short_error(self):
        return self._row['short_error']

    def long_error(self):
        return self._row['long_error']

    def details(self):
        return self._row['details']