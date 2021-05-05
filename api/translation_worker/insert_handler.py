from .types.MFA import Animal
from .types.TestNS import TestTY
from .types.ILS import Packer
from .types.BTN1 import (
    AnimalsCSV, FeederResultsCSV, MatchTableCSV, ProcessingCSV, TreatmentCSV
)
from ..database.inserts_model import statuses_by_name, BlockNotAvailable
from .abstract_type import AbstractType
from core.utilities.blockchain.transmit import transmit
from core.config import BLOCKCHAIN_TRANSLATION_WORKER_UPLOADS


types = [
    Animal.AnimalType,
    TestTY.TestTYType,
    Packer.PackerType,
    AnimalsCSV.AnimalsCSVType,
    FeederResultsCSV.FeederResultsCSVType,
    MatchTableCSV.MatchTableCSVType,
    ProcessingCSV.ProcessingCSVType,
    TreatmentCSV.TreatmentCSVType,
]

types_lookup = {}

for cur in types:
    pair = (cur.NAMESPACE, cur.TYPE)
    if pair in types_lookup:
        raise ValueError("Duplicate pair found.")
    types_lookup[pair] = cur


class InsertHandlerError(Exception):
    """Generic insert handler error"""
    pass


class InsertHandlerErrorBadType(Exception):
    """Insert has an unrecognized type"""
    pass


class InsertHandlerErrorBlocked(Exception):
    """Insert got blocked (unfulfilled block key)"""
    pass


def handle_insert(db, inserts_model, insert):
    """Handle an insert.

    Does not modify the original insert, but might
        insert new unfulfilled block keys.

    Params:
        db: A Database object
        inserts_model: An InsertsModel object
        insert: An insert dictionary, with 'api_blocks.value' and 'api_blocks.resolved'

    Returns:
        emitted matches, emitted blocks
    """

    if (insert['namespace'], insert['type']) not in types_lookup:
        raise InsertHandlerErrorBadType()

    handler: AbstractType = types_lookup[(insert['namespace'], insert['type'])](
        db=db,
        inserts_model=inserts_model,
        insert=insert
    )

    # Note that fields are pre-converted
    block_key = handler.block_key()

    if block_key is None:
        block_value = None
    elif insert['api_blocks.resolved'] is not None and insert['api_blocks.resolved'] != 0:
        block_value = insert['api_blocks.value']
    else:
        # Try looking for the block result. If no block result is available,
        # immediately (while under lock) create new block
        try:
            block_value = inserts_model.blocked_on(block_key, insert['id'])
        except BlockNotAvailable:
            # after running blocked_on another worker could potentially pick it up
            raise InsertHandlerErrorBlocked()

    # Note that fields are pre-converted
    handler.block_value = block_value
    handler.handle()

    return handler.emitted_matches, handler.emitted_blocks
