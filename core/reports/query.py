from .query_types import types

from ..common_exceptions import ExportException, DebugException


def execute_query(db, query):
    """Executes a report query.

    Params:
        db: A Database object
        query: The query (dictionary)

    Returns:
        A dictionary, the result.
    """
    if 'type' not in query:
        raise ExportException("'type' is missing from query")

    if 'params' not in query:
        raise ExportException("'params' is missing from query")

    if query['type'] not in types:
        raise ExportException("type unrecognized: " + query['type'])

    return types[query['type']].execute(db, query)
