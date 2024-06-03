from api.translation_worker.types.helper import process_animal_characteristics, process_birth_date, insert_sighting_if_not_exists, process_weaning_data
from core.database.database import Database
from api.translation_worker.all_to_unix import all_to_unix
from core.database.tables.matches import Matches
from core.utilities.zip_codes import get_lat_lon
from ...exceptions import ExecutionException
from .remapper import remap


def block_key(insert):
    return None


def handle(db: Database, insert):
    partner_account = insert["account"]
    if "partner_id" in insert["fields"]:
        partner_account = insert["fields"]["partner_id"]
    api_insert = insert["id"]
    insert["fields"] = fields = remap(insert["fields"], {
        "Sex": "sex",
        "FarmID": "farmid",
        "ZipCode": "zipcode",
        "PatronID": "patronid",
        "VisualID": "visualid",
        "WeanDate": "wean_date",
        "CreepFeed": "creep_feed",
        "SequenceID": "sequence",
        "SysEndTime": "end_time",
        "WeanWeight": "wean_weight",
        "BirthWeight": "birth_weight",
        "ElectronicID": "electronic",
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

    grouping_id = None
    if "applicatio" in fields.keys() and fields["applicatio"] != "":
        grouping_id = int(fields["applicatio"])

    process_weaning_data(db, fields, eid, partner_account, account_link, api_insert)

    process_birth_date(db, fields, eid, partner_account, account_link, api_insert)

    sold_object = {}
    if "marketingm" in fields and fields['marketingm'].strip().lower() not in ('', "unknown"):
        sold_object["method"] = fields['marketingm'].strip()
    if "salelocati" in fields and fields['salelocati'].strip() != '':
        sold_object["location"] = fields['salelocati'].strip()

    if "numberofca" in fields and fields['numberofca'] != '' and int(fields['numberofca']) > 0:
        sold_object["group_size"] = int(fields['numberofca'])

    if sold_object != {}:
        Matches(db).types.insert_sold(
            partner_account=partner_account,
            account_link=account_link,
            eid=eid,
            visual_id=visual_id,
            time=all_to_unix(fields["marketingd"]),
            data=sold_object,
            grouping_id=grouping_id,
            api_insert=api_insert
        )

    if 'zipcode' in fields and fields['zipcode']:
        zipcode = str(fields['zipcode'])
        insert_sighting_if_not_exists(
            db, eid, account_link, api_insert, zipcode, fields['appdate'], partner_account, visual_id, grouping_id
        )

    process_animal_characteristics(db, fields, eid, api_insert, visual_id)
