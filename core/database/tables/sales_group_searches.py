from ..no_value import NoValue

NO_VALUE = NoValue()


class SalesGroupSearches:

    def __init__(self, db):
        self._db = db

    def insert(self, name, user_id, radius=None, zip=None, category=None, breed=None, minimum_weight=None,
               preconditioning_program=None, process_verified_program=None):
        """
        Inserts a new sales group search

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO sales_group_searches (name, user_id, radius, zip, category, breed, minimum_weight,
                    preconditioning_program, process_verified_program)
                VALUES (%(name)s, %(user_id)s, %(radius)s, %(zip)s, %(category)s, %(breed)s, %(minimum_weight)s,
                    %(preconditioning_program)s, %(process_verified_program)s)
            """,
            {
                "name": name,
                "user_id": user_id,
                "radius": radius,
                "zip": zip,
                "category": category,
                "breed": breed,
                "minimum_weight": minimum_weight,
                "preconditioning_program": preconditioning_program,
                "process_verified_program": process_verified_program
            }
        )
        return self._db.last_row_id()

    def get(self, id=NO_VALUE, user_id=NO_VALUE):
        """
        Gets the sales group search based on the provided parameters

        Returns:
            A list of sales group search or an empty array
        """

        base_query = "SELECT * FROM sales_group_searches"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if user_id is not NO_VALUE:
            query_conditions.append("user_id = %(user_id)s")
            query_values["user_id"] = user_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition + " ORDER BY ID DESC"
        rows = self._db.execute_d(query, query_values)

        if len(rows) > 0:
            return rows
        else:
            return []
