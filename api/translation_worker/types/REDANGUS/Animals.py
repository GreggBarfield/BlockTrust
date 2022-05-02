from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from api.translation_worker.remapper import remap
from core.sectors import sectors_by_name
from ...exceptions import ExecutionException


def block_key(insert):
    return None


def handle(db: Database, insert):
    partner_account = insert["account"]
    api_insert = insert["id"]
    insert["fields"] = fields = remap(insert["fields"], {
        "Sex": "sex",
        "FarmID": "farmid",
        "ZipCode": "zipcode",
        "PatronId": "patronid",
        "VisualID": "visualid",
        "WeanDate": "weandate",
        "CreepFeed": "creepfeed",
        "SequenceID": "sequence",
        "SysEndTime": "end_time",
        "WeanWeight": "weanweight",
        "BirthWeight": "birthweigh",
        "EID": "electronic",
        "SysStartTime": "st_time",
        "ApplicationID": "applicatio",
        "CalfBirthDate": "calfbirthd",
        "MarketingDate": "marketingd",
        "FirstBirthDate": "firstbirth",
        "IsVetProcessed": "isvetproce",
        "NumberOfCalves": "numberofca",
        "ApplicationDate": "appdate",
        "CalfDescription": "calfdescri",
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
        patronid = fields["patronid"]
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

    weaned_object = {}

    weaned_object_tags = [
        ("at", "weaningstr"),
        ("creep_feed", "creepfeed"),
        ("first_14_feed", "first14day"),
        ("first_14_method", "first14da1"),
        ("second_31_feed", "second31da"),
        ("second_31_method", "second31d1")
    ]

    for tag in weaned_object_tags:
        if tag[1] in fields and fields[tag[1]].strip() != "":
            weaned_object[tag[0]] = fields[tag[1]].strip()

    if "weaningstr" in fields and fields["weaningstr"].strip() != "":
        weaned_object["at"] = fields["weaningstr"].strip()

    if "weanweight" in fields and fields["weanweight"].strip() != "" and int(fields["weanweight"]) > 0:
        weaned_object["wean_weight"] = int(fields["weanweight"])

    if weaned_object == {}:
        weaned_object = None

    wean_date = all_to_unix(fields["weandate"]) if "weandate" in fields else None
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

    birth_date = all_to_unix(fields["firstbirth"]) if "firstbirth" in fields else None
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

    sold_object = {}
    if "marketingm" in fields and fields['marketingm'].strip().lower() not in ('', "unknown"):
        sold_object["method"] = fields['marketingm'].strip()
    if "salelocati" in fields and fields['salelocati'].strip() != '':
        sold_object["location"] = fields['salelocati'].strip()

    if "numberofca" in fields and fields['numberofca'] != '' and int(fields['numberofca']) > 0:
        sold_object["group_size"] = int(fields['numberofca'])

    if sold_object != {}:
        db.matches.types.insert_sold(
            partner_account=partner_account,
            account_link=account_link,
            eid=eid,
            visual_id=visual_id,
            time=all_to_unix(fields["marketingd"]),
            data=sold_object,
            grouping_id=grouping_id,
            api_insert=api_insert
        )


    animal_details = {}
    animal_object_tags = [
        ("sex", "sex"),
        ("description", "calfdescri")
    ]

    for tag in animal_object_tags:
        if tag[1] in fields and fields[tag[1]].strip() != "":
            animal_details[tag[0]] = fields[tag[1]].strip()

    if "birthweigh" in fields and fields["birthweigh"].strip() != "" and int(fields["birthweigh"]) > 0:
        animal_details["birth_weight"] = int(fields["birthweigh"])

    if animal_details == {}:
        animal_details = None

    if 'zipcode' in fields and fields['zipcode']:
        zipcode = str(fields['zipcode'])
        f5 = zipcode[0:5] if len(zipcode) > 5 else zipcode
        for d in f5:
            if d not in "0123456789":
                break
        else:
            lat, lon = db.zip_codes.get_lat_lon(int(f5))
            db.matches.types.insert_sighting(
                eid=eid,
                visual_id=visual_id,
                time=all_to_unix(fields['appdate']),
                lat=lat,
                lon=lon,
                partner_account=partner_account,
                account_link=account_link,
                grouping_id=grouping_id,
                debug={"zip": f5},
                api_insert=api_insert,
                data=animal_details
            )
