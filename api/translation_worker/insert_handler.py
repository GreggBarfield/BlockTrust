from .types.MFA import Animal
from .types.TestNS import TestTY
from .types.ILS import Packer
from .types.BTN1 import (
    AnimalsCSV, FeederResultsCSV, MatchTableCSV, ProcessingCSV, TreatmentCSV
)
from ..database.inserts_model import statuses_by_name, BlockNotAvailable


types = {
    "MFA": {
        "Animal": Animal
    },
    "TestNS": {
        "TestTY": TestTY
    },
    "ILS": {
        # "Packer": Packer. Not processing ILS till we figure out the account linking
    },
    "BTN1": {
        "AnimalsCSV": AnimalsCSV,
        "FeederResultsCSV": FeederResultsCSV,
        "MatchTableCSV": MatchTableCSV,
        "ProcessingCSV": ProcessingCSV,
        "TreatmentCSV": TreatmentCSV,
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

    # Note that fields is pre-converted
    block_key = handler.block_key(insert)

    if block_key is None:
        block_value = None
    elif insert['api_blocks.resolved'] is not None and insert['api_blocks.resolved'] != 0:
        block_value = insert['api_blocks.value']
    else:
        # Try looking for the block result. If no block result is available,
        # immediately (while under lock) create new block and update insert
        try:
            block_value = inserts_model.blocked_on(block_key, insert['id'])
        except BlockNotAvailable:
            # blocked_on handles status
            # after running blocked_on another worker could potentially pick it up
            return

    # Note that fields is pre-converted
    emitted_blocks = handler.handle(db, inserts_model, insert, block_value=block_value)

    # Handle any emitted blocks
    if emitted_blocks is not None:
        for emitted_block in emitted_blocks:
            key, value = emitted_block
            inserts_model.emit_block(key, value)

    inserts_model.set_status(insert['id'], "Done")
