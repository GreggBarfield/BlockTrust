import json

class SalesGroupsException(Exception):
    """Sales groups generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class SalesGroups:

    def __init__(self, db):
        self._db = db
        

    def _translate_json(self, d):
        to_process = d

        if not isinstance(d, list):
            to_process = [d]
        
        for d_actual in to_process:
            if d_actual is not None:
                if d_actual["reported"] is not None:
                    d_actual["reported"] = json.loads(d_actual["reported"])
        return d


    def row_by_id(self, row_id):
        """Gets a sales group row by an ID.

        Params:
            row_id: the row id
        
        Returns:
            A dictionary (w/ JSON pre-converted)

        Raises:
            SalesGroupsException
        """
        sales_groups = self._db.execute_d(
            """SELECT * FROM sales_groups
                WHERE id=%(id)s
            """,
            {
                "id": row_id
            }
        )
        if len(sales_groups) != 1:
            raise SalesGroupsException("No sales group found with that ID.")
        return self._translate_json(sales_groups[0])

    def rows_by_account(self, account):
        """Gets sales group rows by an account.

        Params:
            account: the account id
        
        Returns:
            A list of dictionaries

        Raises:
            SalesGroupsException
        """
        sales_groups = self._db.execute_d(
            """SELECT * FROM sales_groups
                WHERE account=%(account)s
            """,
            {
                "account": account
            }
        )
        return self._translate_json(sales_groups)

    def insert(self, account_id, reported):
        """Inserts a new row.

        Params:
            account_id: The owner of sales group
            reported: A dictionary of the user's self-reported information

        Returns:
            The sales group row inserted
        """
        self._db.execute_d(
            """INSERT INTO sales_groups
                (account, reported)
                VALUES (%(account)s, %(reported)s)
            """,
            {
                "account": account_id,
                "reported": json.dumps(reported)  # Does this need to be converted to a string first?
            }
        )
        return self.row_by_id(self._db.last_row_id())
