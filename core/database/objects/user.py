from copy import deepcopy
from .. import database


class User:

    def __init__(self, db: 'database.Database', row):
        """User constructor.

        Params:
            db: Database object
            row: A 'users' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)
        del self._row["password"]

    def username(self):
        return self._row['username']

    def id(self):
        return self._row['id']

    def first(self):
        return self._row['first']

    def last(self):
        return self._row['last']

    def email(self):
        return self._row['email']

    def email_verified(self):
        return self._row('email_verified')

    def id(self):
            return self._row['phone']