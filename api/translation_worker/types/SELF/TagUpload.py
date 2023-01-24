from core.database.combinations import create_connection_with_eid_owner, create_connection_with_all_sighted_accounts_for_eid
from core.utilities.zip_codes import get_lat_lon
from core.sectors import SECTORS_NAME_TO_ID
from core.match_types import MATCH_TYPES_NAME_TO_ID
from core.database.tables.connections import Connections, CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_NAME_TO_ID, ConnectionException
from ...exceptions import ExecutionException
from ...all_to_unix import all_to_unix

def _check_format(insert):
    keys = [
        "EID"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def handle(db, insert):
    """Handle a individual insert from the owner of an account (rancher).

    Currently processing fields like
        {
            "EID": "982000423956846"
        }
    """
    _check_format(insert)

    fields = insert['fields']
    date_created = str(insert['created'])

    eid = int(fields["EID"])
    api_insert = insert["id"]
    visual_id = fields["VisualID"] if "VisualID" in fields and fields["VisualID"] != "" else None

    accounts = db.accounts.get_accounts(id=insert["account"])
    if len(accounts) > 0:
        uploader_account = accounts[0]
        account_link_id = db.account_links.get_account_links(account_id=uploader_account["id"])[0]["id"]
        zipcode = str(uploader_account["zip"])
        if len(zipcode) >= 5:
            f5 = zipcode[0:5]
            for d in f5:
                if d not in "0123456789":
                    break
            else:
                lat, lon = get_lat_lon(int(f5))
                db.matches.types.insert_sighting(
                    eid=eid,
                    visual_id=visual_id,
                    time=all_to_unix(date_created),
                    lat=lat,
                    lon=lon,
                    partner_account=insert["account"],
                    account_link=account_link_id,
                    api_insert=api_insert,
                    zip=zipcode
                )

                if uploader_account["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"]:
                    create_connection_with_all_sighted_accounts_for_eid(
                        db, eid, uploader_account["id"],
                        details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert})
                else:
                    create_connection_with_eid_owner(
                        db=db, eid=eid, connecting_account_id=uploader_account["id"],
                        details={"created_by_operation": "Tag Upload", "eid": eid, "api_insert": api_insert}
                    )
