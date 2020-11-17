class MatchesDataStringsException(Exception):
    """Matches data strings generic exception."""

    def __init__(self, reason):
        """Constructor for MatchesDataStrings.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class MatchesDataStrings:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, match_data_string_id):
        """Gets a match data string by an ID.

        Params:
            id: the match data string id
        
        Returns:
            A string (data)

        Raises:
            MatchesDataStringsException
        """
        match_data_string_rows = self._db.execute_d(
            """SELECT data FROM matches_data_strings
                WHERE id=%(id)s
            """,
            {
                "id": match_data_string_id
            }
        )
        if len(match_data_string_rows) != 1:
            raise MatchesDataStringsException("No match data string found with that ID.")
        return match_data_string_rows[0][0]

    def get_by_data(self, data):
        """Gets the match data ID representing data, or creates a new row if it does not exist

        Params:
            data: the match data (string)
        
        Returns:
            An int
        
        Raises:
            MatchesDataStringsException on multiple
        """
        # TODO: optimize
        match_data_string_rows = self._db.execute_d(
            """SELECT id FROM matches_data_strings
                WHERE data=%(data)s
            """,
            {
                "data": data
            }
        )
        if len(match_data_string_rows) == 1:
            return match_data_string_rows[0]["id"]
        if len(match_data_string_rows) > 1:
            raise MatchesDataStringsException("Multiple rows found with that data")
        self._insert(data)
        return self._db.last_row_id()

    def _insert(self, data):
        """Inserts a new row.

        Does NOT check for the data to be unique (use get_by_data)

        Params:
            data: The data string to insert
        """
        match_data_string_rows = self._db.execute_d(
            """INSERT INTO matches_data_strings
                (data)
                VALUES (%(data)s)
            """,
            {
                "data": data
            }
        )
