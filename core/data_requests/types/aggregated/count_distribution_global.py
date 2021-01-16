from flask import g
from ....common_exceptions import ExportException
from ....reports.query_types.count_distribution_global import execute


def unauth(params):
    return auth(params)


def auth(params):
    return execute(g.db, params)
