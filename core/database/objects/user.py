from copy import deepcopy


class User:

    def __init__(self, db, row):
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

    def first_name(self):
        return self._row['first_name']

    def last_name(self):
        return self._row['last_name']

    def email(self):
        return self._row['email']

    def is_email_verified(self):
        return self._row['is_email_verified']

    def phone(self):
        return self._row['phone']
