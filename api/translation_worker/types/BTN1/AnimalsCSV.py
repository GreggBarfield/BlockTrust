from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import sectors_by_name
from ...exceptions import ExecutionException
from .remapper import remap


def block_key(insert):
    return None


def handle(db: Database, inserts_model: InsertsModel, insert, block_value):
    account = insert["account"]
    api_insert = insert["id"]
    insert["fields"] = fields = remap(insert["fields"], {
        "Sex": "sex",
        "FarmID": "farmid",
        "ZipCode": "zipcode",
        "PatronID": "patronid",
        "VisualID": "visualid",
        "WeanDate": "weandate",
        "CreepFeed": "creepfeed",
        "SequenceID": "sequence",
        "SysEndTime": "end_time",
        "WeanWeight": "weanweight",
        "BirthWeight": "birthweigh",
        "ElectronicID": "electronic",
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
        patronid = int(fields["patronid"])
    except ValueError as e:
        raise ExecutionException("while converting patron id: " + str(e))
    account_link = db.account_links.get_by_affiliate_id(patronid, partner_account=account, api_insert=api_insert, insert=True)[0].id()
    eid = int(fields["electronic"])

    grouping_id = 0
    if "ApplicationID" in fields.keys():
        grouping_id = int(fields["ApplicationID"])
    elif "applicatio" in fields.keys():
        grouping_id = int(fields["applicatio"])

    db.matches.types.insert_visual_id(
        visual_id=fields["visualid"],
        account=account,
        account_link=account_link,
        eid=eid,
        grouping_id=grouping_id,
        api_insert=api_insert
    )

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
        if fields[tag[1]].strip() != "":
            weaned_object[tag[0]] = fields[tag[1]].strip()

    if fields["weaningstr"].strip() != "":
        weaned_object["at"] = fields["weaningstr"].strip()

    if weaned_object == {}:
        weaned_object = None

    db.matches.types.insert_weaned(
        time=all_to_unix(fields["weandate"]),
        account=account,
        account_link=account_link,
        data=weaned_object,
        eid=eid,
        grouping_id=grouping_id,
        api_insert=api_insert
    )

    db.matches.types.insert_born(
        time=all_to_unix(fields["firstbirth"]),
        account=account,
        account_link=account_link,
        eid=eid,
        grouping_id=grouping_id,
        api_insert=api_insert
    )

    sold_object = {}
    if fields['marketingm'].strip().lower() not in ('', "unknown"):
        sold_object["method"] = fields['marketingm'].strip()
    if fields['salelocati'].strip() != '':
        sold_object["location"] = fields['salelocati'].strip()

    if int(fields['numberofca']) != 0:
        sold_object["group_size"] = int(fields['numberofca'])

    if sold_object != {}:
        db.matches.types.insert_sold(
            account=account,
            account_link=account_link,
            eid=eid,
            time=all_to_unix(fields["marketingd"]),
            data=sold_object,
            grouping_id=grouping_id,
            api_insert=api_insert
        )

    if 'zipcode' in fields and fields['zipcode'] and 'patronid' in fields and fields['patronid']:
        zipcode = str(fields['zipcode'])
        patronid = int(fields['patronid'])

        if len(zipcode) >= 5 and patronid > 0:
            f5 = zipcode[0:5]
            for d in f5:
                if d not in "0123456789":
                    break
            else:
                account_link = (
                    db.account_links.get_by_affiliate_id(
                        affiliate_id=patronid,
                        partner_account=account,
                        api_insert=api_insert,
                        insert=True
                    )[0].id()
                )
                lat, lon = db.zip_codes.get_lat_lon(int(f5))
                db.matches.types.insert_sighting(
                    eid=eid,
                    time=all_to_unix(fields['appdate']),
                    lat=lat,
                    lon=lon,
                    account=account,
                    account_link=account_link,
                    grouping_id=grouping_id,
                    api_insert=api_insert
                )
