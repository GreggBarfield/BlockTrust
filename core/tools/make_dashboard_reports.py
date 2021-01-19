import os
import json
import random
import sys

from core.config import *  # noqa
from core.database.database import Database  # noqa

from core.reports.query_types import (
    count_distribution, count_distribution_global, count_eid_distinct,
    count_eid_distinct_by_account
)


db = Database(MYSQL_CONFIG)


def make_global():
    queries = [
        count_distribution_global.create("USDA Yield Grade"),
        count_distribution_global.create("USDA Quality Grade"),
        count_eid_distinct.create(),
    ]
    for query in queries:
        db.reports.insert_query(None, query)


def make_account(account_id):
    queries = [
        count_distribution.create(account_id, "USDA Yield Grade"),
        count_distribution.create(account_id, "USDA Quality Grade"),
        count_eid_distinct_by_account.create(account_id)
    ]

    for query in queries:
        db.reports.insert_query(None, query)


def make_accounts():
    for row in db.execute_d("SELECT id FROM accounts"):
        make_account(row['id'])


make_global()
make_accounts()
