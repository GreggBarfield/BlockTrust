from ..no_value import NoValue

NO_VALUE = NoValue()


class VendorIdentifiersForAccounts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, product_vendor_id=NO_VALUE, vendor_customer_id=None, vendor_customer_shipping_id=None):
        """
        Inserts the Vendor identifiers for an account on placing an order

        Params:
            vendor_customer_id: Vendor Customer ID for given account
            vendor_customer_shipping_id: Vendor Shipping ID for given account
        """
        self._db.execute(
            """
            INSERT INTO vendor_identifiers_for_accounts (account_id, product_vendor_id, vendor_customer_id, vendor_customer_shipping_id)
            VALUES (%(account_id)s, %(product_vendor_id)s, %(vendor_customer_id)s, %(vendor_customer_shipping_id)s)
            """,
            {
                "account_id": account_id,
                "product_vendor_id": product_vendor_id,
                "vendor_customer_id": vendor_customer_id,
                "vendor_customer_shipping_id": vendor_customer_shipping_id
            }
        )

    def get(self, id=NO_VALUE, account_id=NO_VALUE, product_vendor_id=NO_VALUE, vendor_customer_id=NO_VALUE,
            vendor_customer_shipping_id=NO_VALUE):
        """
        Gets the Vendor identifiers for an account based on attributed provided

        Params:
            vendor_customer_id: Vendor Customer ID for given account
            vendor_customer_shipping_id: Vendor Shipping ID for given account

        Returns:
            vendor identifier rows based on attributes provided
        """
        base_query = "SELECT * FROM vendor_identifiers_for_accounts"

        query_conditions = []
        query_values = {}


        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if product_vendor_id is not NO_VALUE:
            query_conditions.append(" product_vendor_id = %(product_vendor_id)s")
            query_values["product_vendor_id"] = product_vendor_id
        if vendor_customer_id is not NO_VALUE:
            query_conditions.append(" vendor_customer_id = %(vendor_customer_id)s")
            query_values["vendor_customer_id"] = vendor_customer_id
        if vendor_customer_shipping_id is not NO_VALUE:
            query_conditions.append(" vendor_customer_shipping_id = %(vendor_customer_shipping_id)s")
            query_values["vendor_customer_shipping_id"] = vendor_customer_shipping_id
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        vendor_identifiers_for_accounts_rows = self._db.execute_d(query, query_values)
        if len(vendor_identifiers_for_accounts_rows) > 0:
            return vendor_identifiers_for_accounts_rows
        else:
            return []