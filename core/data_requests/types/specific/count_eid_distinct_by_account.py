from flask import g
from ....reports.query_types import count_eid_distinct_by_account
from core.database.tables.reports import Reports


def unauth(params):
    return auth(params)


def auth(params):
    row = Reports(g.db).get_ready_by_query(
        count_eid_distinct_by_account.create(g.account.id(), g.account.is_partner())
    )
    if row is not None:
        return row['result']
    return None
