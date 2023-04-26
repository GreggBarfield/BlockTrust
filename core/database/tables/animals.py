from ..no_value import NoValue

NO_VALUE = NoValue()


class AnimalsException(Exception):
    """Animal exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for AnimalException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Animals:

    def __init__(self, db):
        self._db = db

    def create_or_fail_animal(self, eid, visual_id=None, breed=None, calf_registration_number=None,
                              sire_registration_number=None, dam_registration_number=None,
                              birth_weight=None, implants=None, sex=None, description=None,
                              lot_number=None, pen_number=None, feeder_account_number=None, feeder_weight=None,
                              terminal_reimplant_weight=None, terminal_reimplant_date=None):
        """
        Validates and inserts a new animal record

        Raises:
            AnimalException

        Returns:
            id of row inserted
        """

        if len(self.get_animals(eid=eid)) > 0:
            raise AnimalsException(f"Animal with {eid} already exists")

        return self.insert_animal(
            eid, visual_id, breed, calf_registration_number, sire_registration_number, dam_registration_number,
            birth_weight, implants, sex, description, lot_number, pen_number, feeder_account_number, feeder_weight,
            terminal_reimplant_weight, terminal_reimplant_date
        )

    def insert_animal(self, eid, visual_id=None, breed=None, calf_registration_number=None,
                      sire_registration_number=None, dam_registration_number=None,
                      birth_weight=None, implants=None, sex=None, description=None, lot_number=None,
                      pen_number=None, feeder_account_number=None, feeder_weight=None, terminal_reimplant_weight=None,
                      terminal_reimplant_date=None):
        """
        Inserts a new animal record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO animals(eid, visual_id, breed, calf_registration_number, sire_registration_number,
                    dam_registration_number, birth_weight, implants, sex, description, 
                    lot_number, pen_number, feeder_account_number, feeder_weight,
                    terminal_reimplant_weight, terminal_reimplant_date
                )
                VALUES (%(eid)s, %(visual_id)s, %(breed)s, %(calf_registration_number)s, %(sire_registration_number)s,
                    %(dam_registration_number)s, %(birth_weight)s, %(implants)s, %(sex)s, %(description)s,
                    %(lot_number)s, %(pen_number)s, %(feeder_account_number)s, %(feeder_weight)s,
                    %(terminal_reimplant_weight)s, %(terminal_reimplant_date)s
                )
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
                "sex": sex,
                "description": description,
                "lot_number": lot_number,
                "pen_number": pen_number,
                "feeder_account_number": feeder_account_number,
                "feeder_weight": feeder_weight,
                "terminal_reimplant_weight": terminal_reimplant_weight,
                "terminal_reimplant_date": terminal_reimplant_date
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

        animal_rows = self._db.execute_d(query, query_values)
        if len(animal_rows) > 0:
            return animal_rows
        else:
            return []

    def update_animal(self, eid, visual_id=NO_VALUE, breed=NO_VALUE, calf_registration_number=NO_VALUE,
                      sire_registration_number=NO_VALUE, dam_registration_number=NO_VALUE,
                      birth_weight=NO_VALUE, implants=NO_VALUE, sex=NO_VALUE, description=NO_VALUE,
                      lot_number=NO_VALUE, pen_number=NO_VALUE, feeder_account_number=NO_VALUE, feeder_weight=NO_VALUE, 
                      terminal_reimplant_weight=NO_VALUE, terminal_reimplant_date=NO_VALUE):
        """
        Updates an animal.
        """
        base_query = "UPDATE animals"

        query_conditions = []
        query_values = {}
        query_values["eid"] = eid

        if visual_id is not NO_VALUE:
            query_conditions.append("visual_id = %(visual_id)s")
            query_values["visual_id"] = visual_id
        if breed is not NO_VALUE:
            query_conditions.append("breed = %(breed)s")
            query_values["breed"] = breed
        if calf_registration_number is not NO_VALUE:
            query_conditions.append("calf_registration_number = %(calf_registration_number)s")
            query_values["calf_registration_number"] = calf_registration_number
        if sire_registration_number is not NO_VALUE:
            query_conditions.append("sire_registration_number = %(sire_registration_number)s")
            query_values["sire_registration_number"] = sire_registration_number
        if dam_registration_number is not NO_VALUE:
            query_conditions.append("dam_registration_number = %(dam_registration_number)s")
            query_values["dam_registration_number"] = dam_registration_number
        if birth_weight is not NO_VALUE:
            query_conditions.append("birth_weight = %(birth_weight)s")
            query_values["birth_weight"] = birth_weight
        if implants is not NO_VALUE:
            query_conditions.append("implants = %(implants)s")
            query_values["implants"] = implants
        if sex is not NO_VALUE:
            query_conditions.append("sex = %(sex)s")
            query_values["sex"] = sex
        if description is not NO_VALUE:
            query_conditions.append("description = %(description)s")
            query_values["description"] = description
        if lot_number is not NO_VALUE:
            query_conditions.append("lot_number = %(lot_number)s")
            query_values["lot_number"] = lot_number
        if pen_number is not NO_VALUE:
            query_conditions.append("pen_number = %(pen_number)s")
            query_values["pen_number"] = pen_number
        if feeder_account_number is not NO_VALUE:
            query_conditions.append("feeder_account_number = %(feeder_account_number)s")
            query_values["feeder_account_number"] = feeder_account_number
        if feeder_weight is not NO_VALUE:
            query_conditions.append("feeder_weight = %(feeder_weight)s")
            query_values["feeder_weight"] = feeder_weight
        if terminal_reimplant_weight is not NO_VALUE:
            query_conditions.append("terminal_reimplant_weight = %(terminal_reimplant_weight)s")
            query_values["terminal_reimplant_weight"] = terminal_reimplant_weight
        if terminal_reimplant_date is not NO_VALUE:
            query_conditions.append("terminal_reimplant_date = %(terminal_reimplant_date)s")
            query_values["terminal_reimplant_date"] = terminal_reimplant_date

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE eid=%(eid)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Account")