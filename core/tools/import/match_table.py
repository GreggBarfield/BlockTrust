import argparse
import csv
from datetime import datetime
from ...database.database import Database
from ...config import MYSQL_CONFIG
from ...match_types import match_types_by_name
from ...sectors import sectors_by_name

def insert_helper(db, sector, eid, company, date, lat, lon):
    if company == "" or eid == "":
        return
    t = None
    if date != "":
        month, day, year = list(map(int, date.split("/")))
        t = int(datetime(year,month,day,0,0).timestamp())

    sectors_by_abbreviation = {
        "au": "Auction House",
        "cc": "Cow-Calf",
        "fd": "Feedlot",
        "pk": "Packer"
    }

    # account_link = db.account_links.get_by_company(company, insert_sector=sectors_by_name[sectors_by_abbreviation[sector]], insert=True)[0].id(),
    db.matches.insert(
        eid=eid,
        type_int=match_types_by_name["Sighting"],
        lat=lat,
        lon=lon,
        time=t,
        raw_identifier=company
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a match table in CSV encoding.')
    parser.add_argument('file', help='path to match table CSV file', type=str)
    args = parser.parse_args()

    db = Database(MYSQL_CONFIG)
    with open(args.file) as f:
        reader = csv.DictReader(f)

        for r in reader:
            # Cow Calf cc
            sectors = ["cc", "fd", "pk", "au"]

            for sector in sectors:
                insert_helper(db, sector, r["eid"], r[sector + "_name"], r[sector + "_date"], r[sector+"_lat"], r[sector+"_long"])
