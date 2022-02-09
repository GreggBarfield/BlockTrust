from ..objects.usda_account_favorite import USDAAccountFavorite

class USDAAccountFavoritesException(Exception):
    def __init__(self, reason="unspecified"):
        super().__init__(reason)


class USDAAccountFavorites:
    """Model of favorite USDA locations for users"""
    
    def __init__(self, db):
        self._db = db

    def insert(self, account, state, city_id, city_name):
        # Check if data is already in DB, if so don't add
        if (self.check_if_data_exists(account, state, city_id) == False):
            self._db.execute(
                """INSERT IGNORE INTO usda_account_favorites
                    (account, state, city_id, city_name)
                    VALUES (%(account)s, %(state)s, %(city_id)s, %(city_name)s)
                """,
                {
                    "account": account,
                    "state": state,
                    "city_id": city_id,
                    "city_name": city_name
                }
            )

    def get_by_id(self, favorite_id):
        """Gets the USDA Account Favorite by it's id.

        Params:
            favorite_id: USDAAccountFavorites' ID

        Returns:
            A USDAAccountFavorite object on success, or None on no match.
        """
        matching_reports = self._db.execute_d(
            """
                SELECT * FROM usda_account_favorites
                WHERE
                    id=%(id)s
            """,
            {
                "id": favorite_id
            }
        )

        if len(matching_reports) != 1:
            raise USDAAccountFavoritesException("No Favorites found with that ID.")
        return USDAAccountFavorite(self._db, matching_reports[0])

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

    def get_all_by_account(self, account):
        """Gets all USDA Account Favorites for an account

        Returns:
            A list of USDAAccountFavorite objects on success, or None on no match.
        """
        all_favorites = self._db.execute_d(
            """
                SELECT * FROM usda_account_favorites
                WHERE account=%(account)s
            """,
            {
                "account": account
            }
        )

        return all_favorites

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
