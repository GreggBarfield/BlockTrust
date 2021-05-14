from copy import deepcopy


class AccountUser:

    def __init__(self, db, row):
        """AccountUser constructor.

        Params:
            db: Database object
            row: An 'account_users' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)

    def user_id(self):
        return self._row['user']

    def account_id(self):
        return self._row['account']

    def account(self):
        return self._db.accounts.get_by_account_user(self)
