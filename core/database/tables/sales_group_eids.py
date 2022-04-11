from ..no_value import NoValue

NO_VALUE = NoValue()

class SalesGroupEIDsException(Exception):
    """SalesGroupEIDs generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupEIDsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class SalesGroupEIDs:

    def __init__(self, db):
        self._db = db

    def get_sales_group_eids(self, sales_group_id=NO_VALUE, eid=NO_VALUE):
        """
        Gets sales group eids row(s) based on provided arguments
        Params:
            sales_group_id: The sales group ID
            eid: EID

        Returns:
            A list of objects containing EID and corresponding sales group id
        """
        # base query
        base_query = "SELECT * FROM sales_group_eids"
        query_conditions = []
        query_values = {}

        if sales_group_id is not NO_VALUE:
            query_conditions.append(" sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id

        if eid is not NO_VALUE:
            query_conditions.append(" eid = %(eid)s")
            query_values["eid"] = eid

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        sales_group_eids_rows = self._db.execute_d(query, query_values)
        if len(sales_group_eids_rows) > 0:
            return sales_group_eids_rows
        else:
            return []

    def insert_sales_group_eids(self, sales_group_id, eids_and_visual_ids):
        """
        Inserts EIDs for a sales group

        Params:
            sales_group_id: The sales group id
            eids: EIDs which need to be added for a sales group
        """
        for eid_and_visual_id in eids_and_visual_ids:
            self._db.execute(
                """
                INSERT INTO sales_group_eids (sales_group_id, eid, visual_id)
                VALUES (%(sales_group_id)s, %(eid)s, %(visual_id)s)
                """,
                {
                    "sales_group_id": sales_group_id,
                    "eid": eid_and_visual_id["eid"],
                    "visual_id": eid_and_visual_id["visual_id"]
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
