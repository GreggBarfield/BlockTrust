class SalesGroupEIDsException(Exception):
    """Sales group eids generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupEIDsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class SalesGroupEIDs:

    def __init__(self, db):
        self._db = db

    def row_by_id(self, row_id):
        """Gets a sales group EID row by an ID.

        Params:
            row_id: the row id
        
        Returns:
            A dictionary

        Raises:
            SalesGroupsException
        """
        sales_group_eids = self._db.execute_d(
            """SELECT * FROM sales_group_eids
                WHERE id=%(id)s
            """,
            {
                "id": row_id
            }
        )
        if len(sales_group_eids) != 1:
            raise sales_group_eids("No sales group EID found with that ID.")
        return sales_group_eids[0]

    def rows_by_sales_group(self, sales_group):
        """Gets sales group EIDs for a specific sales group.

        Params:
            id: the match data string id
        
        Returns:
            A list of dictionaries

        Raises:
            SalesGroupsException
        """
        sales_group_eids = self._db.execute_d(
            """SELECT * FROM sales_group_eids
                WHERE sales_group=%(sales_group)s
            """,
            {
                "sales_group": sales_group
            }
        )
        return sales_group_eids

    def insert(self, eid, sales_group):
        """Inserts a new row.

        Params:
            eid: An integer containing the EID to add to the sales group
            sales_group: The sales group to bind to
        """
        self._db.execute_d(
            """INSERT INTO sales_groups
                (eid, sales_group)
                VALUES (%(eid)s, %(sales_group)s)
            """,
            {
                "eid": eid,
                "sales_group": sales_group
            }
        )
