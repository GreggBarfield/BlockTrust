from api.translation_worker.types.helper import process_animal_characteristics, process_birth_date, process_sighting, process_weaning_data
from core.database.combinations import create_connection_with_eid_owner, create_connection_with_all_sighted_accounts_for_eid
from core.sectors import SECTORS_NAME_TO_ID
from ...exceptions import ExecutionException


def _check_required(insert):
    keys = [
        "eid"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def handle(db, insert):
    """Handle a individual insert from the owner of an account (rancher).

    Currently processing fields like
        {
            "eid": "982000423956846",
            "visual_id": "ABCDE",
            "breed": "Red Baldy",
            "birth_date": "12/1/2022",
            "birth_weight": "55",
            "calf_reg_no": "812311",
            "sire_reg_no": "534311",
            "wean_date": "12/30/2022",
            "wean_weight": "300",
            "creep_feed": "Yes",
            "sex": "S",
            "implants": "Yes"
        }
    """
    _check_required(insert)

    fields = insert['fields']
    date_created = fields['sighting_date'] if fields.get('sighting_date', None) else str(insert['created'])

    eid = int(fields["eid"])
    api_insert = insert["id"]
    visual_id = fields["visual_id"] if "visual_id" in fields and fields["visual_id"] != "" else None

    accounts = db.accounts.get_accounts(id=insert["account"])
    if len(accounts) > 0:
        uploader_account = accounts[0]
        account_link_id = db.account_links.get_account_links(account_id=uploader_account["id"])[0]["id"]
        zipcode = str(uploader_account["zip"])
        process_sighting(
            db, eid, account_link_id, api_insert, zipcode, date_created,
            insert["account"], visual_id
        )
        process_weaning_data(
            db, fields, eid, insert["account"], account_link_id, api_insert
        )
        process_birth_date(
            db, fields, eid, insert["account"], account_link_id, api_insert
        )
        process_animal_characteristics(db, fields, eid, api_insert, visual_id)

        if uploader_account["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"]:
            create_connection_with_all_sighted_accounts_for_eid(
                db, eid, uploader_account["id"],
                details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert})
        else:
            create_connection_with_eid_owner(
                db=db, eid=eid, connecting_account_id=uploader_account["id"],
                details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert}
            )
