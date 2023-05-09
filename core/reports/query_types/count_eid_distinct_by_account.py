TYPE_NAME = "count_eid_distinct_by_account"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    is_partner = params.get("is_partner", False)
    return {
        'count_eid_distinct': db.matches.get_count_eid_distinct_by_account(params['account'], is_partner),
        'count_eid_distinct_sighted': db.matches.get_sightings_in_auction_house_feedlot_packer_stocker(
            params['account'], is_partner, as_count=True
        )
    }


def accessible(query, account_id):
    """Checks whether the query is accessible by an account.

    Params:
        query: The query (dictionary)
        account_id: The account ID

    Returns:
        Boolean whether query is accessible
    """
    if account_id is None:
        return False
    return query['account'] == account_id


def create(account_id, is_partner=False):
    """Creates a query.

    Params:
        account_id: The account ID

    Returns:
        A dictionary of the query
    """
    params = {'account': account_id, 'is_partner': True} if is_partner else {'account': account_id}
    return {
        'type': TYPE_NAME,
        'params': params
    }
