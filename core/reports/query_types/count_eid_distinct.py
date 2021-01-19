TYPE_NAME = "count_eid_distinct"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    return {
        'count_eid_distinct': db.matches.get_count_eid_distinct()
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
