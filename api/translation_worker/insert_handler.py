from .types.ILS import Packer
from .types.BTN1 import (
    AnimalsCSV, FeederResultsCSV, MatchTableCSV, ProcessingCSV, TreatmentCSV, PackerFileDataExport
)
from .types.REDANGUS import (
    Animals
)
from .types.SELF import TagUpload
from .types.EMP import PackerDataUpload


types = {
    "ILS": {
        "Packer": Packer
    },
    "BTN1": {
        "AnimalsCSV": AnimalsCSV,
        "FeederResultsCSV": FeederResultsCSV,
        "MatchTableCSV": MatchTableCSV,
        "ProcessingCSV": ProcessingCSV,
        "TreatmentCSV": TreatmentCSV,
        "PackerFileDataExport": PackerFileDataExport
    },
    "REDANGUS": {
        "Animals": Animals
    },
    "SELF": {
        "TagUpload": TagUpload
    },
    "EMP": {
        "PackerDataUpload": PackerDataUpload
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

    handler.handle(db, insert)

    inserts_model.set_status(insert['id'], "Done")
