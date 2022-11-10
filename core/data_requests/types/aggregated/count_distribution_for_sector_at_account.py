from flask import g
from ....reports.query_types import count_distribution_for_sector_at_account


def unauth(params):
    return auth(params)


def auth(params):
    row = g.db.reports.get_ready_by_query(
        count_distribution_for_sector_at_account.create(g.account.id(), params['sector_id'])
    )
    if row is not None:
        return row['result']
    return None
