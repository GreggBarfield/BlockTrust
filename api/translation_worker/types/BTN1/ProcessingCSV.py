from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from core.database.tables.matches import Matches
from .medical_helper import format_data
from .remapper import remap
from ...exceptions import ExecutionException


def block_key(insert):
    return None


def handle(db: Database, insert):
    insert["fields"] = fields = remap(insert["fields"], {
        "LotNumber": "lot_no",
        "SequenceID": "sequence",
        "SysEndTime": "end_time",
        "ProductName": "prod_name",
        "ElectronicID": "electronic",
        "LocationName": "loc_name",
        "SysStartTime": "st_time",
        "ProcessingDate": "proc_date",
        "AdministrationRouteName": "admin_rt",
        "AdminstrationRouteName": "admin_rt"
    })
    time = all_to_unix(fields["proc_date"])
    account = insert["account"]
    eid = int(fields["electronic"])  # This might fail!
    api_insert = insert["id"]

    if time is None:
        raise ExecutionException("Time is none")

    medical_data = format_data(
        product=fields.get("prod_name", None),
        method=fields.get("admin_rt", None),
        location=fields.get("loc_name", None),
        diagnosis=fields.get("diagnosis", None)
    )

    if medical_data is None or medical_data == {}:
        raise ExecutionException("Medical data is none")

    Matches(db).types.insert_medical(
        time=time,
        data=medical_data,
        eid=eid,
        partner_account=account,
        api_insert=api_insert
    )
