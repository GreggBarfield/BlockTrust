
from core.database.combinations import perform_feeder_packer_data_received_actions
from core.database.tables.animals import Animals, AnimalsException
from api.translation_worker.all_to_unix import all_to_unix
from core.match_types import MATCH_TYPES_NAME_TO_ID
from core.utilities.zip_codes import get_lat_lon


def insert_sighting_if_not_exists(db, eid, account_link_id, api_insert_id, zipcode, sighting_date,
                                  partner_account, visual_id=None, grouping_id=None, timezone=None):
    f5 = zipcode[0:5] if len(zipcode) > 5 else zipcode
    for d in f5:
        if d not in "0123456789":
            raise Exception(f"Incorrect zipcode: {f5}")
    lat, lon = get_lat_lon(int(f5))
    matches = db.matches.get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"])
    if not matches:
        db.matches.types.insert_sighting(
            eid=eid,
            visual_id=visual_id,
            time=all_to_unix(sighting_date, timezone) if timezone else all_to_unix(sighting_date),
            lat=lat,
            lon=lon,
            partner_account=partner_account,
            account_link=account_link_id,
            grouping_id=grouping_id,
            api_insert=api_insert_id,
            zip=zipcode
        )
    else:
        raise Exception("Duplicate")


def process_sighting(db, eid, account_link_id, api_insert_id, zipcode, sighting_date,
                     partner_account, visual_id=None, grouping_id=None, timezone=None):
    f5 = zipcode[0:5] if len(zipcode) > 5 else zipcode
    for d in f5:
        if d not in "0123456789":
            raise Exception(f"Incorrect zipcode: {f5}")
    lat, lon = get_lat_lon(int(f5))
    matches = db.matches.get_matches(eid=eid, account_link=account_link_id,
                                     restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"])
    if matches:
        # update visual_id, time, zip code (lat and lon as well), partner_account, api_insert
        sighting_data = {}
        if visual_id:
            sighting_data["visual_id"] = visual_id
        if grouping_id:
            sighting_data["grouping_id"] = grouping_id
        previous_api_inserts = matches[0]["debug"].get("previous_api_inserts", []) if matches[0]["debug"] else []
        if matches[0]["api_insert"]:
            previous_api_inserts.append(matches[0]["api_insert"])

        db.matches.update_match(
            id=matches[0]["id"],
            time=all_to_unix(sighting_date, timezone) if timezone else all_to_unix(sighting_date),
            lat=lat,
            lon=lon,
            partner_account=partner_account,
            debug={"previous_api_inserts": previous_api_inserts},
            api_insert=api_insert_id,
            zip_code=zipcode,
            **sighting_data
        )
    else:
        db.matches.types.insert_sighting(
            eid=eid,
            visual_id=visual_id,
            time=all_to_unix(sighting_date, timezone) if timezone else all_to_unix(sighting_date),
            lat=lat,
            lon=lon,
            partner_account=partner_account,
            account_link=account_link_id,
            grouping_id=grouping_id,
            api_insert=api_insert_id,
            zip=zipcode
        )


def process_birth_date(db, input_data, eid, partner_account, account_link, api_insert=None, timezone=None):
    if "birth_date" in input_data:
        if birth_date := (
            all_to_unix(input_data["birth_date"], timezone) if timezone else all_to_unix(input_data["birth_date"])
        ):
            matches = db.matches.get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Born"])
            if matches:
                # update birth_date, partner_account, api_insert id
                previous_api_inserts = matches[0]["debug"].get("previous_api_inserts", []) if matches[0]["debug"] else []
                if matches[0]["api_insert"]:
                    previous_api_inserts.append(matches[0]["api_insert"])
                db.matches.update_match(
                    id=matches[0]["id"],
                    time=birth_date,
                    partner_account=partner_account,
                    api_insert=api_insert,
                    debug={"previous_api_inserts": previous_api_inserts}
                )
            else:
                db.matches.types.insert_born(
                    time=birth_date,
                    partner_account=partner_account,
                    account_link=account_link,
                    eid=eid,
                    api_insert=api_insert
                )


def process_weaning_data(db, input_data, eid, partner_account, account_link, api_insert=None, timezone=None):
    if "wean_date" in input_data:
        if wean_date := (
            all_to_unix(input_data["wean_date"], timezone) if timezone else all_to_unix(input_data["wean_date"])
        ):
            weaned_object = {}

            weaned_object_tags = [
                ("at", "weaningstr"),
                ("creep_feed", "creep_feed"),
                ("first_14_feed", "first14day"),
                ("first_14_method", "first14da1"),
                ("second_31_feed", "second31da"),
                ("second_31_method", "second31d1")
            ]

            for tag in weaned_object_tags:
                if tag[1] in input_data and input_data[tag[1]].strip() != "":
                    weaned_object[tag[0]] = input_data[tag[1]].strip()

            if "wean_weight" in input_data and input_data["wean_weight"].strip() != "" and int(input_data["wean_weight"]) > 0:
                weaned_object["wean_weight"] = int(input_data["wean_weight"])

            if weaned_object == {}:
                weaned_object = None
            matches = db.matches.get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Weaned"])
            if matches:
                # update weaned obj, weaned date, partner_account and api_insert
                previous_api_inserts = matches[0]["debug"].get("previous_api_inserts", []) if matches[0]["debug"] else []
                if matches[0]["api_insert"]:
                    previous_api_inserts.append(matches[0]["api_insert"])
                if existing_weaned_obj := matches[0]["data"]:
                    for k, v in existing_weaned_obj.items():
                        if k not in weaned_object:
                            weaned_object[k] = v
                db.matches.update_match(
                    id=matches[0]["id"],
                    time=wean_date,
                    partner_account=partner_account,
                    data=weaned_object,
                    api_insert=api_insert,
                    debug={"previous_api_inserts": previous_api_inserts}
                )
            else:
                db.matches.types.insert_weaned(
                    time=wean_date,
                    partner_account=partner_account,
                    account_link=account_link,
                    data=weaned_object,
                    eid=eid,
                    api_insert=api_insert
                )


def process_animal_characteristics(db, input_data, eid, api_insert_id, visual_id=None, timezone=None):
    try:
        characteristics = {"eid": eid, "api_insert_id": api_insert_id}
        if visual_id:
            characteristics["visual_id"] = visual_id
        if "birth_weight" in input_data and input_data["birth_weight"].strip() != "" and int(input_data["birth_weight"]) > 0:
            characteristics["birth_weight"] = int(input_data["birth_weight"])
        if "breed" in input_data and input_data["breed"].strip() != "":
            characteristics["breed"] = input_data["breed"]
        if "implants" in input_data and input_data["implants"].strip() != "":
            characteristics["implants"] = input_data["implants"]
        if ("calf_reg_no" in input_data and input_data["calf_reg_no"].strip() != ""
                and int(input_data["calf_reg_no"]) > 0):
            characteristics["calf_registration_number"] = int(input_data["calf_reg_no"])
        if ("sire_reg_no" in input_data and input_data["sire_reg_no"].strip() != ""
                and int(input_data["sire_reg_no"]) > 0):
            characteristics["sire_registration_number"] = int(input_data["sire_reg_no"])
        if "dam_reg_no" in input_data and input_data["dam_reg_no"].strip() != "" and int(input_data["dam_reg_no"]) > 0:
            characteristics["dam_registration_number"] = int(input_data["dam_reg_no"])
        if "implants" in input_data and input_data["implants"].strip() != "":
            characteristics["implants"] = input_data["implants"]
        if "sex" in input_data and input_data["sex"].strip() != "":
            characteristics["sex"] = input_data["sex"]
        if "description" in input_data and input_data["description"].strip() != "":
            characteristics["description"] = input_data["description"]
        if "terminal_reimplant_weight" in input_data and input_data["terminal_reimplant_weight"].strip():
            characteristics["terminal_reimplant_weight"] = int(input_data["terminal_reimplant_weight"])
        if "terminal_reimplant_date" in input_data and input_data["terminal_reimplant_date"].strip():
            characteristics["terminal_reimplant_date"] = (
                all_to_unix(input_data["terminal_reimplant_date"], timezone)
                if timezone else all_to_unix(input_data["terminal_reimplant_date"])
            )

        Animals(db).create_or_fail_animal(**characteristics)
    except AnimalsException as e:
        Animals(db).update_animal(**characteristics)
        print(f"Animal exists and updated {eid}: {e}")


def process_feeder_data(db, input_data, eid, api_insert_id, timezone=None):
    feeder_data = {}
    print("input_data", input_data)
    if input_data.get("LotNumber", "").strip():
        feeder_data["lot_number"] = int(input_data["LotNumber"])
    if input_data.get("PenNumber", "").strip():
        feeder_data["pen_number"] = int(input_data["PenNumber"])
    if input_data.get("FeederInternalAccountId", "").strip():
        feeder_data["feeder_account_number"] = int(input_data["FeederInternalAccountId"])
    if input_data.get("FeederWeight", "").strip():
        feeder_data["feeder_weight"] = int(input_data["FeederWeight"])
    if input_data.get("TerminalReImplantWeight", "").strip():
        feeder_data["terminal_reimplant_weight"] = int(input_data["TerminalReImplantWeight"])
    if input_data.get("TerminalReImplantDate", "").strip():
        feeder_data["terminal_reimplant_date"] = (
            all_to_unix(input_data["terminal_reimplant_date"], timezone)
            if timezone else all_to_unix(input_data["terminal_reimplant_date"])
        )

    if feeder_data:
        try:
            Animals(db).create_or_fail_animal(eid=eid, feeder_api_insert_id=api_insert_id, **feeder_data)
        except AnimalsException as e:
            Animals(db).update_animal(eid=eid, feeder_api_insert_id=api_insert_id, **feeder_data)
            print(f"{e}. It has been updated")


def process_packer_data(db, eid, api_insert_id, harvest_date=None, program_certification=None,
                        marbling_score=None, marbling_score_code=None, ribeye_area=None, fat_thickness=None,
                        calculated_live_weight=None, total_gain=None, days_on_test=None, average_daily_gain=None,
                        timezone=None):
    packer_data = {}
    if harvest_date and harvest_date.strip():
        packer_data["harvest_date"] = (
            all_to_unix(harvest_date, timezone)
            if timezone else all_to_unix(harvest_date)
        )
    if program_certification and program_certification.strip():
        packer_data["program_certification"] = program_certification.strip()
    if marbling_score and marbling_score.strip():
        packer_data["marbling_score"] = marbling_score.strip()
    if marbling_score_code and marbling_score_code.strip():
        packer_data["marbling_score_code"] = int(marbling_score_code)
    if ribeye_area and ribeye_area.strip():
        packer_data["ribeye_area"] = float(ribeye_area)
    if fat_thickness and fat_thickness.strip():
        packer_data["fat_thickness"] = float(fat_thickness)
    if calculated_live_weight and calculated_live_weight.strip():
        packer_data["calculated_live_weight"] = int(calculated_live_weight)
    if total_gain and total_gain.strip():
        packer_data["total_gain"] = int(total_gain)
    if days_on_test and days_on_test.strip():
        packer_data["days_on_test"] = int(days_on_test)
    if average_daily_gain and average_daily_gain.strip():
        packer_data["average_daily_gain"] = float(average_daily_gain)

    if packer_data:
        try:
            Animals(db).create_or_fail_animal(eid=eid, packer_api_insert_id=api_insert_id, **packer_data)
        except AnimalsException as e:
            Animals(db).update_animal(eid=eid, packer_api_insert_id=api_insert_id, **packer_data)
            print(f"{e}. It has been updated")


def process_grades_and_weight(
        db, eid, partner_account, api_insert_id, packer_account_link_id,
        yield_grade, quality_grade, carcass_weight, packer_account_id=None, feeder_account_id=None
):

    matches = db.matches.get_matches(eid=eid, account_link=packer_account_link_id,
                                     restrict_type=MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"])
    if yield_grade and yield_grade.strip():
        if matches:
            db.matches.update_match(
                id=matches[0]["id"],
                partner_account=partner_account,
                data=int(float(yield_grade)),
                api_insert=api_insert_id
            )
        else:
            db.matches.types.insert_usda_yield_grade(
                int(float(yield_grade)),
                eid=eid,
                partner_account=partner_account,
                account_link=packer_account_link_id,
                api_insert=api_insert_id
            )
            perform_feeder_packer_data_received_actions(
                db, eid, schedule_email=True, feeder_account_id=feeder_account_id,
                packer_account_id=packer_account_id, api_insert_id=api_insert_id
            )

    matches = db.matches.get_matches(eid=eid, account_link=packer_account_link_id,
                                     restrict_type=MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"])
    if quality_grade and quality_grade.strip():
        if matches:
            db.matches.update_match(
                id=matches[0]["id"],
                partner_account=partner_account,
                data=quality_grade,
                api_insert=api_insert_id
            )
        else:
            if quality_grade and quality_grade.strip():
                db.matches.types.insert_usda_quality_grade(
                    quality_grade,
                    eid=eid,
                    partner_account=partner_account,
                    account_link=packer_account_link_id,
                    api_insert=api_insert_id
                )

    matches = db.matches.get_matches(eid=eid, account_link=packer_account_link_id,
                                     restrict_type=MATCH_TYPES_NAME_TO_ID["Hot Weight"])
    if carcass_weight and carcass_weight.strip():
        if matches:
            db.matches.update_match(
                id=matches[0]["id"],
                partner_account=partner_account,
                data=float(carcass_weight),
                api_insert=api_insert_id
            )
        else:
            if carcass_weight and carcass_weight.strip():
                db.matches.types.insert_hot_weight(
                    weight=float(carcass_weight),
                    eid=eid,
                    partner_account=partner_account,
                    account_link=packer_account_link_id,
                    api_insert=api_insert_id
                )
