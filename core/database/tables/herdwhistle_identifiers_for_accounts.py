from ..no_value import NoValue

NO_VALUE = NoValue()


class HerdwhistleIdentifiersForAccounts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, herdwhistle_customer_id=None, herdwhistle_customer_shipping_id=None):
        """
        Inserts the Herwhistle identifiers for an account on placing an order

        Params:
            herwhistle_customer_id: Herwhistle Customer ID for given account
            herdwhistle_customer_shipping_id: Herwhistle Shipping ID for given account
        """
        self._db.execute(
            """
            INSERT INTO herdwhistle_identifiers_for_accounts (account_id, herdwhistle_customer_id, herdwhistle_customer_shipping_id)
            VALUES (%(account_id)s, %(herdwhistle_customer_id)s, %(herdwhistle_customer_shipping_id)s)
            """,
            {
                "account_id": account_id,
                "herdwhistle_customer_id": herdwhistle_customer_id,
                "herdwhistle_customer_shipping_id": herdwhistle_customer_shipping_id
            }
        )

    def get(self, id=NO_VALUE, account_id=NO_VALUE, herwhistle_customer_id=NO_VALUE,
            herdwhistle_customer_shipping_id=NO_VALUE):
        """
        Gets the Herwhistle identifiers for an account based on attributed provided

        Params:
            herwhistle_customer_id: Herwhistle Customer ID for given account
            herdwhistle_customer_shipping_id: Herwhistle Shipping ID for given account

        Returns:
            Herdwhistle identifier rows based on attributes provided
        """
        base_query = "SELECT * FROM herdwhistle_identifiers_for_accounts"

        query_conditions = []
        query_values = {}


        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if herwhistle_customer_id is not NO_VALUE:
            query_conditions.append(" herwhistle_customer_id = %(herwhistle_customer_id)s")
            query_values["herwhistle_customer_id"] = herwhistle_customer_id
        if herdwhistle_customer_shipping_id is not NO_VALUE:
            query_conditions.append(" herdwhistle_customer_shipping_id = %(herdwhistle_customer_shipping_id)s")
            query_values["herdwhistle_customer_shipping_id"] = herdwhistle_customer_shipping_id
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        herdwhistle_identifiers_for_accounts_rows = self._db.execute_d(query, query_values)
        if len(herdwhistle_identifiers_for_accounts_rows) > 0:
            return herdwhistle_identifiers_for_accounts_rows
        else:
            return []