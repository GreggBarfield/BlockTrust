from flask import g
from ....common_exceptions import ExportException
from ....reports.query_types.count_distribution import execute


def unauth(params):
    return auth(params)


def auth(params):
    if 'account' in params and params['account'] is not None:
        raise ExportException("account none null not implemented")
        # WARNING: visibility system not set up here

    return execute(
        g.db,
        {
            'account': g.account.id(),
            'match_type': params['match_type']
        }
    )
