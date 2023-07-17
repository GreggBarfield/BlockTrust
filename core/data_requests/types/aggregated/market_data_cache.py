from flask import g
from ....reports.query_types import market_data_cache
from core.database.tables.reports import Reports


def unauth(params):
    return auth(params)


def auth(params):
    row = Reports(g.db).get_ready_by_query(market_data_cache.create())
    if row is not None:
        return row['result']
    return None
