
from core.database.tables.animals import Animals, AnimalsException
from api.translation_worker.all_to_unix import all_to_unix


def process_birth_date(db, fields, eid, visual_id, partner_account, account_link, grouping_id=None, api_insert=None):
    birth_date = all_to_unix(fields["birth_date"]) if "birth_date" in fields else None
    if birth_date is not None:
        db.matches.types.insert_born(
            time=birth_date,
            partner_account=partner_account,
            account_link=account_link,
            eid=eid,
            visual_id=visual_id,
            grouping_id=grouping_id,
            api_insert=api_insert
        )


def process_weaning_data(db, fields, eid, visual_id, partner_account, account_link, grouping_id=None, api_insert=None):
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
        if tag[1] in fields and fields[tag[1]].strip() != "":
            weaned_object[tag[0]] = fields[tag[1]].strip()

    if "wean_weight" in fields and fields["wean_weight"].strip() != "" and int(fields["wean_weight"]) > 0:
        weaned_object["wean_weight"] = int(fields["wean_weight"])

    if weaned_object == {}:
        weaned_object = None
    wean_date = all_to_unix(fields["wean_date"]) if "wean_date" in fields else None
    if wean_date is not None:
        db.matches.types.insert_weaned(
            time=wean_date,
            partner_account=partner_account,
            account_link=account_link,
            data=weaned_object,
            eid=eid,
            visual_id=visual_id,
            grouping_id=grouping_id,
            api_insert=api_insert
        )


def process_animal_characteristics(db, fields, eid, visual_id, api_insert_id):
    try:
        kwargs = {"eid": eid, "visual_id": visual_id, "api_insert_id": api_insert_id}
        if "birth_weight" in fields and fields["birth_weight"].strip() != "" and int(fields["birth_weight"]) > 0:
            kwargs["birth_weight"] = int(fields["birth_weight"])
        if "breed" in fields and fields["breed"].strip() != "":
            kwargs["breed"] = fields["breed"]
        if "implants" in fields and fields["implants"].strip() != "":
            kwargs["implants"] = fields["implants"]
        if "calf_reg_no" in fields and fields["calf_reg_no"].strip() != "" and int(fields["calf_reg_no"]) > 0:
            kwargs["calf_registration_number"] = int(fields["calf_reg_no"])
        if "sire_reg_no" in fields and fields["sire_reg_no"].strip() != "" and int(fields["sire_reg_no"]) > 0:
            kwargs["sire_registration_number"] = int(fields["sire_reg_no"])
        if "dam_reg_no" in fields and fields["dam_reg_no"].strip() != "" and int(fields["dam_reg_no"]) > 0:
            kwargs["dam_registration_number"] = int(fields["dam_reg_no"])
        if "implants" in fields and fields["implants"].strip() != "":
            kwargs["implants"] = fields["implants"]
        if "sex" in fields and fields["sex"].strip() != "":
            kwargs["sex"] = fields["sex"]
        if "description" in fields and fields["description"].strip() != "":
            kwargs["description"] = fields["description"]

        Animals(db).create_or_fail_animal(**kwargs)
    except AnimalsException as e:
        Animals(db).update_animal(**kwargs)
        print(f"Animal exists and updated {eid}: {e}")