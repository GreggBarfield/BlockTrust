from json import dumps, loads
from ..no_value import NoValue
from ...common_exceptions import ExportException

NO_VALUE = NoValue()

FIELD_NAMES_TO_IDS = {
    "vaccination": 1
}

FIELD_IDS_TO_NAMES = {value: key for key, value in FIELD_NAMES_TO_IDS.items()}

sales_group_fields_values_cols = ("id", "field_id", "value")

class SalesGroupFieldsValues:

    def __init__(self, db):
        self._db = db

    def insert(self, field_id=NO_VALUE, value=NO_VALUE):
        """
        Inserts a new row for sales group field values
        """
        self._db.execute(
            """
            INSERT INTO sales_group_fields_values(field_id, value)
            VALUES(%(field_id)s, %(value)s)
            """, 
            {
                "field_id": field_id,
                "value": value
            }
        )

    def get(self, id=NO_VALUE, field_id=NO_VALUE):
        """
        Gets the sales group fields values based on provided parameters

        Params:
            sales_group_form_type: Type of form fields values are requested for

        Returns:
            A list of sales group fields values
        """
        base_query = "SELECT * FROM sales_group_fields_values"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if field_id is not NO_VALUE:
            query_conditions.append("field_id = %(field_id)s")
            query_values["field_id"] = field_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        rows = self._db.execute_d(query, query_values)
        return rows
        
    def update(self, id, field_id=NO_VALUE, value=NO_VALUE):
        """
        Updates the JSON value for a given column wiht field values

        Params:
            updated_field_names_and_values: A dictionary containing the field names to be updated and updated values
        """
        base_query = "UPDATE sales_group_fields_values"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if field_id is not NO_VALUE:
            query_conditions.append("field_id = %(field_id)s")
            query_values["field_id"] = field_id        
        if value is not NO_VALUE:
            query_conditions.append("value = %(value)s")
            query_values["value"] = value

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")

        
            