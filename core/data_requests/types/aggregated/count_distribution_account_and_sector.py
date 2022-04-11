from flask import g
from ....reports.query_types import count_distribution_account_and_sector


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(
        count_distribution_account_and_sector.create(g.account.id(), params['sector_id'])
    )
    if row is not None:
        return row['result']
    return None
