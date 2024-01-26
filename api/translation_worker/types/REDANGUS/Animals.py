from api.translation_worker.types.helper import process_animal_characteristics, process_sighting
from core.database.database import Database
from core.database.tables.animals import Animals, AnimalsException
from api.translation_worker.all_to_unix import all_to_unix
from api.translation_worker.remapper import remap
from core.utilities.zip_codes import get_lat_lon
from ...exceptions import ExecutionException


def block_key(insert):
    return None


def handle(db: Database, insert):
    partner_account = insert["account"]
    api_insert = insert["id"]
    insert["fields"] = fields = remap(insert["fields"], {
        "Sex": "sex",
        "FarmID": "farmid",
        "Zip": "zipcode",
        "PatronId": "patronid",
        "VisualID": "visualid",
        "WeanDate": "wean_date",
        "CreepFeed": "creep_feed",
        "SequenceID": "sequence",
        "SysEndTime": "end_time",
        "WeanWeight": "wean_weight",
        "BirthWeight": "birth_weight",
        "EID": "electronic",
        "SysStartTime": "st_time",
        "ApplicationID": "applicatio",
        "CalfBirthDate": "calfbirthd",
        "MarketingDate": "marketingd",
        "FirstBirthDate": "birth_date",
        "IsVetProcessed": "isvetproce",
        "NumberOfCalves": "numberofca",
        "ApplicationDate": "appdate",
        "CalfDescription": "description",
        "First14DateFeed": "first14day",
        "Second31DayFeed": "second31da",
        "WeaningStrategy": "weaningstr",
        "SaleLocationName": "salelocati",
        "MarketingMethodName": "marketingm",
        "EstimatedSaleWeaight": "estimateds",
        "EstimatedSaleWeight": "estimateds",
        "First14DayFeedMethod": "first14da1",
        "Second31DayFeedMethod": "second31d1",
    })
    try:
        patronid = int(fields["patronid"]) if fields["patronid"].isdigit() else fields["patronid"]
        if patronid is None or patronid == '':
            raise Exception("patron id is none or blank")
    except Exception as e:
        raise ExecutionException("patron id error: " + str(e))
    account_link = db.account_links.get_by_affiliate_id(patronid, partner_account=partner_account, api_insert=api_insert, insert=True)[0]

    # See if account is present but not linked to account_links and if so link the account.
    if account_link.account_id() is None:
        account = db.accounts.get_by_partner_affiliate_id(account_link.partner_account_id(), account_link.affiliate_id())
        if account is not None:
            db.account_links.update_account_link_with_account(account.partner_account_id(), account.affiliate_id(), account.sector_id(), account.company(), account.name(), account.id())

    account_link = account_link.id()
    eid = int(fields["electronic"])
    visual_id = fields["visualid"] if "visualid" in fields and fields["visualid"] != "" else None

    if 'zipcode' in fields and fields['zipcode']:
        zipcode = str(fields['zipcode'])
        process_sighting(db, eid, account_link, api_insert, zipcode, fields['appdate'], partner_account, visual_id)

    process_animal_characteristics(db, fields, eid, api_insert, visual_id, is_paid=int(True))
