from flask import g
from ....reports.query_types import count_eid_distinct_by_account


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(
        count_eid_distinct_by_account.create(g.account.id())
    )
    if row is not None:
        return row['result']
    return None
