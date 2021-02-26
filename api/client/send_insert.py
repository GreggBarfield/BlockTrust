import requests
import json
import gzip


TARGET = "BlockTrust Network Ingestion API"
VERSION = "1.4.3"


class SendInsertException(Exception):
    pass


def send_insert(
    endpoint, account, token, insert_namespace, insert_type, fields, values
):
    assert isinstance(fields, (tuple, list))
    assert isinstance(values, (tuple, list))
    for value in values:
        assert isinstance(value, (tuple, list))
    assert isinstance(account, int)
    assert isinstance(token, str)

    message = {
        "target": TARGET,
        "version": VERSION,
        "account": account,
        "token": token,
        "actions": [
            {
                "action": "Insert",
                "data": {
                    "namespace": insert_namespace,
                    "type": insert_type,
                    "fields": fields,
                    "values": values
                }
            }
        ]
    }

    r = requests.post(
        url=endpoint,
        headers={
            "Content-Encoding": "gzip"
        },
        data=gzip.compress(json.dumps(message).encode())
    )
    if r.status_code != 200:
        raise SendInsertException("Send insert failed: " + r.text)
