from copy import deepcopy

class AccountLinkException(Exception):
    """Generic account link exception."""

    def __init__(self, reason):
        """Constructor for AccountLinkException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class AccountLink:

    def __init__(self, account_link_row):
        """AccountLink constructor.

        Params:
            account_link_row: The account link's database row
        """
        self._row = deepcopy(account_link_row)


    def id(self):
        """Gets link ID

        Returns:
            The ID
        """
        return self._row['id']

    def partner_account_id(self): 
        """Gets the partner_account attached to the link

        Returns:
            An int or None
        """
        return self._row['partner_account']

    def account_id(self):
        """Gets the account ID attached to the link

        Returns:
            An account ID or None
        """
        return self._row['account']

    def company(self):
        """Gets the company attached to the link

        Returns:
            A str or None
        """
        return self._row['company']

    def affiliate_id(self):
        """Gets the affiliate_id attached to the link

        Returns:
            An int or None
        """
        return self._row['affiliate_id']

    def sector(self):
        """Gets the sector ID attached to the link.

        Returns:
            An int or None
        """
        return self._row['sector']
