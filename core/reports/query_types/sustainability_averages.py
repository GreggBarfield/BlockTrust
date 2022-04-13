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

        sectorTotals = {
            "excellent": 0,
            "acceptable": 0,
            "needsWork": 0
        }

        # for sectors which don't have any sustainability data, all the scores would be None
        if data["total_first_score_points"] is not None:
            sectorTotals = {
                "excellent": int(data["total_first_score_points"]),
                "acceptable": int(data["total_second_score_points"]),
                "needsWork": int(data["total_third_score_points"])
            }

            allSectorTotals["excellent"] += int(data["total_first_score_points"])
            allSectorTotals["acceptable"] += int(data["total_second_score_points"])
            allSectorTotals["needsWork"] += int(data["total_third_score_points"])

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
