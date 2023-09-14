from core.database.tables.matches import Matches
from ...match_types import MATCH_TYPES_NAME_TO_ID


TYPE_NAME = "count_distribution_global"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    return {
        "count_distribution": Matches(db).get_count_distribution_global(
            MATCH_TYPES_NAME_TO_ID[params["match_type"]]
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
