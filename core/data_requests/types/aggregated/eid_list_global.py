from flask import g
from ....reports.query_types import eid_list_global


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(eid_list_global.create())
    if row is not None:
        return row['result']
    return None
