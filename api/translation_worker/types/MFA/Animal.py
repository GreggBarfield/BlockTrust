from core.database.tables.matches import Matches
from ...exceptions import ExecutionException
from .blocks import block_eid_from_animal_id
from ...all_to_unix import all_to_unix
from core.database.database import Database
from api.database.inserts_model import InsertsModel


def _check_format(insert):
    keys = ["AnimalID", "EID", "VisualID", "Birthdate", "WeanDate"]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def block_key(insert):
    return None


def handle(db: Database, inserts_model: InsertsModel, insert, block_value):
    _check_format(insert)

    account = insert["account"]
    eid = int(insert["fields"]["EID"])
    visual_id = insert["fields"]["VisualID"]
    birth_date = all_to_unix(insert["fields"]["Birthdate"])
    wean_date = all_to_unix(insert["fields"]["WeanDate"])
    api_insert = insert["id"]

    if (
        visual_id is not None and (
            isinstance(visual_id, str) and visual_id != "" or
            isinstance(visual_id, int) and visual_id != 0
        )
    ):
        Matches(db).types.insert_visual_id(
            account=account,
            visual_id=visual_id,
            eid=eid,
            api_insert=api_insert
        )

    if birth_date is not None:
        Matches(db).types.insert_born(
            account=account,
            time=birth_date,
            eid=eid,
            api_insert=api_insert
        )

    if wean_date is not None:
        Matches(db).types.insert_weaned(
            account=account,
            time=wean_date,
            eid=eid,
            api_insert=api_insert
        )

    return [
        (
            block_eid_from_animal_id(
                insert['account'],
                insert['fields']['AnimalID']
            ),
            insert['fields']['EID']
        )
    ]
