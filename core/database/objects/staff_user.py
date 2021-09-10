from copy import deepcopy
from .. import database


class StaffUser:

    def __init__(self, db: 'database.Database', row):
        """Staff user constructor.

        Params:
            db: Database object
            row: A 'staff user' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)
        del self._row["password"]

    def id(self):
        return self._row['id']

    def first_name(self):
        return self._row['first_name']

    def last_name(self):
        return self._row['last_name']

    def username(self):
        return self._row['username']

    def email(self):
        return self._row['email']

    def phone(self):
        return self._row['phone']

    def is_admin(self):
        return self._row['is_admin']