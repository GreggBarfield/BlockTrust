from flask import g
from ....common_exceptions import ExportException
from ....reports.query_types import annual_count_distribution_by_account
from core.database.tables.reports import Reports


def unauth(params):
    return auth(params)


def auth(params):
    if 'account' in params and params['account'] is not None:
        raise ExportException("account none null not implemented")

    row = Reports(g.db).get_ready_by_query(
        annual_count_distribution_by_account.create(
            g.account.id(),
            params.get('match_type', None),
            g.account.is_partner()
        )
    )
    if row is not None:
        return row['result']
    return None