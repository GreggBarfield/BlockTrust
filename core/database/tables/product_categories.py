from ..no_value import NoValue
NO_VALUE = NoValue()


class ProductCategories:

    def __init__(self, db):
        self._db = db

    def get_product_categories(self, id=NO_VALUE, category_name=NO_VALUE):
        """
        Returns all product categories

        Returns:
            A list of all product categories
        """
        base_query = "SELECT * FROM product_categories"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if category_name is not NO_VALUE:
            query_conditions.append("category_name = %(category_name)s")
            query_values["category_name"] = category_name

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        product_category_rows = self._db.execute_d(query, query_values)
        if len(product_category_rows) > 0:
            return product_category_rows
        else:
            return []

    def insert_product_category(self, category_name):
        """
        Inserts a new product category in the table

        Params:
            category_name: Name of the new product category
        """
        self._db.execute(
            """
            INSERT INTO product_categories (category_name)
            VALUES (%(category_name)s)
            """,
            {
                "category_name": category_name
            }
        )
        product_category_rows = self.get_product_categories(id=self._db.last_row_id())
        return product_category_rows[0]
