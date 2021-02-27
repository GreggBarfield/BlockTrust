import logging
import datetime
from api.client.send_insert import send_insert


BATCH_SIZE = 10000


class UploadGeneratorException(Exception):
    pass


def upload_generator(generator, insert_namespace, insert_type, account, token, endpoint):
    """Upload a generator to the API.

    Params:
        generator: A generator of tuples. The first row will be the fields.
        insert_namespace: The insert namespace
        insert_type: The insert type
        account: The Account ID
        token: The Account token
        endpoint: The endpoint URL
    """
    fields = next(generator)

    if len(fields) == 0:
        raise UploadGeneratorException("First row is empty")

    rows = []
    total = 0

    def send_rows():
        nonlocal rows, total
        print(
            "Uploading {rows} rows ({prior} prior) ({at})".format(
                rows=len(rows),
                prior=total,
                at=datetime.datetime.now().ctime()
            )
        )

        if len(rows) != 0:
            send_insert(
                endpoint=endpoint,
                account=account,
                token=token,
                insert_namespace=insert_namespace,
                insert_type=insert_type,
                fields=fields,
                values=rows
            )
        total += len(rows)
        rows = []

    for row in generator:
        if len(row) == 0 or len(row) == 1 and row[0] == "":
            continue
        if len(row) != len(fields):
            raise UploadGeneratorException(
                "Row does not match fields: " + str(row)
            )
        rows.append(row)
        if len(rows) == BATCH_SIZE:
            send_rows()

    send_rows()

    print("Uploaded", total, "rows")
