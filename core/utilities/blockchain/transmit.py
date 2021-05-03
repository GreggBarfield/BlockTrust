from urllib.request import urlopen, Request
from urllib.error import HTTPError
from traceback import print_exc
import json
from ...config import BLOCKCHAIN_ENDPOINT


def transmit(hashes):
    """Transmits hashes to the blockchain.

    Returns:
        String, 64-character record ID (transaction ID?).
    """
    try:
        res = urlopen(Request(
            "http://" + BLOCKCHAIN_ENDPOINT + "/api/add-record",
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
