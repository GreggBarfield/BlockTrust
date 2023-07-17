from api.translation_worker.types.helper import process_grades_and_weight, process_packer_data, process_sighting
from ...exceptions import ExecutionException
from core.database.database import Database


def _check_format(insert):
    keys = [
        "eid", "packer_account_number"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def handle(db: Database, insert):
    """Handle a Packer insert from Employee to create matches and add account links (if necessary)
    """
    _check_format(insert)

    fields = insert['fields']

    partner_account = insert["account"]
    eid = int(fields["eid"])
    api_insert = insert["id"]

    packer = db.accounts.get_accounts(id=fields["packer_account_number"])[0]
    packer_account_link_id = db.account_links.get_account_links(account_id=packer["id"])[0]["id"]
    # if packer is not None:
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

    process_grades_and_weight(
        db, eid=eid, partner_account=partner_account, api_insert_id=api_insert,
        packer_account_link_id=packer_account_link_id,
        yield_grade=fields.get("yield_grade", None),
        quality_grade=fields.get("quality_grade", None),
        carcass_weight=fields.get("carcass_weight", None),
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
        average_daily_gain=fields.get("average_daily_gain", None)
    )
