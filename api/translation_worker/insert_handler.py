from .types.MFA import Animal
from .types.TestNS import TestTY
from .types.ILS import Packer
from .types.BTN1 import (
    AnimalsCSV, FeederResultsCSV, MatchTableCSV, ProcessingCSV, TreatmentCSV
)
from ..database.inserts_model import statuses_by_name, BlockNotAvailable


types = {
    "ILS": {
        "Packer": Packer
    },
    "BTN1": {
        "AnimalsCSV": AnimalsCSV,
        "FeederResultsCSV": FeederResultsCSV,
        "MatchTableCSV": MatchTableCSV,
        "ProcessingCSV": ProcessingCSV,
        "TreatmentCSV": TreatmentCSV
    }
}


def handle_insert(db, inserts_model, insert):
    """Handle an insert.

    Params:
        db: A Database object
        inserts_model: An InsertsModel object
        insert: An insert dictionary, with 'api_blocks.value' and 'api_blocks.resolved'
    """

    if insert['namespace'] not in types:
        inserts_model.set_status(insert['id'], "Bad Namespace")
        return

    if insert['type'] not in types[insert['namespace']]:
        inserts_model.set_status(insert['id'], "Bad Type")
        return

    handler = types[insert['namespace']][insert['type']]

    handler.handle(db, inserts_model, insert)

    inserts_model.set_status(insert['id'], "Done")
