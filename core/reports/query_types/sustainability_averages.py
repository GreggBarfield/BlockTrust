from ...sectors import sectors_by_id

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
        data = db.sustainability.get_sustainability_totals_by_sector(sectorID)[0]
        print(data)

        sectorTotals = {
            "excellent": 0,
            "acceptable": 0,
            "needsWork": 0
        }

        if data["total_excellent_score"] != None:
            sectorTotals = {
                "excellent": int(data["total_excellent_score"]), 
                "acceptable": int(data["total_acceptable_score"]),
                "needsWork": int(data["total_needsWork_score"])
            }

            allSectorTotals["excellent"] += int(data["total_excellent_score"])
            allSectorTotals["acceptable"] += int(data["total_acceptable_score"])
            allSectorTotals["needsWork"] += int(data["total_needsWork_score"])

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
