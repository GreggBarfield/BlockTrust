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
        data = db.sustainability.get_sustainability_by_sector(sectorID)

        sectorTotals = {
            'allSections': {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            }
        }
        for item in data:
            response = json.loads(item['response'])
            for section_type in response:
                sectorTotals[section_type] = {
                    "excellent": 0, 
                    "acceptable": 0,
                    "needsWork": 0
                }

                for answer in response[section_type]:
                    if 'a' in answer:
                        sectorTotals['allSections']['excellent'] += 1
                        sectorTotals[section_type]['excellent'] += 1
                        results['allSectors']['excellent'] += 1
                    elif 'b' in answer:
                        sectorTotals['allSections']['acceptable'] += 1
                        sectorTotals[section_type]['acceptable'] += 1
                        results['allSectors']['acceptable'] += 1
                    elif 'c' in answer:
                        sectorTotals['allSections']['needsWork'] += 1
                        sectorTotals[section_type]['needsWork'] += 1
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
