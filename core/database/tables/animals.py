from ..no_value import NoValue

NO_VALUE = NoValue()


class Animals:

    def __init__(self, db):
        self._db = db

    def create_animal(self, eid, visual_id=None, breed=None, calf_registration_number=None,
                      sire_registration_number=None, dam_registration_number=None,
                      birth_weight=None, implants=None, sex=None):
        """
        Validates and inserts a new animal record

        Raises:
            Exception
        
        Returns:
            id of row inserted
        """

        if len(self.get_animals(eid=eid)) > 0:
            raise Exception(f"Animal with {eid} already exists")

        return self.insert_animal(
            eid, visual_id, breed, calf_registration_number,
            sire_registration_number, dam_registration_number,
            birth_weight, implants, sex
        )

    def insert_animal(self, eid, visual_id=None, breed=None, calf_registration_number=None,
                      sire_registration_number=None, dam_registration_number=None,
                      birth_weight=None, implants=None, sex=None):
        """
        Inserts a new animal record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO animals(eid, visual_id, breed, calf_registration_number, sire_registration_number,
                dam_registration_number, birth_weight, implants, sex)
                VALUES (%(eid)s, %(visual_id)s, %(breed)s, %(calf_registration_number)s, %(sire_registration_number)s,
                %(dam_registration_number)s, %(birth_weight)s, %(implants)s, %(sex)s)
            """,
            {
                "eid": eid,
                "visual_id": visual_id,
                "breed": breed,
                "calf_registration_number": calf_registration_number,
                "sire_registration_number": sire_registration_number,
                "dam_registration_number": dam_registration_number,
                "birth_weight": birth_weight,
                "implants": implants,
                "sex": sex
            }
        )
        return self._db.last_row_id()

    def get_animals(self, id=NO_VALUE, eid=NO_VALUE):
        """
        Get a animal by the values specified.

        Returns:
            A list of animal row(s) if found else []
        """
        base_query = "SELECT * FROM animals"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id

        if eid is not NO_VALUE:
            query_conditions.append("eid = %(eid)s")
            query_values["eid"] = eid

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        tip_rows = self._db.execute_d(query, query_values)
        if len(tip_rows) > 0:
            return tip_rows
        else:
            return []
