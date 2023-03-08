from ..no_value import NoValue

NO_VALUE = NoValue()

# TABLE_COLUMNS = ("id", "owner_account_id", "viewer_account_id", "viewer_user_id", "data_type_id",
#                  "created_timestamp", "last_updated_timestamp")

TRANSACTION_TYPE_NAMES_TO_IDS = {
    "Subscription": 1
}

TRANSACTION_TYPE_IDS_TO_NAMES = {value: key for key, value in TRANSACTION_TYPE_NAMES_TO_IDS.items()}


class Transactions:

    def __init__(self, db):
        self._db = db

    def insert_transaction(self, transaction_type_id, purchasing_partner_id, account_credits_purchased):
        """
        Inserts a new transaction record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO transactions (transaction_type_id, purchasing_partner_id, account_credits_purchased)
                VALUES (%(transaction_type_id)s, %(purchasing_partner_id)s, %(account_credits_purchased)s)
            """,
            {
                "transaction_type_id": transaction_type_id,
                "purchasing_partner_id": purchasing_partner_id,
                "account_credits_purchased": account_credits_purchased
            }
        )
        return self._db.last_row_id()

    # def get_view_logs(self, id=NO_VALUE, owner_account_id=NO_VALUE, viewer_account_id=NO_VALUE, data_type_id=NO_VALUE, 
    #                   get_related_details=False):
    #     """
    #     Gets the view logs based on the provided parameters

    #     Returns:
    #         A list of view logs or an empty array
    #     """
    #     if get_related_details:
    #         base_query = """
    #             SELECT vl.*, a.company, CONCAT(u.first_name,' ',u.last_name) as 'user_name' FROM view_logs vl
    #             INNER JOIN accounts a on a.id = vl.viewer_account_id
    #             LEFT JOIN users u ON u.id = vl.viewer_user_id
    #         """
    #     else:
    #         base_query = "SELECT * FROM view_logs vl"

    #     query_conditions = []
    #     query_values = {}
    #     if id is not NO_VALUE:
    #         query_conditions.append("vl.id = %(id)s")
    #         query_values["id"] = id
    #     if owner_account_id is not NO_VALUE:
    #         query_conditions.append("owner_account_id = %(owner_account_id)s")
    #         query_values["owner_account_id"] = owner_account_id
    #     if viewer_account_id is not NO_VALUE:
    #         query_conditions.append("viewer_account_id = %(viewer_account_id)s")
    #         query_values["viewer_account_id"] = viewer_account_id
    #     if data_type_id is not NO_VALUE:
    #         query_conditions.append("data_type_id = %(data_type_id)s")
    #         query_values["data_type_id"] = data_type_id

    #     if len(query_conditions) >= 1:
    #         combined_query_condition = " WHERE " + " AND ".join(query_conditions)
    #     else:
    #         combined_query_condition = ""
    #     query = base_query + combined_query_condition + " ORDER BY ID DESC"
    #     view_log_rows = self._db.execute_d(query, query_values)

    #     if len(view_log_rows) > 0:
    #         return view_log_rows
    #     else:
    #         return []
