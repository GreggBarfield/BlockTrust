from ...match_types import match_types_by_name


TYPE_NAME = "count_distribution_global"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    return {
        "count_distribution": db.matches.get_count_distribution_global(
            match_types_by_name[params["match_type"]]
        )
    }


def accessible():
    """Checks whether the query is accessible by an account.

    Returns:
        True
    """
    return True


def create(match_type):
    """Creates a query.

    Params:
        match_type: The match type name

    Returns:
        A query dictionary
    """
    return {
        'type': TYPE_NAME,
        'params': {
            'match_type': match_type
        }
    }
