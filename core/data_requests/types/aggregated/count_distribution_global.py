from flask import g
from ....common_exceptions import ExportException
from ....reports.query_types import count_distribution_global


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(
        count_distribution_global.create(params['match_type'])
    )
    if row is not None:
        return row['result']
    return None
