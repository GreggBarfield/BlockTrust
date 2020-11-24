import requests
import json
import gzip
URL = "https://api.dev.blocktrustnetwork.com/api"
data = {
    "target": "BlockTrust Network Ingestion API",
    "version": "1.4.3",
    "account": 582,
    "token": "5yg9h9ensyvhgfw8734tyj",
    "actions": [
        {
            "action": "Insert",
            "data": {
                "namespace": "MFA",
                "type": "treatment",
                "fields":
                    ["electronic","a", "b","end_time"],
                "values": [
                    [i, i/2, hex(i), hex(int(i/2))]
                    for i in range(10000)
                ]
            }
        }
    ]
}
encoded = json.dumps(data).encode()
compressed = gzip.compress(encoded)
print("Encoded:", len(encoded) / (1000 * 1000))
print("Compressed:", len(compressed) / (1000 * 1000))
print(requests.post(
    url=URL,
    data=compressed,
    headers={
        'Content-Encoding': 'gzip'
    }
))
