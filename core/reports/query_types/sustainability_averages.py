from ...sectors import sectors_by_id
import json

TYPE_NAME = "sustainability_averages"


def execute(db, query):
    """Gets the totals of all the responses for each sector"""
    results = {}

    for sectorID in sectors_by_id:
        results[sectorID] = {}
        data = db.sustainability.get_by_sector(sectorID)

        sectorTotal = {
            "excellent": 0, 
            "acceptable": 0,
            "needsWork": 0
        }

        for item in data:
            response = json.loads(item['response'])
            for type in response:
                for answer in response[type]:
                    if 'a' in answer:
                        sectorTotal['excellent'] += 1
                    elif 'b' in answer:
                        sectorTotal['acceptable'] += 1
                    elif 'c' in answer:
                        sectorTotal['needsWork'] += 1

        results[sectorID] = sectorTotal

    return results


def create():
    """Creates a query.

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {}
    }
