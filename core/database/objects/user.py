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

    def is_user_locked(self):
        return self._row['is_user_locked']

    def failed_attempts(self):
        return self._row['failed_attempts']

    def locked_until_time(self):
        return self._row['locked_until_time']

    def phone(self):
        return self._row['phone']

    def is_system_generated(self):
        return self._row["is_system_generated"]
