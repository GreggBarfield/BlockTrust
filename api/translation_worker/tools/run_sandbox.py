from unittest.mock import MagicMock
from .sandbox import inserts
from ..insert_handler import handle_insert

# Note that this tool is VERY incomplete and is primarily for testing basic configuration
# translation_worker/main.py has a flag --id that is very useful for testing
# python -m api.translation_worker.tools.run_sandbox

if __name__ == "__main__":
    print("Running sandbox...")

    for insert in inserts:
        print("Running insert", insert["namespace"], insert["type"], insert["id"])

        db = MagicMock()
        inserts_model = MagicMock()

        handle_insert(db, inserts_model, insert)

        print("inserts_model:", inserts_model.mock_calls)
        print("db:", db.mock_calls)
