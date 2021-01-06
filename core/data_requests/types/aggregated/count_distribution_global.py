from flask import g
from ....common_exceptions import ExportException
from ....match_types import match_types_by_name


def unauth(params):
    return auth(params)


def auth(params):
    return {
        "count_distribution": g.db.matches.get_count_distribution_global(
            match_types_by_name[params["match_type"]]
        )
    }
