from flask import g
from ....common_exceptions import ExportException
from ....match_types import match_types_by_name


def unauth(params):
    return auth(params)


def auth(params):
    if 'account' in params and params['account'] is not None:
        raise ExportException("account none null not implemented")
        # WARNING: visibility system not set up here

    account_user = g.db.account_users.get_by_user_and_account_id(
        g.user,
        g.account.id()
    )
    account = account_user.account()
    account_links = account.account_links()

    if len(account_links) == 0:
        return {"count_distribution": []}

    return {
        "count_distribution": g.db.matches.get_count_distribution(
            match_types_by_name[params["match_type"]],
            account_links=account_links
        )
    }
