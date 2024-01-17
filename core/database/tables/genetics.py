from ..no_value import NoValue

NO_VALUE = NoValue()

class Genetics:

    def __init__(self, db):
        self._db = db

    def insert(self, owner_account_id=NO_VALUE, uid=NO_VALUE, breed=NO_VALUE, ranch_name=NO_VALUE, address=NO_VALUE,
               city=NO_VALUE, state=NO_VALUE, zip_code=NO_VALUE):
        """
        Inserts a new row for sales group field values

        Params:
            field_id: Field ID for the value
            value: Option value for the field
        """
        self._db.execute(
            """
            INSERT INTO genetics(owner_account_id, uid, breed, ranch_name, address, city, state, zip_code)
            VALUES(%(breed)s)
            """,
            {
                "owner_account_id": owner_account_id,
                "uid": uid,
                "breed": breed,
                "ranch_name": ranch_name,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
        )

    def get(self, id=NO_VALUE, owner_account_id=NO_VALUE, uid=NO_VALUE, breed=NO_VALUE, ranch_name=NO_VALUE,
            address=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip_code=NO_VALUE):
        """
        Get genetics data based on parameters provided

        Params:
            id: ID of the genetics row
            owner_account_id: Owner account ID
            uid: UID of genetics kit
            breed: Heifer Breed
            ranch_name: Ranch name
            address: Genetics account address 
            city: Genetics account city 
            state: Genetics account state 
            zip_code: Genetics account zip code 
        """
        base_query = "SELECT * FROM genetics"

        query_conditions = []
        query_values = {}
        
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if owner_account_id is not NO_VALUE:
            query_conditions.append("owner_account_id = %(owner_account_id)s")
            query_values["owner_account_id"] = owner_account_id
        if uid is not NO_VALUE:
            query_conditions.append("uid = %(uid)s")
            query_values["uid"] = uid
        if breed is not NO_VALUE:
            query_conditions.append("breed = %(breed)s")
            query_values["breed"] = breed
        if ranch_name is not NO_VALUE:
            query_conditions.append("ranch_name = %(ranch_name)s")
            query_values["ranch_name"] = ranch_name
        if address is not NO_VALUE:
            query_conditions.append("address = %(address)s")
            query_values["address"] = address
        if owner_account_id is not NO_VALUE:
            query_conditions.append("city = %(city)s")
            query_values["city"] = city
        if owner_account_id is not NO_VALUE:
            query_conditions.append("state = %(state)s")
            query_values["state"] = state
        if owner_account_id is not NO_VALUE:
            query_conditions.append("zip_code = %(zip_code)s")
            query_values["zip_code"] = zip_code

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        rows = self._db.execute_d(query, query_values)
        return rows

    def update(self, id, owner_account_id=NO_VALUE, uid=NO_VALUE, breed=NO_VALUE, ranch_name=NO_VALUE,
            address=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip_code=NO_VALUE):
        """
        Get genetics data based on parameters provided

        Params:
            id: ID of the genetics row
            owner_account_id: Owner account ID
            uid: UID of genetics kit
            breed: Heifer Breed
            ranch_name: Ranch name
            address: Genetics account address 
            city: Genetics account city 
            state: Genetics account state 
            zip_code: Genetics account zip code 
        """
        base_query = "UPDATE genetics"

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if owner_account_id is not NO_VALUE:
            query_conditions.append("owner_account_id = %(owner_account_id)s")
            query_values["owner_account_id"] = owner_account_id
        if uid is not NO_VALUE:
            query_conditions.append("uid = %(uid)s")
            query_values["uid"] = uid
        if breed is not NO_VALUE:
            query_conditions.append("breed = %(breed)s")
            query_values["breed"] = breed
        if ranch_name is not NO_VALUE:
            query_conditions.append("ranch_name = %(ranch_name)s")
            query_values["ranch_name"] = ranch_name
        if address is not NO_VALUE:
            query_conditions.append("address = %(address)s")
            query_values["address"] = address
        if owner_account_id is not NO_VALUE:
            query_conditions.append("city = %(city)s")
            query_values["city"] = city
        if owner_account_id is not NO_VALUE:
            query_conditions.append("state = %(state)s")
            query_values["state"] = state
        if owner_account_id is not NO_VALUE:
            query_conditions.append("zip_code = %(zip_code)s")
            query_values["zip_code"] = zip_code

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")