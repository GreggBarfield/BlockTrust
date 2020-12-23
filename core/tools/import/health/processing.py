import argparse
import csv
from ....database.database import Database
from ....config import MYSQL_CONFIG

from .helper import insert_helper, date_to_epoch


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload processing in CSV encoding.')
    parser.add_argument('file', help='path to processing CSV file', type=str)
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
                insert_helper(
                    db=db,
                    eid=r["electronic"],
                    time=date_to_epoch(r["proc_date"]),
                    type="Medical",
                    product=r["prod_name"],
                    method=r["admin_rt"],
                    location=r["loc_name"],
                )

            except Exception as e:
                print("row_count", row_count)
                print("row", r)
                raise e
