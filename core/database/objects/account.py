from copy import deepcopy
from ...sectors import sectors_by_id
from ..tables.account_users import AccountUsersException


class AccountException(Exception):
    """Generic account exception."""

    def __init__(self, reason):
        """Constructor for AccountException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Account:

    def __init__(self, db, row):
        """User constructor.

        Params:
            db: Database object
            row: An 'accounts' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)
        self._account_links = None

    def id(self):
        return self._row['id']

    def company(self):
        return self._row['company']

    def token(self):
        return self._row['token']

    def sector_id(self):
        return self._row['sector']

    def sector_name(self):
        return sectors_by_id[self._row['sector']]

    def partner_account(self):
        return self._row['partner_account']

    def affiliate_id(self):
        return self._row['affiliate_id']

    def address(self):
        return self._row['address']

    def city(self):
        return self._row['city']

    def state(self):
        return self._row['state']

    def zip(self):
        return self._row['zip']

    def phone(self):
        return self._row['phone']

    def stripe_paid(self):
        return self._row['stripe_paid']

    def manual_paid(self):
        return self._row['manual_paid']

    def generated_paid(self):
        return self._row['generated_paid']

    def stripe_customer_id(self):
        return self._row['stripe_customer_id']

    def partner_stripe_publishable_key(self):
        return self._row['partner_stripe_publishable_key']

    def partner_stripe_secret_key(self):
        return self._row['partner_stripe_secret_key']

    def add_user(self, user, is_admin=0):
        """Add a user to this account.

        Params:
            user: a User object to add
        """
        try:
            self._db.account_users.add_user_to_account(user, self, is_admin)
        except AccountUsersException as e:
            raise AccountException("Failed to add user to the account: " + str(e))

    def account_links(self, allow_cache=True):
        """Get account's account links

        Params:
            allow_cache: Allow this to come from the cache (default True)

        Returns:
            a (possibly empty) list of AccountLink objects
        """
        if not allow_cache or not self._account_links:
            self._account_links = self._db.account_links.get_by_account_id(self.id())
        return self._account_links
