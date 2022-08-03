TYPE_NAME = "sustainability_response_averages"


def execute(db, query):
    """Execute the query."""
    params = query['params']
    sustainability_response_averages = db.sustainability_responses.get_sustainability_response_averages()
    result = {
        "air_average": float(sustainability_response_averages["air_average"]),
        "land_average": float(sustainability_response_averages["land_average"]),
        "water_average": float(sustainability_response_averages["water_average"]),
        "animal_average": float(sustainability_response_averages["animal_average"]),
        "safety_average": float(sustainability_response_averages["safety_average"]),
        "efficiency_average": float(sustainability_response_averages["efficiency_average"]),
        "improvement_average": float(sustainability_response_averages["improvement_average"]),
    }
    return {
        'sustainability_response_averages': result
    }


def create():
    """Creates a query.

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {}
    }
