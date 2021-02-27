import argparse
import importlib
import os
from .process_csv import process

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a CSV to the API.')

    parser.add_argument('--profile', help='Profile name', type=str, required=True)
    parser.add_argument('--memory', help='Memory file path (must already be made)', type=str, required=True)
    parser.add_argument('--working', help='Working directory', type=str, required=True)
    parser.add_argument('-a', '--analyze', help='Only generate orders', action='store_true')
    # Note that it will be marked as processed even if move fails
    parser.add_argument('-m', '--move', help='Move destination (optional) (only moves those not processed yet)', type=str, default=None)

    args = parser.parse_args()

    profile = importlib.import_module(args.profile)

    profile.setup(args.memory)

    file_names = os.listdir(args.working)

    print("File names:", file_names)

    orders = profile.get_orders(file_names)

    print("Received", len(orders), "orders")
    print("Orders:", orders)

    if args.analyze:
        print("Set to analyze only, exiting")
        exit()

    print("Running orders")

    for order in orders:
        print("Running order", order)
        profile.cb_running(order)
        full = os.path.join(args.working, order["File Name"])
        process(
            file=full,
            insert_namespace=order["Insert Namespace"],
            insert_type=order["Insert Type"],
            account=order["Account"],
            token=order["Token"],
            endpoint=order["Endpoint"]
        )
        profile.cb_processed(order)
        if args.move is not None:
            full2 = os.path.join(args.move, order["File Name"])
            print("Renaming", full, "to", full2)
            os.rename(full, full2)

    print("Finished orders")
