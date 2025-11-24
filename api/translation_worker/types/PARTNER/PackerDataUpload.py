from api.translation_worker.types.helper import process_grades_and_weight, process_packer_data, process_sighting, process_kill_date
from ...exceptions import ExecutionException
from core.database.database import Database
from core.database.tables.api_inserts_unknown_fields import APIInsertsUnknownFields
from core.utilities.field_lists import CARCASS_DATA_ACCEPTED_FIELDS
from remapper import remap


def _check_format(insert):
    eid_present = False
    if "eid" in insert["fields"] or "EID" in insert["fields"]:
        eid_present = True
    if not eid_present:
        raise ExecutionException("Key missing: EID")



def handle(db: Database, insert):
    """Handle a Packer insert from Employee to create matches and add account links (if necessary)
    """
    _check_format(insert)
    insert["fields"] = fields = remap(insert["fields"], {
        "HotWt": "hot_weight"
    })
    partner_account = insert["account"]
    eid = 0
    if "eid" in fields:
        eid = int(fields["eid"])
    elif "EID" in fields:
        eid = int(fields["EID"])
    api_insert = insert["id"]

    if "plant_id" in fields:
        if fields["plant_id"].isdigit():
            fields["plant_id"] =  fields["plant_id"].strip("0")
        packer_account_link = db.account_links.get_account_links(partner_account, fields["plant_id"])[0]        
        packer = db.accounts.get_accounts(id=packer_account_link["account"])[0]
        packer_account_link_id = packer_account_link["id"]
    elif "packer_account_number" in fields:
        packer = db.accounts.get_accounts(id=fields["packer_account_number"])[0]
        packer_account_link_id = db.account_links.get_account_links(account_id=packer["id"])[0]["id"]
    else:
        raise Exception("Both plant_id and packer_account_number missing")

    zipcode = str(packer["zip"])
    if len(zipcode) >= 5:
        f5 = zipcode[0:5]
        for d in f5:
            if d not in "0123456789":
                break
        else:
            sighting_date = fields["harvest_date"] if fields.get("harvest_date", None) else str(insert["created"])
            process_sighting(
                db, eid, packer_account_link_id, api_insert, f5,
                sighting_date, partner_account, account_id=packer["id"],
                sector_id=packer["sector"],
                connection_details={
                    "created_by_operation": "Partner Packer Upload", "eid": eid, "api_insert": api_insert
                }
            )

    
    for field in fields.keys():
        if field not in CARCASS_DATA_ACCEPTED_FIELDS:
            unknown_field_rows = APIInsertsUnknownFields(db).get(unknown_field_name=field)
            if len(unknown_field_rows) == 0:
                APIInsertsUnknownFields(db).insert(
                    account_id=partner_account,
                    api_action="Insert",
                    api_action_type=insert["type"],
                    unknown_field_name=field,
                    unknown_field_data=str(fields[field])
                )

    process_grades_and_weight(
        db, eid=eid, partner_account=partner_account, api_insert_id=api_insert,
        packer_account_link_id=packer_account_link_id,
        yield_grade=fields.get("yield_grade", None),
        quality_grade=fields.get("quality_grade", None),
        carcass_weight=fields.get("hot_weight", None),
        packer_account_id=packer["id"] if packer else None
    )

    process_packer_data(
        db=db, eid=eid, api_insert_id=api_insert,
        harvest_date=fields.get("harvest_date", None),
        program_certification=fields.get("program_certification", None),
        marbling_score=fields.get("marbling_score", None),
        marbling_score_code=fields.get("marbling_score_code", None),
        ribeye_area=fields.get("ribeye_area", None),
        fat_thickness=fields.get("fat_thickness", None),
        calculated_live_weight=fields.get("calculated_live_weight", None),
        total_gain=fields.get("total_gain", None),
        days_on_test=fields.get("days_on_test", None),
        average_daily_gain=fields.get("average_daily_gain", None),
        over_30=fields.get("over_30", None),
        hard_bone=fields.get("hard_bone", None),
        dark_cutter=fields.get("dark_cutter", None),
        average_lot_live=fields.get("Avg_Lot_Live", None),
        back_fat=fields.get("back_fat", None)
    )

    if fields.get("kill_date", None) is not None:
        process_kill_date(
            db, eid=eid, partner_account=partner_account, api_insert_id=api_insert,
            packer_account_link_id=packer_account_link_id,
            kill_date=fields.get("kill_date", None)
        )
