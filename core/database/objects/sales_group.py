from copy import deepcopy

class SalesGroupException(Exception):
    """Generic sales group exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class SalesGroup:

    def __init__(self, db, row):
        """SalesGroup constructor.

        Params:
            db: Database object
            row: A 'matches' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)


    def id(self):
        """Gets match ID
        
        Returns:
            The match ID
        """
        return self._row['id']

