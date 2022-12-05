from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import SECTORS_NAME_TO_ID


def block_key(insert):
    return None


def handle(db: Database, insert):
    fields = insert["fields"]
    eid = int(fields["eid"])  # This might fail!
    account = insert["account"]
    api_insert = insert["id"]
    
    sectors = ["cc", "fd", "pk", "au"]
    sectors_by_abbreviation = {
        "au": "Auction House",
        "cc": "Cow-Calf",
        "fd": "Feedlot",
        "pk": "Packer"
    }

    for sector in sectors:
        lat = fields[sector+"_lat"]
        lon = fields[sector+"_long"]
        date = fields[sector+"_date"]
        company = fields[sector+"_name"].strip()

        if company == "":
            return

        # account_link= db.account_links.get_by_company(
        #                 company,
        #                 insert_sector=sectors_by_name[sectors_by_abbreviation[sector]],
        #                 insert=True
        #             )[0].id()

        db.matches.types.insert_sighting(
            eid=eid,
            time=all_to_unix(date),
            lat=lat,
            lon=lon,
            account=account,
            api_insert=api_insert
        )
