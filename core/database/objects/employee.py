from copy import deepcopy


class Employee:

    def __init__(self, row):
        """Employee constructor.

        Params:
            row: An 'employee' row dictionary
        """
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

    def phone(self):
        return self._row['phone']