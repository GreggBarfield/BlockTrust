from urllib.request import urlopen, Request
from urllib.error import HTTPError
from traceback import print_exc
import json
from dateutil import parser
from hashlib import sha256
from ...config import BLOCKCHAIN_ENDPOINT, BLOCKCHAIN_UPLOADS


def transmit(hashes):
    """Transmits hashes to the blockchain.

    Returns:
        String, 64-character record ID (transaction ID?). Or None if uploads are switched off
    """
    if BLOCKCHAIN_UPLOADS:
        try:
            res = urlopen(Request(
                BLOCKCHAIN_ENDPOINT + "/api/add-record",
                data=json.dumps(
                    {
                        "data": hashes
                    }
                ).encode(),
                headers={
                    "Content-Type": "application/json"
                }
            ))
        except HTTPError as e:
            print_exc()
            print("START HTTP ERROR", e.read(), "END HTTP ERROR")
            raise RuntimeError("Failed to transmit hashes: " + str(e))

        if res.status != 200:
            raise RuntimeError("Failed to transmit hashes!")

        result = json.loads(res.read().decode())

        assert result["record"]["data"] == hashes
        assert len(result["record"]["id"]) == 64
        return result["record"]["id"]
    else:
        return None


def check(match_hash, record_id):
    """Checks if a hash is present in the configured blockchain.

    Params:
        match_hash: The hash to check for
        record_id: The record ID to use during the lookup

    Returns:
        datetime.datetime, the time it was entered in the blockchain, or False
    """
    res = urlopen(Request(
        "http://" + BLOCKCHAIN_ENDPOINT + "/api/get-record/" + record_id
    ))

    if res.status != 200:
        raise RuntimeError("Failed to retrieve record!")

    result = json.loads(res.read().decode())
    date = parser.parse(result["result"]["created"])

    for _hash in result["result"]["data"]:
        if _hash == match_hash:
            return date

    return False


def generate_bc_hash(dict):
    """Generates the blockchain hash, overriding internal value.

    Returns:
        The hash.
    """

    for key in tuple(dict.keys()):
        value = dict[key]
        if value is None:
            del dict[key]

    bc_hash = sha256(json.dumps(
        dict,
        sort_keys=True,
        separators=(',', ':'),
        indent=0
    ).encode()).hexdigest().lower()

    return bc_hash
