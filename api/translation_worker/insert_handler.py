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


def handle_insert(db, inserts_model, insert):
    """Handle an insert.

    Params:
        db: A Database object
        inserts_model: An InsertsModel object
        insert: An insert dictionary, with 'api_blocks.value' and 'api_blocks.resolved'
    """

    if (insert['namespace'], insert['type']) not in types_lookup:
        inserts_model.set_status(insert['id'], "Bad Type")
        return

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
        # immediately (while under lock) create new block and update insert
        try:
            block_value = inserts_model.blocked_on(block_key, insert['id'])
        except BlockNotAvailable:
            # blocked_on handles status
            # after running blocked_on another worker could potentially pick it up
            return

    # Note that fields are pre-converted
    handler.block_value = block_value
    handler.handle()

    # Handle any emitted matches
    if handler.emitted_matches:
        hashes = [match.generate_bc_hash() for match in handler.emitted_matches]

        bc_record = None
        if BLOCKCHAIN_TRANSLATION_WORKER_UPLOADS:
            bc_record = transmit(hashes)

        for match in handler.emitted_matches:
            match.bc_record = bc_record
            db.matches.insert_match_object(match)

    # Handle any emitted blocks
    if handler.emitted_blocks:
        for emitted_block in handler.emitted_blocks:
            key, value = emitted_block
            inserts_model.emit_block(key, value)

    inserts_model.set_status(insert['id'], "Done")
