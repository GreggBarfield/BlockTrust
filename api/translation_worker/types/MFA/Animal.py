from ...exceptions import ExecutionException
from .blocks import block_eid_from_animal_id
from .datetime import all_to_unix


def _check_format(insert):
    keys = ["AnimalID", "EID", "VisualID", "Birthdate", "WeanDate"]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def block_key(insert):
    return None


def handle(db, inserts_model, insert, block_value):
    _check_format(insert)

    account = insert["account"]
    eid = int(insert["fields"]["EID"])
    visual_id = insert["fields"]["VisualID"]
    birth_date = all_to_unix(insert["fields"]["Birthdate"])
    wean_date = all_to_unix(insert["fields"]["WeanDate"])

    if (
        visual_id is not None and (
            isinstance(visual_id, str) and visual_id != "" or
            isinstance(visual_id, int) and visual_id != 0
        )
    ):
        db.matches.types.insert_visual_id(
            account=account,
            visual_id=visual_id,
            eid=eid
        )

    if birth_date is not None:
        db.matches.types.insert_born(
            account=account,
            unix=birth_date,
            eid=eid
        )

    if wean_date is not None:
        db.matches.types.insert_weaned(
            account=account,
            unix=wean_date,
            eid=eid
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
