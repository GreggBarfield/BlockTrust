from ..no_value import NoValue
import time

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
                              terminal_reimplant_weight=None, terminal_reimplant_date=None, api_insert_id=None,
                              seller_id=None, vaccination_date=None, vaccination_summary=None, herd_sire=None,
                              ranch_source_county=None, ranch_size=None, home_raised=None, family_farm_or_ranch=None,
                              harvest_date=None, program_certification=None, marbling_score=None,
                              marbling_score_code=None, ribeye_area=None, fat_thickness=None,
                              calculated_live_weight=None, total_gain=None, days_on_test=None, average_daily_gain=None,
                              packer_api_insert_id=None, feeder_api_insert_id=None, is_paid=None,
                              sire_epd_wean_weight=None, sire_epd_yearling_weight=None, sire_epd_dry_matter_intake=None,
                              sire_epd_carcass_weight=None, sire_epd_rib_fat=None, sire_epd_ribeye_area=None,
                              sire_epd_certified_hereford_beef_index=None, sire_epd_marbling=None,
                              over_30=None, hard_bone=None, dark_cutter=None, average_lot_live=None):
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
            terminal_reimplant_weight, terminal_reimplant_date, api_insert_id, seller_id, vaccination_date,
            vaccination_summary, herd_sire, ranch_source_county, ranch_size, home_raised, family_farm_or_ranch,
            harvest_date, program_certification, marbling_score, marbling_score_code, ribeye_area, fat_thickness,
            calculated_live_weight, total_gain, days_on_test, average_daily_gain, packer_api_insert_id,
            feeder_api_insert_id, is_paid, sire_epd_wean_weight, sire_epd_yearling_weight, sire_epd_dry_matter_intake,
            sire_epd_carcass_weight, sire_epd_rib_fat, sire_epd_ribeye_area, sire_epd_certified_hereford_beef_index,
            sire_epd_marbling, over_30, hard_bone, dark_cutter, average_lot_live
        )

    def insert_animal(self, eid, visual_id=None, breed=None, calf_registration_number=None,
                      sire_registration_number=None, dam_registration_number=None,
                      birth_weight=None, implants=None, sex=None, description=None, lot_number=None,
                      pen_number=None, feeder_account_number=None, feeder_weight=None, terminal_reimplant_weight=None,
                      terminal_reimplant_date=None, api_insert_id=None, seller_id=None, vaccination_date=None,
                      vaccination_summary=None, herd_sire=None, ranch_source_county=None, ranch_size=None,
                      home_raised=None, family_farm_or_ranch=None, harvest_date=None, program_certification=None,
                      marbling_score=None, marbling_score_code=None, ribeye_area=None, fat_thickness=None,
                      calculated_live_weight=None, total_gain=None, days_on_test=None, average_daily_gain=None,
                      packer_api_insert_id=None, feeder_api_insert_id=None, is_paid=None, sire_epd_wean_weight=None,
                      sire_epd_yearling_weight=None, sire_epd_dry_matter_intake=None, sire_epd_carcass_weight=None,
                      sire_epd_rib_fat=None, sire_epd_ribeye_area=None, sire_epd_certified_hereford_beef_index=None,
                      sire_epd_marbling=None, over_30=None, hard_bone=None, dark_cutter=None, average_lot_live=None):
        """
        Inserts a new animal record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO animals(
                    eid, visual_id, breed, calf_registration_number, sire_registration_number,
                    dam_registration_number, birth_weight, implants, sex, description,
                    lot_number, pen_number, feeder_account_number, feeder_weight,
                    terminal_reimplant_weight, terminal_reimplant_date, api_insert_id, seller_id, vaccination_date,
                    vaccination_summary, herd_sire, ranch_source_county, ranch_size, home_raised, family_farm_or_ranch,
                    harvest_date, program_certification, marbling_score, marbling_score_code, ribeye_area,
                    fat_thickness, calculated_live_weight, total_gain, days_on_test, average_daily_gain,
                    packer_api_insert_id, feeder_api_insert_id, is_paid, sire_epd_wean_weight, sire_epd_yearling_weight,
                    sire_epd_dry_matter_intake, sire_epd_carcass_weight, sire_epd_rib_fat, sire_epd_ribeye_area,
                    sire_epd_certified_hereford_beef_index, sire_epd_marbling, over_30, hard_bone, dark_cutter, average_lot_live
                )
                VALUES (
                    %(eid)s, %(visual_id)s, %(breed)s, %(calf_registration_number)s, %(sire_registration_number)s,
                    %(dam_registration_number)s, %(birth_weight)s, %(implants)s, %(sex)s, %(description)s,
                    %(lot_number)s, %(pen_number)s, %(feeder_account_number)s, %(feeder_weight)s,
                    %(terminal_reimplant_weight)s, %(terminal_reimplant_date)s, %(api_insert_id)s, %(seller_id)s,
                    %(vaccination_date)s, %(vaccination_summary)s, %(herd_sire)s, %(ranch_source_county)s,
                    %(ranch_size)s, %(home_raised)s, %(family_farm_or_ranch)s, %(harvest_date)s,
                    %(program_certification)s, %(marbling_score)s, %(marbling_score_code)s, %(ribeye_area)s,
                    %(fat_thickness)s, %(calculated_live_weight)s, %(total_gain)s, %(days_on_test)s,
                    %(average_daily_gain)s, %(packer_api_insert_id)s, %(feeder_api_insert_id)s, %(is_paid)s,
                    %(sire_epd_wean_weight)s, %(sire_epd_yearling_weight)s, %(sire_epd_dry_matter_intake)s,
                    %(sire_epd_carcass_weight)s, %(sire_epd_rib_fat)s, %(sire_epd_ribeye_area)s,
                    %(sire_epd_certified_hereford_beef_index)s, %(sire_epd_marbling)s, %(over_30)s, %(hard_bone)s, 
                    %(dark_cutter)s, %(average_lot_live)s
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
                "terminal_reimplant_date": terminal_reimplant_date,
                "api_insert_id": api_insert_id,
                "seller_id": seller_id,
                "vaccination_date": vaccination_date,
                "vaccination_summary": vaccination_summary,
                "herd_sire": herd_sire,
                "ranch_source_county": ranch_source_county,
                "ranch_size": ranch_size,
                "home_raised": home_raised,
                "family_farm_or_ranch": family_farm_or_ranch, 
                "harvest_date": harvest_date,
                "program_certification": program_certification,
                "marbling_score": marbling_score,
                "marbling_score_code": marbling_score_code,
                "ribeye_area": ribeye_area,
                "fat_thickness": fat_thickness,
                "calculated_live_weight": calculated_live_weight,
                "total_gain": total_gain,
                "days_on_test": days_on_test,
                "average_daily_gain": average_daily_gain,
                "packer_api_insert_id": packer_api_insert_id,
                "feeder_api_insert_id": feeder_api_insert_id,
                "is_paid": is_paid,
                "sire_epd_wean_weight": sire_epd_wean_weight,
                "sire_epd_yearling_weight": sire_epd_yearling_weight,
                "sire_epd_dry_matter_intake": sire_epd_dry_matter_intake,
                "sire_epd_carcass_weight": sire_epd_carcass_weight,
                "sire_epd_rib_fat": sire_epd_rib_fat,
                "sire_epd_ribeye_area": sire_epd_ribeye_area,
                "sire_epd_certified_hereford_beef_index": sire_epd_certified_hereford_beef_index,
                "sire_epd_marbling": sire_epd_marbling,
                "over_30": over_30,
                "hard_bone": hard_bone,
                "dark_cutter": dark_cutter,
                "average_lot_live": average_lot_live
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
                      terminal_reimplant_weight=NO_VALUE, terminal_reimplant_date=NO_VALUE, api_insert_id=NO_VALUE,
                      seller_id=NO_VALUE, vaccination_date=NO_VALUE, vaccination_summary=NO_VALUE, herd_sire=NO_VALUE,
                      ranch_source_county=NO_VALUE, ranch_size=NO_VALUE, home_raised=NO_VALUE,
                      family_farm_or_ranch=NO_VALUE, harvest_date=NO_VALUE, program_certification=NO_VALUE,
                      marbling_score=NO_VALUE, marbling_score_code=NO_VALUE, ribeye_area=NO_VALUE,
                      fat_thickness=NO_VALUE, calculated_live_weight=NO_VALUE, total_gain=NO_VALUE,
                      days_on_test=NO_VALUE, average_daily_gain=NO_VALUE, packer_api_insert_id=NO_VALUE,
                      feeder_api_insert_id=NO_VALUE, is_paid=NO_VALUE, payment_id=NO_VALUE,
                      sire_epd_wean_weight=NO_VALUE, sire_epd_yearling_weight=NO_VALUE,
                      sire_epd_dry_matter_intake=NO_VALUE, sire_epd_carcass_weight=NO_VALUE, sire_epd_rib_fat=NO_VALUE,
                      sire_epd_ribeye_area=NO_VALUE, sire_epd_certified_hereford_beef_index=NO_VALUE,
                      sire_epd_marbling=NO_VALUE, over_30=NO_VALUE, hard_bone=NO_VALUE, dark_cutter=NO_VALUE,
                      average_lot_live=NO_VALUE):
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
        if api_insert_id is not NO_VALUE:
            query_conditions.append("api_insert_id = %(api_insert_id)s")
            query_values["api_insert_id"] = api_insert_id
        if seller_id is not NO_VALUE:
            query_conditions.append("seller_id = %(seller_id)s")
            query_values["seller_id"] = seller_id
        if vaccination_date is not NO_VALUE:
            query_conditions.append("vaccination_date = %(vaccination_date)s")
            query_values["vaccination_date"] = vaccination_date
        if vaccination_summary is not NO_VALUE:
            query_conditions.append("vaccination_summary = %(vaccination_summary)s")
            query_values["vaccination_summary"] = vaccination_summary
        if herd_sire is not NO_VALUE:
            query_conditions.append("herd_sire = %(herd_sire)s")
            query_values["herd_sire"] = herd_sire
        if ranch_source_county is not NO_VALUE:
            query_conditions.append("ranch_source_county = %(ranch_source_county)s")
            query_values["ranch_source_county"] = ranch_source_county
        if ranch_size is not NO_VALUE:
            query_conditions.append("ranch_size = %(ranch_size)s")
            query_values["ranch_size"] = ranch_size
        if home_raised is not NO_VALUE:
            query_conditions.append("home_raised = %(home_raised)s")
            query_values["home_raised"] = home_raised
        if family_farm_or_ranch is not NO_VALUE:
            query_conditions.append("family_farm_or_ranch = %(family_farm_or_ranch)s")
            query_values["family_farm_or_ranch"] = family_farm_or_ranch
        if harvest_date is not NO_VALUE:
            query_conditions.append("harvest_date = %(harvest_date)s")
            query_values["harvest_date"] = harvest_date
        if program_certification is not NO_VALUE:
            query_conditions.append("program_certification = %(program_certification)s")
            query_values["program_certification"] = program_certification
        if marbling_score is not NO_VALUE:
            query_conditions.append("marbling_score = %(marbling_score)s")
            query_values["marbling_score"] = marbling_score
        if marbling_score_code is not NO_VALUE:
            query_conditions.append("marbling_score_code = %(marbling_score_code)s")
            query_values["marbling_score_code"] = marbling_score_code
        if ribeye_area is not NO_VALUE:
            query_conditions.append("ribeye_area = %(ribeye_area)s")
            query_values["ribeye_area"] = ribeye_area
        if fat_thickness is not NO_VALUE:
            query_conditions.append("fat_thickness = %(fat_thickness)s")
            query_values["fat_thickness"] = fat_thickness
        if calculated_live_weight is not NO_VALUE:
            query_conditions.append("calculated_live_weight = %(calculated_live_weight)s")
            query_values["calculated_live_weight"] = calculated_live_weight
        if total_gain is not NO_VALUE:
            query_conditions.append("total_gain = %(total_gain)s")
            query_values["total_gain"] = total_gain
        if days_on_test is not NO_VALUE:
            query_conditions.append("days_on_test = %(days_on_test)s")
            query_values["days_on_test"] = days_on_test
        if average_daily_gain is not NO_VALUE:
            query_conditions.append("average_daily_gain = %(average_daily_gain)s")
            query_values["average_daily_gain"] = average_daily_gain
        if packer_api_insert_id is not NO_VALUE:
            query_conditions.append("packer_api_insert_id = %(packer_api_insert_id)s")
            query_values["packer_api_insert_id"] = packer_api_insert_id
        if feeder_api_insert_id is not NO_VALUE:
            query_conditions.append("feeder_api_insert_id = %(feeder_api_insert_id)s")
            query_values["feeder_api_insert_id"] = feeder_api_insert_id
        if is_paid is not NO_VALUE:
            query_conditions.append("is_paid = %(is_paid)s")
            query_values["is_paid"] = is_paid
        if payment_id is not NO_VALUE:
            query_conditions.append("payment_id = %(payment_id)s")
            query_values["payment_id"] = payment_id
        if sire_epd_wean_weight is not NO_VALUE:
            query_conditions.append("sire_epd_wean_weight = %(sire_epd_wean_weight)s")
            query_values["sire_epd_wean_weight"] = sire_epd_wean_weight
        if sire_epd_yearling_weight is not NO_VALUE:
            query_conditions.append("sire_epd_yearling_weight = %(sire_epd_yearling_weight)s")
            query_values["sire_epd_yearling_weight"] = sire_epd_yearling_weight
        if sire_epd_dry_matter_intake is not NO_VALUE:
            query_conditions.append("sire_epd_dry_matter_intake = %(sire_epd_dry_matter_intake)s")
            query_values["sire_epd_dry_matter_intake"] = sire_epd_dry_matter_intake
        if sire_epd_carcass_weight is not NO_VALUE:
            query_conditions.append("sire_epd_carcass_weight = %(sire_epd_carcass_weight)s")
            query_values["sire_epd_carcass_weight"] = sire_epd_carcass_weight
        if sire_epd_rib_fat is not NO_VALUE:
            query_conditions.append("sire_epd_rib_fat = %(sire_epd_rib_fat)s")
            query_values["sire_epd_rib_fat"] = sire_epd_rib_fat
        if sire_epd_ribeye_area is not NO_VALUE:
            query_conditions.append("sire_epd_ribeye_area = %(sire_epd_ribeye_area)s")
            query_values["sire_epd_ribeye_area"] = sire_epd_ribeye_area
        if sire_epd_certified_hereford_beef_index is not NO_VALUE:
            query_conditions.append("sire_epd_certified_hereford_beef_index = %(sire_epd_certified_hereford_beef_index)s")
            query_values["sire_epd_certified_hereford_beef_index"] = sire_epd_certified_hereford_beef_index
        if sire_epd_marbling is not NO_VALUE:
            query_conditions.append("sire_epd_marbling = %(sire_epd_marbling)s")
            query_values["sire_epd_marbling"] = sire_epd_marbling
        if over_30 is not NO_VALUE:
            query_conditions.append("over_30 = %(over_30)s")
            query_values["over_30"] = over_30
        if hard_bone is not NO_VALUE:
            query_conditions.append("hard_bone = %(hard_bone)s")
            query_values["hard_bone"] = hard_bone
        if dark_cutter is not NO_VALUE:
            query_conditions.append("dark_cutter = %(dark_cutter)s")
            query_values["dark_cutter"] = dark_cutter
        if average_lot_live is not NO_VALUE:
            query_conditions.append("average_lot_live = %(average_lot_live)s")
            query_values["average_lot_live"] = average_lot_live

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE eid=%(eid)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values set to update Animal")


    def get_animals_by_packer_insert_ids(self, packer_insert_ids=NO_VALUE):
            """
            Get animals by the packer insert ID values specified.

            Params:
                last_updated_start_time: The start timestamp from where all updated records need to be fetched
                packer_insert_ids: A lisy of IDs from api_inserts table representing the Packer Inserts

            Returns:
                A list of animal row(s) if found else []
            """
            query_values = {}
            base_query = "SELECT * FROM animals WHERE packer_api_insert_id in "
            packer_insert_ids_condition = "(" + ",".join(str(packer_insert_id) for packer_insert_id in packer_insert_ids) + ")"

            query = base_query + packer_insert_ids_condition

            animal_rows = self._db.execute_d(query, query_values)
            if len(animal_rows) > 0:
                return animal_rows
            else:
                return []