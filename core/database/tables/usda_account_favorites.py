from ..objects.usda_account_favorite import USDAAccountFavorite
from ..no_value import NoValue

NO_VALUE = NoValue()

class USDAAccountFavoritesException(Exception):
    def __init__(self, reason="unspecified"):
        super().__init__(reason)


class USDAAccountFavorites:
    """Model of favorite USDA locations for users"""
    
    def __init__(self, db):
        self._db = db

    def insert(self, account, state, city_id):
        # Check if data is already in DB, if so don't add
        if (self.check_if_data_exists(account, state, city_id) == False):
            self._db.execute(
                """INSERT IGNORE INTO usda_account_favorites
                    (account, state, city_id)
                    VALUES (%(account)s, %(state)s, %(city_id)s)
                """,
                {
                    "account": account,
                    "state": state,
                    "city_id": city_id
                }
            )

    def check_if_data_exists(self, account, state, city_id):
        """Checks if this data is already in the DB as to not 
            add duplicates.

        Params:
            account: User's account ID
            state: USDA Favorites' state
            city_id: USDA Favorites' city ID

        Returns:
            True if that data is already in the DB, false if not.
        """
        favorites = self._db.execute_d(
            """
                SELECT * FROM usda_account_favorites
                WHERE account=%(account)s 
                AND state=%(state)s
                AND city_id=%(city_id)s
            """,
            {
                "account": account,
                "state": state,
                "city_id": city_id,
            }
        )

        return len(favorites) != 0

    def get_by_id(self, favorite_id):
        """Gets the USDA Account Favorite by it's id.

        Params:
            favorite_id: USDAAccountFavorites' ID

        Returns:
            A USDAAccountFavorite object on success, or None on no match.
        """
        matching_favorites = self._db.execute_d(
            """
                SELECT * FROM usda_account_favorites
                WHERE
                    id=%(id)s
            """,
            {
                "id": favorite_id
            }
        )

        if len(matching_favorites) != 1:
            raise USDAAccountFavoritesException("No Favorites found with that ID.")
        return USDAAccountFavorite(self._db, matching_favorites[0])

    def delete(self, account, state, city_id):
        """Deletes Favorite with given info."""
        self._db.execute("""
            DELETE FROM usda_account_favorites
            WHERE account=%(account)s AND state=%(state)s
            AND city_id=%(city_id)s
            """,
            {
                "account": account,
                "state": state,
                "city_id": city_id
            }
        )

    def get_by_account_with_names(self, account):
        """Gets the favorites by account with their associated names.
        """
        matching_favorites = self._db.execute_d(
            """
                SELECT DISTINCT f.*, r.market_location_city AS "city_name" 
                FROM usda_account_favorites AS f
                INNER JOIN usda_reports AS r ON f.city_id=r.slug_id
                WHERE f.account=%(account)s 
            """,
            {
                "account": account
            }
        )

        if len(matching_favorites) > 0:
            return matching_favorites
        else:
            return []

    def get_favorites(self, account=NO_VALUE, state=NO_VALUE, 
                            city_id=NO_VALUE):
        """
        Get favorites by the values specified.

        Returns:
            A list of favorites(s) record if found else []
        """

        # base query
        base_query = "SELECT * FROM usda_account_favorites"

        query_conditions = []
        query_values = {}

        if account is not NO_VALUE:
            query_conditions.append(" account = %(account)s")
            query_values["account"] = account

        if state is not NO_VALUE:
            query_conditions.append(" state = %(state)s")
            query_values["state"] = state

        if city_id is not NO_VALUE:
            query_conditions.append(" city_id = %(city_id)s")
            query_values["city_id"] = city_id

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
