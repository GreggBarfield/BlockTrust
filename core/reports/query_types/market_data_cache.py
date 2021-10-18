TYPE_NAME = "market_data_cache"


def execute(db, query):
    """Gets all the states and cities per state."""
    data = {
        "states": [],
        "cities_per_state": {}
    }
    states = db.usda_reports.get_all_states()
    data['states'] = states

    # Go through each state and get all cities
    for state in states:
        state = state['market_location_state']
        db_data = db.usda_reports.get_all_city_by_state(state)

        for item in db_data:
            if state not in data['cities_per_state']:
                data['cities_per_state'][state] = {}

            if item['slug_id'] not in data['cities_per_state'][state]:
                data['cities_per_state'][state][item['slug_id']] = item

    return data


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
