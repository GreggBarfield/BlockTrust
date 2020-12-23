from datetime import datetime
import json
from ....match_types import match_types_by_name

def insert_helper(db, eid, time, type, product=None, location=None, method=None, symptom=None, fatal=False, category=None):

    data = {}

    def is_something(s):
        return s is not None and s.strip().lower() not in ("n/a", "none", "", "na", "other", "unknown")

    if is_something(product):
        data["product"] = product
    if is_something(location):
        data["location"] = location
    if is_something(symptom):
        data["symptom"] = symptom
    if is_something(method):
        data["method"] = method
    if fatal:
        data["fatal"] = fatal
    if is_something(category):
        data["category"] = category
        

    data = json.dumps(data)

    all_digits = False
    for digit in str(eid):
        if digit not in "0123456789":
            print("Skipping for eid issue",eid,time,product)
            return
    
    if data=={}:
        print("Skipping for lack of data",eid,time,type,product,location,method,symptom,fatal)
        return

    db.matches.insert(
        eid=eid,
        type_int=match_types_by_name[type],
        time=time,
        data=data
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
