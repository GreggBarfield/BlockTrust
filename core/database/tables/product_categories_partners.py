from ..no_value import NoValue
NO_VALUE = NoValue()


class ProductCategoriesPartners:

    def __init__(self, db):
        self._db = db

    def get_product_categories_partners(self, id=NO_VALUE, product_category_id=NO_VALUE, partner_id=NO_VALUE):
        """
        Gets the product categories partner rows based on provided attributes

        Params:
            product_category_id: Product Category ID
            partner_id: partner_id

        Returns:
        A list of product category partners or an empty list
        """
        base_query = "SELECT * FROM product_categories_partners"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if product_category_id is not NO_VALUE:
            query_conditions.append("product_category_id = %(product_category_id)s")
            query_values["product_category_id"] = product_category_id
        if partner_id is not NO_VALUE:
            query_conditions.append("partner_id = %(partner_id)s")
            query_values["partner_id"] = partner_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        product_categories_partner_rows = self._db.execute_d(query, query_values)
        if len(product_categories_partner_rows) > 0:
            return product_categories_partner_rows
        else:
            return []

    def insert_product_categories_partner(self, product_category_id, partner_id):
        """
        Inserts a new product category in the table

        Params:
            category_name: Name of the new product category
        """
        self._db.execute(
            """
            INSERT INTO product_categories_partners (product_category_id, partner_id)
            VALUES (%(product_category_id)s, %(partner_id)s)
            """,
            {
                "product_category_id": product_category_id,
                "partner_id": partner_id
            }
        )
