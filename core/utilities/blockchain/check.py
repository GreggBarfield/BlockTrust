from urllib.request import urlopen, Request
from dateutil import parser
import json
from ...config import BLOCKCHAIN_ENDPOINT


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
