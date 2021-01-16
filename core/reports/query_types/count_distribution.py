from ...match_types import match_types_by_name


def execute(db, params):
    """Execute the query."""
    account = db.accounts.get_by_id(params['account'])
    account_links = account.account_links()

    if len(account_links) == 0:
        return {"count_distribution": []}

    return {
        "count_distribution": db.matches.get_count_distribution(
            match_types_by_name[params["match_type"]],
            account_links=account_links
        )
    }
