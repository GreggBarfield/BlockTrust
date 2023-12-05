from json import dumps, loads
from ..no_value import NoValue
from ...common_exceptions import ExportException

NO_VALUE = NoValue()

SALES_GROUP_FORM_TYPES_NAMES_TO_IDS = {
    "External": 0,
    "Internal": 1
}

SALES_GROUP_FORM_TYPES_IDS_TO_NAMES = {
    value: key for key, value in SALES_GROUP_FORM_TYPES_NAMES_TO_IDS.items()
}

FIELD_NAME_TO_COLUMN_NAME_MAPPING = {
    "Vaccinations": "vaccinations"
}

sales_group_fields_values_cols = ("id", "vaccinations", "sales_group_form_type")

class SalesGroupFieldsValues:

    def __init__(self, db):
        self._db = db

    def insert(vaccinations=NO_VALUE, sales_group_form_type=NO_VALUE):
        """
        Inserts a new row for sales group field values
        """
        self._db.execute(
            """
            INSERT INTO sales_group_fields_values(vaccinations, sales_group_form_type),
            VALUES(%(vaccinations)s, %(sales_group_form_type)s)
            """, 
            {
                "vaccinations": dumps(vaccinations) if vaccinations else None,
                "sales_group_form_type": sales_group_form_type
            }
        )

    def get(self, id=NO_VALUE, sales_group_form_type=NO_VALUE):
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
        if sales_group_form_type is not NO_VALUE:
            query_conditions.append("sales_group_form_type = %(sales_group_form_type)s")
            query_values["sales_group_form_type"] = sales_group_form_type

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition + " ORDER BY ID DESC"
        rows = self._db.execute_d(query, query_values)
        if len(rows) > 0:
            sales_group_fields_values = rows[0]
            if sales_group_fields_values["vaccinations"] is not None:
                sales_group_fields_values["vaccinations"] = loads(sales_group_fields_values["vaccinations"])
            else:
                sales_group_fields_values["vaccinations"] = None
            return sales_group_fields_values
        else:
            return []
        
    def update(self, id, **updated_field_names_and_values):
        """
        Updates the JSON value for a given column wiht field values

        Params:
            updated_field_names_and_values: A dictionary containing the field names to be updated and updated values
        """
        for field_name in updated_field_names_and_values.keys():
            if field_name not in sales_group_fields_values_cols:
                raise Exception("Specified column does not exist: " + field_name)
        
        base_query = "UPDATE sales_group_fields_values"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        for field_name, updated_field_value in updated_field_names_and_values.items():
            query_conditions.append(field_name + " = %(" + field_name + ")s")
            query_values[field_name] = dumps(updated_field_value) if updated_field_value else None

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")

    def insert_new_value_for_specified_field(self, field_name, new_field_value, sales_group_form_type):
        """
        Inserts a new value to the list of values of the specified sales group field

        Params:
            field_name: Name of the sales group field (Column name)
            new_field_value: New value for the sales group field that needs to be inserted
            sales_group_form_type: Type of form values that need to be updated (Internal or External)

        Raise:
            Exception if the specified value is already present or invalid
        """
        updated_field_values = {}
        sales_group_fields_values = self.get(sales_group_form_type=sales_group_form_type)
        if field_name not in sales_group_fields_values_cols:
            raise Exception("Specified Column does not exist: " + field_name)
        existing_field_values = sales_group_fields_values[field_name]["values"]
        if new_field_value in existing_field_values:
            raise ExportException("Entered Option already exists in the available options.")
        existing_field_values.append(new_field_value)
        updated_field_values["values"] = existing_field_values
        updated_field_name_and_value = {field_name: updated_field_values}
        self.update(sales_group_fields_values["id"], **updated_field_name_and_value)

        
            