from json import dumps, loads
from ..no_value import NoValue
from ...common_exceptions import ExportException

NO_VALUE = NoValue()

SALES_GROUP_FIELD_NAMES_TO_IDS = {
    "vaccination": 1,
    "genetics_verification": 2,
    "comingled_status": 3,
    "creep_feed": 4,
    "weaned": 5,
    "breed": 6,
    "pvp_program": 7,
    "preconditioning_program": 8,
    "frame": 9,
    "muscling": 10,
    "horn": 11,
    "delivery_location_type": 12,
    "castrated": 13,
    "feeding_program": 14,
    "implant": 15,
    "category": 16,
    "pregnancy_status": 17,
    "breed_program_certification_co": 18
}

SALES_GROUP_FIELD_IDS_TO_NAMES = {value: key for key, value in SALES_GROUP_FIELD_NAMES_TO_IDS.items()}

sales_group_fields_values_cols = ("id", "field_id", "value")

class SalesGroupFieldsValues:

    def __init__(self, db):
        self._db = db

    def insert(self, field_id=NO_VALUE, value=NO_VALUE):
        """
        Inserts a new row for sales group field values

        Params:
            field_id: Field ID for the value
            value: Option value for the field
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
            id: ID of the sales group field value
            field_id: Field ID for the value

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
        Updates the row based on the provided attributes

        Params:
            id: ID of the sales group field value
            field_id: Field ID for the 
            value: Option value for the field
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