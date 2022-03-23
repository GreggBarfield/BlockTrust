from ..no_value import NoValue

NO_VALUE = NoValue()

class USDAFavoritesForAccounts:
    """Model of favorite USDA locations for users"""
    
    def __init__(self, db):
        self._db = db

    def insert_usda_favorites_for_accounts(self, account_id, state, slug_id):
        # Check if data is already in DB, if so don't add
        if (self.get_usda_favorites_for_accounts(account_id=account_id, state=state, slug_id=slug_id) == []):
            self._db.execute(
                """INSERT INTO usda_favorites_for_accounts (account_id, state, slug_id)
                    VALUES (%(account_id)s, %(state)s, %(slug_id)s)
                """,
                {
                    "account_id": account_id,
                    "state": state,
                    "slug_id": slug_id
                }
            )

    def delete_usda_favorites_for_accounts(self, account_id, state, slug_id):
        """Deletes Favorite with given info."""
        self._db.execute("""
            DELETE FROM usda_favorites_for_accounts
            WHERE account_id=%(account_id)s AND state=%(state)s AND slug_id=%(slug_id)s
            """,
            {
                "account_id": account_id,
                "state": state,
                "slug_id": slug_id
            }
        )

    def get_favorites_for_account(self, account_id):
        """Gets the favorites by account_id with their associated names.
        """
        matching_favorites = self._db.execute_d(
            """
                SELECT DISTINCT f.*, r.market_location_city, r.market_location_name
                FROM usda_favorites_for_accounts AS f
                INNER JOIN usda_reports AS r ON f.slug_id=r.slug_id
                WHERE f.account_id=%(account_id)s 
            """,
            {
                "account_id": account_id
            }
        )

        if len(matching_favorites) > 0:
            return matching_favorites
        else:
            return []

    def get_usda_favorites_for_accounts(self, account_id=NO_VALUE, state=NO_VALUE, 
                            slug_id=NO_VALUE, id=NO_VALUE):
        """
        Get favorites by the values specified.

        Returns:
            A list of favorites(s) record if found else []
        """

        # base query
        base_query = "SELECT * FROM usda_favorites_for_accounts"

        query_conditions = []
        query_values = {}

        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id

        if state is not NO_VALUE:
            query_conditions.append(" state = %(state)s")
            query_values["state"] = state

        if slug_id is not NO_VALUE:
            query_conditions.append(" slug_id = %(slug_id)s")
            query_values["slug_id"] = slug_id

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        favorites_rows = self._db.execute_d(query, query_values)
        if len(favorites_rows) > 0:
            return favorites_rows
        else:
            return []
