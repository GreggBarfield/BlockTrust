from flask import g
from ....reports.query_types import sustainability_averages


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(sustainability_averages.create())
    if row is not None:
        return row['result']
    return None