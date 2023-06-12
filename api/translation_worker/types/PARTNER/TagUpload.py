from api.translation_worker.types.helper import process_animal_characteristics, process_birth_date, process_sighting, process_weaning_data
from core.database.combinations import create_connection_with_eid_owner, create_connection_with_all_sighted_accounts_for_eid
from core.sectors import SECTORS_NAME_TO_ID
from ...exceptions import ExecutionException
from pytz import timezone


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
    date_created = str(insert['created'])

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
                db, eid, account_link["id"], api_insert, zipcode, date_created,
                insert["account"], visual_id
            )
            process_weaning_data(
                db, fields, eid, insert["account"], account_link["id"], api_insert
            )
            process_birth_date(
                db, fields, eid, insert["account"], account_link["id"], api_insert
            )
            process_animal_characteristics(db, fields, eid, api_insert, visual_id)

            if account["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"]:
                create_connection_with_all_sighted_accounts_for_eid(
                    db, eid, account["id"],
                    details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert}
                )
            else:
                create_connection_with_eid_owner(
                    db=db, eid=eid, connecting_account_id=account["id"],
                    details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert}
                )
    else:
        raise Exception(f"""No account exists for partner: {insert['account']}
                         and affiliate ID: {fields['affiliate_id']}""")
