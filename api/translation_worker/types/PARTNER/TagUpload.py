from api.translation_worker.types.helper import (
    process_animal_characteristics, process_birth_date, process_sighting, process_weaning_data
)
from core.database.tables.accounts import RED_ANGUS_PARTNER_COMPANY
from ...exceptions import ExecutionException


def _check_required(insert):
    keys = [
        "eid", "affiliate_id"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def handle(db, insert):
    """
    Handle a individual insert from a partner.
    """
    _check_required(insert)

    fields = insert['fields']
    sighting_date = fields["birth_date"] if fields.get("birth_date", None) else str(insert['created'])

    eid = int(fields["eid"])
    api_insert = insert["id"]
    visual_id = fields["visual_id"] if "visual_id" in fields and fields["visual_id"] != "" else None

    if len(account_link := db.account_links.get_account_links(
        partner_account=insert['account'], affiliate_id=fields['affiliate_id'])
    ) > 0:
        account_link = account_link[0]
        if len(account := db.accounts.get_accounts(id=account_link["account"])) > 0:
            account = account[0]
            zipcode = str(account["zip"])
            process_sighting(
                db, eid, account_link["id"], api_insert, zipcode, sighting_date,
                insert["account"], account_id=account["id"], sector_id=account["sector"],
                visual_id=visual_id,
                connection_details={"created_by_operation": "Partner Tag Upload", "eid": eid, "api_insert": api_insert}
            )
            process_weaning_data(
                db, fields, eid, insert["account"], account_link["id"], api_insert
            )
            process_birth_date(
                db, fields, eid, insert["account"], account_link["id"], api_insert
            )
            red_angus_partner = db.accounts.get_partners(company=RED_ANGUS_PARTNER_COMPANY)[0]
            if insert["account"] == red_angus_partner["id"]:
                is_paid = int(True)
            else:
                is_paid = int(False)
            process_animal_characteristics(db, fields, eid, api_insert, visual_id, is_paid=is_paid)

        else:
            raise Exception(f"""No account exists for partner: {insert['account']}
                            and affiliate ID: {fields['affiliate_id']}""")
    else:
        raise Exception(f"""No account link exists for partner: {insert['account']}
                         and affiliate ID: {fields['affiliate_id']}""")
