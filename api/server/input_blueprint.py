import json
import os
import gzip


from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)


from ..database.inserts_model import InsertsModel
from core.database.tables.accounts import AccountsException
from core.database.database import Database
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG
from core.common_exceptions import ExportException


bp = Blueprint('input_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route('/', methods=["GET", "POST"])
def serve_index():
    raise ExportException("Good endpoint, bad path")


@bp.route('/api', methods=["POST"])
def serve_api():
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
    account = g.db.accounts.get_account_by_id(data["account"])
    if account is not None:
        if account.token() != data["token"]:
            raise ExportException("Bad token")
    else:
        raise ExportException("Bad account ID")

    # Check for bad syntax

    for action in data["actions"]:
        rows = action["data"]["values"]

        for row in rows:
            if len(action["data"]["fields"]) != len(row):
                raise ExportException("Fields & row length mismatch")

    # Execute actions

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
                fields = {
                    key: value for key, value in zip(
                        action["data"]["fields"],
                        row
                    )
                }
                ss += (
                    data["account"],
                    action["data"]["namespace"],
                    action["data"]["type"],
                    json.dumps(fields)
                )

            sql = (
                "INSERT INTO api_inserts (account, namespace, type, fields) VALUES " +
                ",".join(["(%s, %s, %s, %s)" for i in range(right - left)])
            )
            print(sql)
            g.db.execute(
                sql, ss
            )

            left = right

    print("sent to db")

    # All-good
    print("api good")
    return "", 200
