import os
import json
import random
import sys
import argparse
from threading import Thread
import traceback

sys.path = [
    os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
] + sys.path


try:
    __name__ = "api.translation_worker.main"

    from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG  # noqa
    from .logistics import run  # noqa
    from ..database.inserts_model import InsertsModel  # noqa

    parser = argparse.ArgumentParser(description='Start an instance of the translation worker.')

    parser.add_argument('-v', '--verbose', help='Verbose', action='store_true')
    parser.add_argument('-i', '--id', help='Run ID (regardless of status) (exits after finishing)', type=int, default=None)
    parser.add_argument('-t', '--threads', help='Number of threads', type=int, default=1)

    args = parser.parse_args()

    def threaded_function():
        try:
            run(
                InsertsModel(API_MYSQL_CONFIG),
                verbose=args.verbose,
                insert_id=args.id
            )
        except BaseException as e:
            print(e, traceback.print_exc())
            print("Thread excepted, killing program")
            exit()

    threads = []
    thread_count = args.threads
    if args.id is not None:
        print("--id: forcing thread count to 1")
        thread_count = 1

    for i in range(thread_count):
        thread = Thread(target=threaded_function)
        thread.start()
        threads.append(thread)
    print("Spawned", len(threads), "threads")
    for thread in threads:
        thread.join()
except Exception as e:
    print("Translation worker", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
