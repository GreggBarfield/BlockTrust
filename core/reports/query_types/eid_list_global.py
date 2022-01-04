TYPE_NAME = "eid_list_global"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    return {
        'eid_list_global': db.matches.get_distinct_eids(number_of_years=1)
    }


def accessible():
    """Checks whether the query is accessible by an account.

    Returns:
        True
    """
    return True


def create():
    """Creates a query.

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {}
    }
