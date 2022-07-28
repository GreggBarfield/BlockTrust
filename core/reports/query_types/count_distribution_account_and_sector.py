TYPE_NAME = "count_distribution_account_and_sector"


def execute(db, query):
    """Execute the query."""
    account_id = query['params']['account_id']
    result = db.matches.get_count_distribution_for_account_across_sector(account_id=account_id,
                                                                         sector_id=int(query['params']['sector_id']))
    return result


def create(account_id, sector_id):
    """Creates a query.
    Params:
        account_id: the account for which we are generating the report
        sector_id: the sector accounts which the report should contain
    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {
            'account_id': account_id,
            'sector_id': sector_id
        }
    }
