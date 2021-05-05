from time import sleep
from .exceptions import ExecutionException
from core.reports.query import execute_query
from core.common_exceptions import ExportException
from core.utilities.blockchain.transmit import transmit
from core.config import (
    BLOCKCHAIN_TRANSLATION_WORKER_UPLOADS,
    BLOCKCHAIN_RECOMMENDED_BATCH_SIZE
)
from .insert_handler import (
    InsertHandlerErrorBadType,
    InsertHandlerErrorBlocked,
    handle_insert
)


def _get_batch(
    db,
    inserts_model,
    verbose,
    insert_id,
    blockchain_recommended_batch_size
):
    batch_insert_ids = []
    batch_emitted_matches = []
    batch_emitted_blocks = []

    for batch_i in range(blockchain_recommended_batch_size):

        # Find insert
        if insert_id is not None:
            insert = inserts_model.get_by_id(insert_id)
        else:
            insert = inserts_model.get_next()

        # If no insert found, then end the batch
        if insert is None:
            if insert_id is not None and verbose:
                print("Failed to find the insert!")
            break

        print("Running insert", insert['id'])

        # Gather matches and blocks
        try:
            emitted_matches, emitted_blocks = handle_insert(db, inserts_model, insert)
            batch_emitted_matches += emitted_matches
            batch_emitted_blocks += emitted_blocks
            batch_insert_ids += [insert["id"]]
        except InsertHandlerErrorBadType as e:
            inserts_model.set_status(insert['id'], "Bad Type")
        except InsertHandlerErrorBlocked as e:
            inserts_model.set_status(insert['id'], "Blocked")
        except ExecutionException as e:
            inserts_model.set_status(insert['id'], "Exception")

            if verbose:
                print("ExecutionException", str(e))

        # End batch immediately if doing a single ID lookup
        if insert_id is not None:
            break

    return batch_insert_ids, batch_emitted_matches, batch_emitted_blocks


def _submit_batch(
    db,
    inserts_model,
    batch_insert_ids,
    batch_emitted_matches,
    batch_emitted_blocks,
    verbose,
    blockchain_uploads
):
    # Batch not empty?
    if batch_insert_ids:
        if verbose:
            print("Submitting batch", batch_insert_ids)

        if batch_emitted_matches:
            hashes = [
                match.generate_bc_hash()
                for match in batch_emitted_matches
            ]

            bc_record = None
            if blockchain_uploads:
                bc_record = transmit(hashes)

            for match in batch_emitted_matches:
                match.bc_record = bc_record
                db.matches.insert_match_object(match)

        for emitted_block in batch_emitted_blocks:
            key, value = emitted_block
            inserts_model.emit_block(key, value)

        for insert_id in batch_insert_ids:
            inserts_model.set_status(insert_id, "Done")

    else:
        if verbose:
            print("Empty batch")


def run(
    db,
    inserts_model,
    verbose=False,
    insert_id=None,
    blockchain_uploads=BLOCKCHAIN_TRANSLATION_WORKER_UPLOADS,
    blockchain_recommended_batch_size=BLOCKCHAIN_RECOMMENDED_BATCH_SIZE
):
    """Starts the translation worker.

    Params:
        db: A Database object
    """

    if blockchain_recommended_batch_size <= 0:
        raise ValueError("Blockchain recommended batch size should be at least 1")

    # Main loop
    while True:
        batch_insert_ids, batch_emitted_matches, batch_emitted_blocks = _get_batch(
            db=db,
            inserts_model=inserts_model,
            verbose=verbose,
            insert_id=insert_id,
            blockchain_recommended_batch_size=blockchain_recommended_batch_size
        )

        _submit_batch(
            db=db,
            inserts_model=inserts_model,
            verbose=verbose,
            batch_insert_ids=batch_insert_ids,
            batch_emitted_matches=batch_emitted_matches,
            batch_emitted_blocks=batch_emitted_blocks,
        )

        # No infinite loop if single insert
        if insert_id is not None:
            break

        if not batch_insert_ids:
            print("Sleeping")
            sleep(10)
