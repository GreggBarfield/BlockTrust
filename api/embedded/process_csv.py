import argparse
from csv import reader
from .upload_generator import upload_generator


def process(file, insert_namespace, insert_type, account, token, endpoint):
    if 'http' not in endpoint:
        print("Please include the http:// or https:// in the endpoint.")
        exit()

    print("Uploading", file)

    csv_file = open(file)

    upload_generator(
        generator=reader(csv_file),
        insert_namespace=insert_namespace,
        insert_type=insert_type,
        account=account,
        token=token,
        endpoint=endpoint
    )

    csv_file.close()

    print("Finished uploading")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a CSV to the API.')

    parser.add_argument('--file', help='Path to the CSV file', type=str, required=True)
    parser.add_argument('--namespace', help='Insert namespace', type=str, required=True)
    parser.add_argument('--type', help='Insert type', type=str, required=True)
    parser.add_argument('--account', help='Account ID', type=int, required=True)
    parser.add_argument('--token', help='Account token', type=str, required=True)
    parser.add_argument('--endpoint', help='Full URL to the endpoint', type=str, required=True)

    args = parser.parse_args()

    process(
        file=args.file,
        insert_namespace=args.namespace,
        insert_type=args.type,
        account=args.account,
        token=args.token,
        endpoint=args.endpoint
    )
