import argparse
import csv
from database.database import Database
from config import MYSQL_CONFIG
from datetime import datetime
from match_types import match_types_by_name
from sectors import sectors_by_name

def insert_helper(db, eid, time, company, type, data):

    db.matches.insert(
        eid=eid,
        type_int=match_types_by_name[type],
        account_link=db.account_links.get_by_company(company, insert_sector=sectors_by_name["Packer"], insert=True)[0].id(),
        raw_identifier=company,
        time=time,
        data=data
    )

def date_to_epoch(s):
    month, day, year = list(map(int, s.split("/")))
    if year <= 1800:
        return 0
    return int(datetime(year,month,day).timestamp())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a feeder results in CSV encoding.')
    parser.add_argument('file', help='path to feeder results CSV file', type=str)
    args = parser.parse_args()

    db = Database(MYSQL_CONFIG)
    with open(args.file) as f:
        reader = csv.DictReader(f)

        row_count = 0
        for r in reader:
            row_count += 1
            if row_count % 100 == 0:
                print(row_count)
            try:
                died = False
                if int(float(r["hotwt"])) != 0:
                    died = True
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "Hot Weight", int(float(r["hotwt"])))
                if r["grade1"].strip() != "":
                    died = True
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "USDA Quality Grade", (r["grade1"].strip()))
                if int(r["side1yiel1"]) != 0:
                    died = True
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "USDA Yield Grade", int(r["side1yiel1"]))
                if int(r["railedind"]) != 0:
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "Railed", None)
                if r["packer"].strip() != "":
                    packer_str = r["packer"].strip() + ";" + r["plantid"].strip()
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "Packer", packer_str)
                if died:
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "Died", None)
                elif int(r["deadind"]) != 0:
                    s = "Died before being packed"
                    if int(r["treat_cnt"]) != 0:
                        s += " after being treated " + r["treat_cnt"] + " times"
                    insert_helper(db, r["eid"], date_to_epoch(r["killdate"]), r["packer"], "Died", s)

            except Exception as e:
                print("row_count", row_count)
                print("row", r)
                raise e
