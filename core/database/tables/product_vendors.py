from ..no_value import NoValue
NO_VALUE = NoValue()

HERD_WHISTLE_VENDOR_NAME = "Herd Whistle"

class ProductVendors:

    def __init__(self, db):
        self._db = db

    def get_product_vendors(self, id=NO_VALUE, vendor_name=NO_VALUE, vendor_email=NO_VALUE):
        """
        Returns product vendors based on attributes provided

        Params:
            id: Vendor ID
            vendor_name: Name of vendor
            vendor_email: Email of vendor

        Returns:
            A list of relevant product vendors or an empty list
        """
        base_query = "SELECT * FROM product_vendors"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if vendor_name is not NO_VALUE:
            query_conditions.append("vendor_name = %(vendor_name)s")
            query_values["vendor_name"] = vendor_name
        if vendor_email is not NO_VALUE:
            query_conditions.append("vendor_email = %(vendor_email)s")
            query_values["vendor_email"] = vendor_email

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        product_vendor_rows = self._db.execute_d(query, query_values)
        if len(product_vendor_rows) > 0:
            return product_vendor_rows
        else:
            return []

    def insert_product_vendor(self, vendor_name, vendor_email):
        """
        Inserts a new product vendor in the table

        Params:
            vendor_name: Name of the new product vendor
            vendor_email: Email of new vendor
        """
        self._db.execute(
            """
            INSERT INTO product_categories (vendor_name, vendor_email)
            VALUES (%(vendor_name)s, %(vendor_email)s)
            """,
            {
                "vendor_name": vendor_name,
                "vendor_email": vendor_email
            }
        )
        product_vendor_rows = self.get_product_vendors(id=self._db.last_row_id())
        return product_vendor_rows[0]