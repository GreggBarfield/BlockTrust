from ..no_value import NoValue

NO_VALUE = NoValue()

class NotInterestedSalesGroupIdsForAccounts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=NO_VALUE, sales_group_id=NO_VALUE):
        """
        Insert a new row for not interested sales group for account

        Params:
            account_id: ID of the account
            sales_group_id: ID of uninterested Sales Group
        """
        self._db.execute(
            """
            INSERT INTO not_interested_sales_group_ids_for_accounts(account_id, sales_group_id)
            VALUES(%(account_id)s, %(sales_group_id)s)
            """,
            {
                "account_id": account_id,
                "sales_group_id": sales_group_id
            }
        )

    def get(self, id=NO_VALUE, account_id=NO_VALUE, sales_group_id=NO_VALUE):
        """
        Get not interested sales group based on attributes provided

        Params:
            id: ID of the uninterested sales group row
            account_id: ID of the account
            sales_group_id: ID of uninterested Sales Group
        Returns:
            Rows based on attributes provided
        """

        base_query = "SELECT * FROM not_interested_sales_group_ids_for_accounts"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if sales_group_id is not NO_VALUE:
            query_conditions.append("sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        rows = self._db.execute_d(query, query_values)
        return rows

    def update(self, id, field_id=NO_VALUE, account_id=NO_VALUE, sales_group_id=NO_VALUE):
        """
        Updates the row based on the provided attributes

        Params:
            id: ID of the uninterested sales group row
            account_id: ID of the account
            sales_group_id: ID of uninterested Sales Group
        """
        base_query = "UPDATE not_interested_sales_group_ids_for_accounts"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if field_id is not NO_VALUE:
            query_conditions.append("field_id = %(field_id)s")
            query_values["field_id"] = field_id
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if sales_group_id is not NO_VALUE:
            query_conditions.append("sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")