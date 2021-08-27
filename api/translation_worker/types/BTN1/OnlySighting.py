from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import sectors_by_name
from ...exceptions import ExecutionException
from .remapper import remap


def block_key(insert):
    return None

# TODO: below code is incomplete and needs further development


def handle(db: Database, inserts_model: InsertsModel, insert, block_value):
    account = insert["account"]

    #eid = int(insert["fields"]["EID"])

    # Sighting
    # no real data about the sighting except the EID. 
    # db.matches.types.insert_sighting(
    #     eid=eid,
    #     account=account,
    #     account_link=None
    # )
