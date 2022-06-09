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

    account = db.accounts.get_account_by_id(insert["account"])
    if account is not None:
        account_link_id = account.account_links()[0].id()
        zipcode = str(account.zip())
        if len(zipcode) >= 5:
            f5 = zipcode[0:5]
            for d in f5:
                if d not in "0123456789":
                    break
            else:
                lat, lon = db.zip_codes.get_lat_lon(int(f5))
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
