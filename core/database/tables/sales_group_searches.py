from json import dumps, loads
from ..no_value import NoValue

NO_VALUE = NoValue()


class SalesGroupSearches:

    def __init__(self, db):
        self._db = db

    def insert(self, name, user_id, radius=None, zip=None, minimum_weight=None,
               preconditioning_program=None, target_date_description=None, multi_select_fields=None):
        """
        Inserts a new sales group search

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO sales_group_searches (name, user_id, radius, zip, minimum_weight,
                    preconditioning_program, target_date_description, multi_select_fields)
                VALUES (%(name)s, %(user_id)s, %(radius)s, %(zip)s, %(minimum_weight)s,
                    %(preconditioning_program)s, %(target_date_description)s, %(multi_select_fields)s)
            """,
            {
                "name": name,
                "user_id": user_id,
                "radius": radius,
                "zip": zip,
                "minimum_weight": minimum_weight,
                "preconditioning_program": preconditioning_program,
                "target_date_description": target_date_description,
                "multi_select_fields": dumps(multi_select_fields) if multi_select_fields else None
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
            for row in rows:
                row["multi_select_fields"] = loads(row["multi_select_fields"]) if row["multi_select_fields"] else None
            return rows
        else:
            return []

    def update(self, id, name=NO_VALUE, radius=NO_VALUE, zip=NO_VALUE,
               minimum_weight=NO_VALUE, preconditioning_program=NO_VALUE, target_date_description=NO_VALUE,
               multi_select_fields=NO_VALUE):
        """
        Update sales group search

        Returns:
            id of row inserted
        """

        base_query = "UPDATE sales_group_searches"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if name is not NO_VALUE:
            query_conditions.append("name = %(name)s")
            query_values["name"] = name
        if radius is not NO_VALUE:
            query_conditions.append("radius = %(radius)s")
            query_values["radius"] = radius
        if zip is not NO_VALUE:
            query_conditions.append("zip = %(zip)s")
            query_values["zip"] = zip
        if minimum_weight is not NO_VALUE:
            query_conditions.append("minimum_weight = %(minimum_weight)s")
            query_values["minimum_weight"] = minimum_weight
        if preconditioning_program is not NO_VALUE:
            query_conditions.append("preconditioning_program = %(preconditioning_program)s")
            query_values["preconditioning_program"] = preconditioning_program
        if multi_select_fields is not NO_VALUE:
            query_conditions.append("multi_select_fields = %(multi_select_fields)s")
            query_values["multi_select_fields"] = dumps(multi_select_fields) if multi_select_fields else None
        if target_date_description is not NO_VALUE:
            query_conditions.append("target_date_description = %(target_date_description)s")
            query_values["target_date_description"] = target_date_description
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")
        return self._db.row_count()
