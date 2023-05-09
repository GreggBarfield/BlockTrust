from ...match_types import MATCH_TYPES_NAME_TO_ID


TYPE_NAME = "count_distribution"


def execute(db, query):
    """Execute the query. Used by report worker"""
    params = query['params']
    is_partner = params.get("is_partner", False)

    if params.get("match_type", None):
        return {
            "count_distribution": db.matches.get_count_distribution(
                MATCH_TYPES_NAME_TO_ID[params["match_type"]],
                account_id=params['account'],
                is_partner=is_partner
            )
        }
    else:
        partner_account_links = db.account_links.get_account_links(partner_account=params['account'],
                                                                   account_is_not_null=True)
        return {
            "count_distribution": db.matches.get_count_distribution(
                is_partner=True,
                partner_account_links=partner_account_links
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


def create(account_id, match_type=None, is_partner=False):
    """Creates a query.

    Params:
        account_id: The account ID to get cows associated with
        match_type: The match type name to generate distribution data on
        is_partner: whether the account is a partner or not.
    Returns:
        The query dictionary
    """
    params = {'account': account_id}
    if match_type:
        params['match_type'] = match_type
    if is_partner:
        params['is_partner'] = True
    return {
        'type': TYPE_NAME,
        'params': params
    }
