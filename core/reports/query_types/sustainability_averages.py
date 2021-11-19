from ...sectors import sectors_by_id
import json

TYPE_NAME = "sustainability_averages"


def execute(db, query):
    """Gets the totals of all the responses for each sector"""
    results = {}
    allSectorTotals = {
        "excellent": 0, 
        "acceptable": 0,
        "needsWork": 0
    }
    results['allSectors'] = allSectorTotals

    for sectorID in sectors_by_id:
        results[sectorID] = {}
        data = db.sustainability.get_by_sector(sectorID)

        sectorTotals = {
            'all': {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            }
        }
        for item in data:
            response = json.loads(item['response'])
            for type in response:
                sectorTotals[type] = {
                    "excellent": 0, 
                    "acceptable": 0,
                    "needsWork": 0
                }

                for answer in response[type]:
                    if 'a' in answer:
                        sectorTotals['all']['excellent'] += 1
                        sectorTotals[type]['excellent'] += 1
                        results['allSectors']['excellent'] += 1
                    elif 'b' in answer:
                        sectorTotals['all']['acceptable'] += 1
                        sectorTotals[type]['acceptable'] += 1
                        results['allSectors']['acceptable'] += 1
                    elif 'c' in answer:
                        sectorTotals['all']['needsWork'] += 1
                        sectorTotals[type]['needsWork'] += 1
                        results['allSectors']['needsWork'] += 1

        results[sectorID] = sectorTotals

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
