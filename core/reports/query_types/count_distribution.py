from ...match_types import MATCH_TYPES_NAME_TO_ID


TYPE_NAME = "count_distribution"


def execute(db, query):
    """Execute the query."""
    params = query['params']

    account = db.accounts.get_account_by_id(params['account'])
    account_links = account.account_links()

    if len(account_links) == 0:
        return {"count_distribution": []}

    return {
        "count_distribution": db.matches.get_count_distribution(
            MATCH_TYPES_NAME_TO_ID[params["match_type"]],
            account_links=account_links
        )
    }


def accessible(query, account_id):
    """Checks whether the query is accessible by an account.

    Params:
        query: The query dictionary
        account_id: The account ID of who is accessing the query
            or None if anonymous

    Returns:
        A boolean of whether the query is accessible
    """
    if account_id is None:
        return False
    return account_id == query['params']['account']


def create(account_id, match_type):
    """Creates a query.

    Params:
        account_id: The account ID to get cows associated with
        match_type: The match type name to generate distribution data on

    Returns:
        The query dictionary
    """
    return {
        'type': TYPE_NAME,
        'params': {
            'account': account_id,
            'match_type': match_type
        }
    }
