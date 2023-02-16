TYPE_NAME = "count_eid_distinct_by_account"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    account_link_id = db.account_links.get_account_links(account_id=params['account'])[0]["id"]
    return {
        'count_eid_distinct': db.matches.get_count_eid_distinct_by_account(params['account']),
        'count_eid_distinct_sighted': db.matches.get_sightings_in_auction_house_feedlot_packer_stocker(
            account_link_id, as_count=True
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


def create(account_id):
    """Creates a query.

    Params:
        account_id: The account ID

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {
            'account': account_id
        }
    }
