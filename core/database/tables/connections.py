from .accounts import Accounts


class Connections:

    def __init__(self, db):
        self._db = db

    def get_account_connections(self, account_id):
        """
        Params:
            account_id: Account ID whose connections are requested

        Returns:
            connections: List of connected accounts

        """
        connections = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE user_account_id= %(account_id)s
            """,
            {
                "account_id": account_id
            }
        )
        return connections

    def create_account_connection(self, user_account_id, friend_account_id):
        """
        Params:
            user_account_id: Account ID of user
            friend_account_id:
        Returns:
            None
        """
        user_account = Accounts.accounts.get_by_id(user_account_id)
        friend_account = Accounts.accounts.get_by_id(friend_account_id)
        user_account_name = user_account.name()
        friend_account_name = friend_account.name()
        # We add two entries per connection with each of the accounts having an entry under user_account_id
        # This helps save time during lookup and simplifies generating the account connection list
        self._db.execute(
            """
                INSERT INTO  connections
                    (friend_account_id,friend_account_name,user_account_id)
                    VALUES
                        (%(friend_account_id)s, %(friend_account_name)s, %(user_account_id)s)
            """,
            {
                "friend_account_id": friend_account_id,
                "friend_account_name": friend_account_name,
                "user_account_id": user_account_id
            }
        )
        self._db.execute(
            """
                INSERT INTO  connections
                    (friend_account_id,friend_account_name,user_account_id)
                    VALUES
                        (%(friend_account_id)s, %(friend_account_name)s, %(user_account_id)s)
            """,
            {
                "friend_account_id": user_account_id,
                "friend_account_name": user_account_name,
                "user_account_id": friend_account_id
            }
        )
