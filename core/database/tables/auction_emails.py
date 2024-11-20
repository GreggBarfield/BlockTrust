from ..no_value import NoValue

NO_VALUE = NoValue()

TABLE_COLUMNS = ("id", "account_id", "name", "email", "created_timestamp", "last_updated_timestamp")


class AuctionEmails:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id, name, email):
        """
        Inserts a new account_email record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO auction_emails (account_id, name, email)
                VALUES (%(account_id)s, %(name)s, %(email)s)
            """,
            {
                "account_id": account_id,
                "name": name,
                "email": email
            }
        )
        return self._db.last_row_id()

    def get(self, id=NO_VALUE, account_id=NO_VALUE, email=NO_VALUE):
        """
        Gets the auction emails based on the provided parameters

        Returns:
            A list of auction emails or an empty array
        """
        base_query = "SELECT * FROM auction_emails"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s")
            query_values["email"] = email
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition + " ORDER BY ID DESC"
        rows = self._db.execute_d(query, query_values)

        if len(rows) > 0:
            return rows
        else:
            return []

    def delete(self, id):
        self._db.execute(
            """
                DELETE FROM auction_emails WHERE id = %(id)s
            """,
            {
                "id": id
            }
        )
        return self._db.row_count()
