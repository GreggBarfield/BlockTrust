import argparse
from csv import DictReader
import json
from ..embedded.upload_generator import upload_generator


# Note that the created field does not get migrated
# Full read into ram


def process(file, account, token, endpoint):
    if 'http' not in endpoint:
        print("Please include the http:// or https:// in the endpoint.")
        exit()

    print("Uploading", file)

    csv_file = open(file)

    batches = {}

    for line in DictReader(csv_file):
        if line['account'] != str(account):
            print("Account mismatch", line)
            exit()


        if (
            line["row"].strip() == '' or
            line["fields"][0] == "\"" or
            line["fields"][-1] == "\"" or
            line["row"][0] == "\"" or
            line["row"][-1] == "\""
        ):
            print("Skipping A", line)
            continue


        line["fields"] = json.loads(line["fields"])
        line["row"] = json.loads(line["row"])

        if isinstance(line["row"], str) or len(line["fields"]) != len(line["row"]):
            print("Skipping B", line)
            continue

        t = (line["namespace"], line["type"])

        if t in batches:
            batches[t].append(line)
        else:
            batches[t] = [line]

    for value in batches.values():
        g = [value[0]["fields"]]
        g += [line["row"] for line in value]
        upload_generator(
            generator=(
                (
                    a for a in g
                )
            ),
            insert_namespace=value[0]["namespace"],
            insert_type=value[0]["type"],
            account=int(value[0]["account"]),
            token=token,
            endpoint=endpoint
        )

    csv_file.close()

    print("Finished uploading")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload an old format CSV to the API.')

    parser.add_argument('--file', help='Path to the CSV file', type=str, required=True)
    parser.add_argument('--account', help='Account ID', type=int, required=True)
    parser.add_argument('--token', help='Account token', type=str, required=True)
    parser.add_argument('--endpoint', help='Full URL to the endpoint', type=str, required=True)

    args = parser.parse_args()

    process(
        file=args.file,
        account=args.account,
        token=args.token,
        endpoint=args.endpoint
    )
