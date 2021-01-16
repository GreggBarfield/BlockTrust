from flask import g
from ....reports.query_types.count_eid_distinct import execute


def unauth(params):
    return auth(params)


def auth(params):
    return execute(g.db, params)
