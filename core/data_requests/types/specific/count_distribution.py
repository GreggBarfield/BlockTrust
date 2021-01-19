from flask import g
from ....common_exceptions import ExportException
from ....reports.query_types import count_distribution


def unauth(params):
    return auth(params)


def auth(params):
    if 'account' in params and params['account'] is not None:
        raise ExportException("account none null not implemented")
        # WARNING: visibility system not set up here

    row = g.db.reports.get_ready_by_query(
        count_distribution.create(
            g.account.id(),
            params['match_type']
        )
    )
    if row is not None:
        return row['result']
    return None
