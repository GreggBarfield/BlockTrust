from ..frag import frag, frag_insert_into
from .. import database


class SalesGroupEIDsException(Exception):
    """SalesGroupEIDs generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupEIDsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class SalesGroupEIDs:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def get_sales_group_eids(self, sales_group_id):
        """
        Gets all EIDs for a sales group.
        Params:
            sales_group_id: The sales group ID

        Returns:
            A list of objects containing EID and corresponding sales group id
        """
        eid_rows = self._db.execute_d(
            """
            SELECT * FROM sales_group_eids
            WHERE sales_group_id = %(sales_group_id)s
            """,
            {
                "sales_group_id": sales_group_id
            }
        )
        return eid_rows

    def insert_sales_group_eids(self, sales_group_id, eids):
        """
        Inserts EIDs for a sales group

        Params:
            sales_group_id: The sales group id
            eids: EIDs which need to be added for a sales group
        """
        for eid in eids:
            self._db.execute(
                """
                INSERT INTO sales_group_eids (sales_group_id, eid)
                VALUES (%(sales_group_id)s, %(eid)s)
                """,
                {
                    "sales_group_id": sales_group_id,
                    "eid": eid
                }
            )

    def delete_sales_group_eids(self, sales_group_id):
        """
        Deletes eid rows of a sales group

        Params:
            sales_group_id: The sales group ID
        """
        self._db.execute(
            """
            DELETE FROM sales_group_eids
            WHERE sales_group_id = %(sales_group_id)s
            """,
            {
                "sales_group_id": sales_group_id
            }
        )

    def update_sales_group_eids(self, sales_group_id, eids):
        """
        Update eids for a sales group

        Params:
            sales_group_id: Sales group ID
            eids: Alist of new eids for a sales group
        """
        self.delete_sales_group_eids(sales_group_id)
        self.insert_sales_group_eids(sales_group_id, eids)
