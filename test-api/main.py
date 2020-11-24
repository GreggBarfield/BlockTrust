import gzip
import json

from flask import Flask, request, g

from database import Database

app = Flask(__name__)

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "dev",
    "passwd": "4g79en0908g4ws4",
    "database": "api",
    "autocommit": True
}

@app.before_request
def before_request():
    """Per-request setup."""
    # Database
    print("receiving request")
    if getattr(g, "db", None) is None:
        g.db = Database(MYSQL_CONFIG)
        print("database connected")

@app.route('/', methods=["GET", "POST"])
def serve_index():
    return "This website is for robots only!", 404

@app.route('/api', methods=["POST"])
def serve_api():
    print("routed to api")
    # Decode the data

    data = None
    if request.headers.get('content-encoding', None) is not None:
        print("decompressing")
        gzip_data = gzip.decompress(request.data)
        print("decoding")
        gzip_data_decoded = gzip_data.decode()
        print("freeing gzip_data")
        gzip_data = None
        print("loading json")
        data = json.loads(gzip_data_decoded)
        print("freeing gzip_data_decoded")
        gzip_data_decoded = None

    else:
        data = json.loads(request.data)

    # Check target
    assert data["target"] == "BlockTrust Network Ingestion API"
    
    # Check version
    version = list(map(int, data["version"].split('.')))
    assert version[0] == 1

    # Check account
    allowed = [
        (12345, "We’ll provide this later"),
        (582, "5yg9h9ensyvhgfw8734tyj")
    ]
    if (data["account"], data["token"]) not in allowed:
        return "", 403
    for action in data["actions"]:
        rows = action["data"]["values"]
        left = 0
        size = 5000
        right = 0
        while left < len(rows):
            print(left, "/", len(rows))
            right = left + size
            if right > len(rows):
                right = len(rows)

            ss = []

            for row in rows[left:right]:
                ss += (
                    data["account"],
                    action["data"]["namespace"],
                    action["data"]["type"],
                    json.dumps(action["data"]["fields"]),
                    json.dumps(row)
                )

            g.db.execute(
                "INSERT INTO inserts (account, namespace, type, fields, row) VALUES " + 
                ",".join(["(%s, %s, %s, %s, %s)" for i in range(right - left)]),
                ss
            )

            left = right

    print("sent to db")

    # All-good
    print("api good")
    return "", 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=80
    )
