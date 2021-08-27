import argparse
import csv
from json import dumps
from datetime import datetime
from ...database.database import Database
from ...config import MYSQL_CONFIG
from ...match_types import match_types_by_name

def insert_helper(db, eid, patronid, type, data=None, time=None):
    #account_link=db.account_links.get_by_affiliate_id(affiliate_id=patronid, insert=True)[0].id(),
    db.matches.insert(
        eid=eid,
        type_int=match_types_by_name[type],     
        raw_identifier=patronid,
        data=data,
        time=time
    )

def date_to_epoch(s):
    n_in = False
    digits = ''.join([str(i) for i in range(10)])
    for c in s:
        if c in digits:
            n_in = True
    if not n_in:
        return 0
    date, time = s.split(" ")
    month, day, year = list(map(int, date.split("/")))
    if year <= 1800:
        return 0
    hms = list(map(int, time.split(":")))
    return int(datetime(year,month,day,*hms).timestamp())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a master animal in CSV encoding.')
    parser.add_argument('file', help='path to master animal CSV file', type=str)
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
                patron_id = 0
                try:
                    patron_id= int(r["patronid"])
                except:
                    print("Skipping", r, "for bad patronid")
                    continue

                # TODO: A lot more matches possible from this
                try:
                    insert_helper(db, r["electronic"], patron_id, "Visual ID", int(r["visualid"]))
                except:
                    insert_helper(db, r["electronic"], patron_id, "Visual ID Complex", r["visualid"])
                    
                weaned_object = {

                }
                
                weaned_object_tags = [("at", "weaningstr"), ("creep_feed", "creepfeed"), ("first_14_feed", "first14day"), ("first_14_method", "first14da1"), ("second_31_feed", "second31da"), ("second_31_method", "second31d1")]

                for tag in weaned_object_tags:
                    if r[tag[1]].strip() != "":
                        weaned_object[tag[0]] = r[tag[1]].strip()

                
                if r["weaningstr"].strip() != "":
                    weaned_object["at"] = r["weaningstr"].strip()
                
                
                
                w_object_res = dumps(weaned_object)
                if w_object_res == "{}":
                    w_object_res = None
                #print(w_object_res)
                insert_helper(db, r["electronic"], patron_id, "Weaned", data=w_object_res, time=date_to_epoch(r["weandate"]))
                insert_helper(db, r["electronic"], patron_id, "Born", time=date_to_epoch(r["firstbirth"]))

                sold_object = {

                }
                if r['marketingm'].strip().lower() not in ('', "unknown"):
                    sold_object["method"] = r['marketingm'].strip()
                if r['salelocati'].strip() != '':
                    sold_object["location"] = r['salelocati'].strip()
                    
                if int(r['numberofca']) != 0:
                    sold_object["group_size"] = int(r['numberofca'])
                
                s_object_res = dumps(sold_object)
                if s_object_res != "{}":
                    insert_helper(db, r["electronic"], patron_id, "Sold", data=s_object_res, time=date_to_epoch(r["marketingd"]))

            except Exception as e:
                print("row_count", row_count)
                print("row", r)
                raise e
