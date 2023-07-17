from copy import deepcopy
from ...match_types import MATCH_TYPES_ID_TO_NAME

class MatchException(Exception):
    """Generic match exception."""

    def __init__(self, reason):
        """Constructor for MatchException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Match:

    def __init__(self, db, row):
        """Match constructor.

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


    def partner_account_id(self):
        """Gets match account ID

        (This is the data owner)
        
        Returns:
            The account ID
        """
        return self._row['partner_account']


    def account_link_id(self):
        """Gets match account link ID

        (This is the account link that the data is associated with)
        
        Returns:
            The account link ID
        """
        return self._row['account_link']


    def eid(self):
        """Gets match EID
        
        Returns:
            The match EID
        """
        return self._row['eid']


    def lat(self):
        """Gets match lattitude, if it exists
        
        Returns:
            The match lattitude, or None
        """
        return self._row['lat']


    def lon(self):
        """Gets match longitude, if it exists
        
        Returns:
            The match longitude, or None
        """
        return self._row['lon']


    def time(self):
        """Gets match time, if it exists
        
        (This was when the data was originally generated, so likely when the animal was scanned)

        Returns:
            The match time, or None
        """
        return self._row['time']


    def created(self):
        """Gets match time created

        (This was the time when it was uploaded to the system)

        Returns:
            The match time created
        """
        return self._row['created']


    def type_str(self):
        """Gets the type string

        Returns:
            The type of data (as a string)
        """
        return MATCH_TYPES_ID_TO_NAME[self._row['type']]


    def type_id(self):
        """Gets the type ID

        Returns:
            The type of data (as an int)
        """
        return self._row['type']
    

    def data(self):
        """Gets the raw match data

        Returns:
            The raw match data as unencoded json
        """
        return self._row['data']

    def row(self):
        """Returns the row data."""
        return self._row
