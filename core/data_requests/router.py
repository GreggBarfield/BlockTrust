from .exceptions import (
    DataRequestMalformedException,
    DataRequestTypeUnknownException
)

from .types.aggregated import count_eid_distinct
from .types.specific import (
    count_distribution, matches_by_eids, matches_by_account,
    matches_by_auction_account
)

routing_table = {
    'count_eid_distinct': count_eid_distinct,
    'count_distribution': count_distribution,
    'matches_by_eids': matches_by_eids,
    'matches_by_account': matches_by_account,
    'matches_by_auction_account': matches_by_auction_account
}


def unauth_route(request):
    """Routes an unauthenticated request from the frontend.

    Note: it should already be confirmed by this point the user
    is logged in and has an account selected!

    Params:
        request: A dictionary of
            type: The request type
            params: A dictionary of parameters
    
    Returns:
        A dictionary of
            type: The request type
            params: The dictionary of parameters
            result: A dictionary as specified by the request type
    """

    if 'type' not in request:
        raise DataRequestMalformedException("request['type'] is missing")

    if 'params' not in request:
        raise DataRequestMalformedException("request['params'] is missing")

    if request['type'] not in routing_table:
        raise DataRequestTypeUnknownException("request type unknown")

    result = routing_table[request['type']].unauth(request['params'])

    return {
        'type': request['type'],
        'params': request['params'],
        'result': result
    }
