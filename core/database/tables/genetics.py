from ..no_value import NoValue

NO_VALUE = NoValue()

class Genetics:

    def __init__(self, db):
        self._db = db

    def insert(self, breed=NO_VALUE):
        """
        Inserts a new row for sales group field values

        Params:
            field_id: Field ID for the value
            value: Option value for the field
        """
        self._db.execute(
            """
            INSERT INTO genetics(breed)
            VALUES(%(breed)s)
            """,
            {
                "breed": breed
            }
        )