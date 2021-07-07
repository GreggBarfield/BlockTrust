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
    # insert["fields"] = fields = remap(insert["fields"], {
    #     "Sex": "sex",
    #     "FarmID": "farmid",
    #     "ZipCode": "zipcode",
    #     "PatronID": "patronid",
    #     "VisualID": "visualid",
    #     "WeanDate": "weandate",
    #     "CreepFeed": "creepfeed",
    #     "SequenceID": "sequence",
    #     "SysEndTime": "end_time",
    #     "WeanWeight": "weanweight",
    #     "BirthWeight": "birthweigh",
    #     "ElectronicID": "electronic",
    #     "SysStartTime": "st_time",
    #     "ApplicationID": "applicatio",
    #     "CalfBirthDate": "calfbirthd",
    #     "MarketingDate": "marketingd",
    #     "FirstBirthDate": "firstbirth",
    #     "IsVetProcessed": "isvetproce",
    #     "NumberOfCalves": "numberofca",
    #     "ApplicationDate": "appdate",
    #     "CalfDescription": "calfdescri",
    #     "First14DateFeed": "first14day",
    #     "Second31DayFeed": "second31da",
    #     "WeaningStrategy": "weaningstr",
    #     "SaleLocationName": "salelocati",
    #     "MarketingMethodName": "marketingm",
    #     "EstimatedSaleWeaight": "estimateds",
    #     "EstimatedSaleWeight": "estimateds",
    #     "First14DayFeedMethod": "first14da1",
    #     "Second31DayFeedMethod": "second31d1",
    # })

    try:
        #who is the partner? do I get that from the account? and if they don't ahve a partner then we need to do someting
        #patron id is the account id in the partner's table. And so it should come in the json. But in this case we don't have it.
        #patronid = db.accounts.get_by_id(account).partner
        #if patronid is None:
        patronid = 0
    except ValueError as e:
        raise ExecutionException("while converting patron id: " + str(e))
    #account_link = db.account_links.get_by_uid(patronid, 0, insert=True)[0].id()
    eid = int(insert["fields"]["EID"])

    # db.matches.types.insert_visual_id(
    #     visual_id=fields["visualid"],
    #     account=account,
    #     account_link=account_link,
    #     eid=eid,
    # )

    # Sighting
    # no real data about the sighting except the EID. We don't even have an account_link
    db.matches.types.insert_sighting(
        eid=eid,
        account=account,
        account_link=None
    )
