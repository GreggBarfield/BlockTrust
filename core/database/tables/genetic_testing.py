from ..no_value import NoValue

NO_VALUE = NoValue()

class GeneticTesting:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, user_id=None, eid=None, sample_barcode=None, breed=None, sex=None,
               parentage_testing=None, sample_type=None):
        """
        Inserts a genetic testing record

        Params:
            account_id: Account ID  of the account uploading the record
            user_id: User ID of the user uploading the record
            eid: Animal ID
            sample_barcode: Sample barcode
            breed: Breed of the animal
            sex: Sex of the animal
            parentage_testing: Is parentage testing performed
            sample_type: Type of sample
        """
        self._db.execute(
            """
            INSERT INTO genetic_testing (account_id, user_id, eid, sample_barcode, breed, sex, parentage_testing,
            sample_type)
            VALUES (%(account_id)s, %(user_id)s, %(eid)s, %(sample_barcode)s, %(breed)s, %(sex)s,
            %(parentage_testing)s, %(sample_type)s)
            """, 
            {
                "account_id": account_id,
                "user_id": user_id,
                "eid": eid,
                "sample_barcode": sample_barcode,
                "breed": breed,
                "sex": sex,
                "parentage_testing": parentage_testing,
                "sample_type": sample_type
            })
        
    def get(self, id=NO_VALUE, account_id=NO_VALUE, user_id=NO_VALUE, eid=NO_VALUE, sample_barcode=NO_VALUE,
            breed=NO_VALUE, sex=NO_VALUE, parentage_testing=NO_VALUE, sample_type=NO_VALUE):
        """
        Gets geentic testing rows based on provided attributes

        Params:
            id: ID of the geentic testing record
            account_id: Account ID  of the account uploading the record
            user_id: User ID of the user uploading the record
            eid: Animal ID
            sample_barcode: Sample barcode
            breed: Breed of the animal
            sex: Sex of the animal
            parentage_testing: Is parentage testing performed
            sample_type: Type of sample
        
        Returns:
            A list of genetic testing rows or an empty list
        """
        base_query = "SELECT * FROM genetic_testing"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if eid is not NO_VALUE:
            query_conditions.append(" eid = %(eid)s")
            query_values["eid"] = eid
        if sample_barcode is not NO_VALUE:
            query_conditions.append(" sample_barcode = %(sample_barcode)s")
            query_values["sample_barcode"] = sample_barcode
        if breed is not NO_VALUE:
            query_conditions.append(" breed = %(breed)s")
            query_values["breed"] = breed
        if sex is not NO_VALUE:
            query_conditions.append(" sex = %(sex)s")
            query_values["sex"] = sex
        if parentage_testing is not NO_VALUE:
            query_conditions.append(" parentage_testing = %(parentage_testing)s")
            query_values["parentage_testing"] = parentage_testing
        if sample_type is not NO_VALUE:
            query_conditions.append(" sample_type = %(sample_type)s")
            query_values["sample_type"] = sample_type
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        genetic_testing_rows = self._db.execute_d(query, query_values)
        if len(genetic_testing_rows) > 0:
            return genetic_testing_rows
        else:
            return []
    
    def update(self, id, account_id=NO_VALUE, user_id=NO_VALUE, eid=NO_VALUE, sample_barcode=NO_VALUE, breed=NO_VALUE,
               sex=NO_VALUE, parentage_testing=NO_VALUE, sample_type=NO_VALUE):
        """
        Updates the genetic testing row based on ID provided

        Params:
            id: ID of the geentic testing record
            account_id: Account ID  of the account uploading the record
            user_id: User ID of the user uploading the record
            eid: Animal ID
            sample_barcode: Sample barcode
            breed: Breed of the animal
            sex: Sex of the animal
            parentage_testing: Is parentage testing performed
            sample_type: Type of sample
        """
        base_query = "UPDATE genetic_testing"

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if eid is not NO_VALUE:
            query_conditions.append(" eid = %(eid)s")
            query_values["eid"] = eid
        if sample_barcode is not NO_VALUE:
            query_conditions.append(" sample_barcode = %(sample_barcode)s")
            query_values["sample_barcode"] = sample_barcode
        if breed is not NO_VALUE:
            query_conditions.append(" breed = %(breed)s")
            query_values["breed"] = breed
        if sex is not NO_VALUE:
            query_conditions.append(" sex = %(sex)s")
            query_values["sex"] = sex
        if parentage_testing is not NO_VALUE:
            query_conditions.append(" parentage_testing = %(parentage_testing)s")
            query_values["parentage_testing"] = parentage_testing
        if sample_type is not NO_VALUE:
            query_conditions.append(" sample_type = %(sample_type)s")
            query_values["sample_type"] = sample_type

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Genetic Testing")