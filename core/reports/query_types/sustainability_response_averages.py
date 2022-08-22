from ...database.tables.sustainability_responses import SustainabilityResponses
from ...sectors import sectors_by_name

TYPE_NAME = "sustainability_response_averages"


def execute(db, query):
    """Execute the query."""

    cow_calf_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Cow-Calf"])
    feedlot_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Feedlot"])
    auction_house_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Auction House"])
    packer_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Packer"])

    result = {
        "Cow-Calf": {
            "air_average": float(cow_calf_sustainability_response_averages["air_average"])  if cow_calf_sustainability_response_averages["air_average"] else 0,
            "land_average": float(cow_calf_sustainability_response_averages["land_average"])  if cow_calf_sustainability_response_averages["land_average"] else 0,
            "water_average": float(cow_calf_sustainability_response_averages["water_average"])  if cow_calf_sustainability_response_averages["water_average"] else 0,
            "animal_average": float(cow_calf_sustainability_response_averages["animal_average"])  if cow_calf_sustainability_response_averages["animal_average"] else 0,
            "safety_average": float(cow_calf_sustainability_response_averages["safety_average"])  if cow_calf_sustainability_response_averages["safety_average"] else 0,
            "efficiency_average": float(cow_calf_sustainability_response_averages["efficiency_average"])  if cow_calf_sustainability_response_averages["efficiency_average"] else 0,
            "improvement_average": float(cow_calf_sustainability_response_averages["improvement_average"])  if cow_calf_sustainability_response_averages["improvement_average"] else 0
        },
        "Feedlot": {
            "air_average": float(feedlot_sustainability_response_averages["air_average"]) if feedlot_sustainability_response_averages["air_average"] else 0,
            "land_average": float(feedlot_sustainability_response_averages["land_average"]) if feedlot_sustainability_response_averages["land_average"] else 0,
            "water_average": float(feedlot_sustainability_response_averages["water_average"]) if feedlot_sustainability_response_averages["water_average"] else 0,
            "animal_average": float(feedlot_sustainability_response_averages["animal_average"]) if feedlot_sustainability_response_averages["animal_average"] else 0,
            "safety_average": float(feedlot_sustainability_response_averages["safety_average"]) if feedlot_sustainability_response_averages["safety_average"] else 0,
            "efficiency_average": float(feedlot_sustainability_response_averages["efficiency_average"]) if feedlot_sustainability_response_averages["efficiency_average"] else 0,
            "improvement_average": float(feedlot_sustainability_response_averages["improvement_average"]) if feedlot_sustainability_response_averages["improvement_average"] else 0
        },
        "Auction House": {
            "water_average": float(auction_house_sustainability_response_averages["water_average"]) if auction_house_sustainability_response_averages["water_average"] else 0,
            "animal_average": float(auction_house_sustainability_response_averages["animal_average"]) if auction_house_sustainability_response_averages["animal_average"] else 0,
            "safety_average": float(auction_house_sustainability_response_averages["safety_average"]) if auction_house_sustainability_response_averages["safety_average"] else 0,
            "improvement_average": float(auction_house_sustainability_response_averages["improvement_average"]) if auction_house_sustainability_response_averages["improvement_average"] else 0
        },
        "Packer": {
            "air_average": float(packer_sustainability_response_averages["air_average"]) if packer_sustainability_response_averages["air_average"] else 0,
            "land_average": float(packer_sustainability_response_averages["land_average"]) if packer_sustainability_response_averages["land_average"] else 0,
            "water_average": float(packer_sustainability_response_averages["water_average"]) if packer_sustainability_response_averages["water_average"] else 0,
            "animal_average": float(packer_sustainability_response_averages["animal_average"]) if packer_sustainability_response_averages["animal_average"] else 0,
            "safety_average": float(packer_sustainability_response_averages["safety_average"]) if packer_sustainability_response_averages["safety_average"] else 0,
            "efficiency_average": float(packer_sustainability_response_averages["efficiency_average"]) if packer_sustainability_response_averages["efficiency_average"] else 0,
            "improvement_average": float(packer_sustainability_response_averages["improvement_average"]) if packer_sustainability_response_averages["improvement_average"] else 0
        }
    }
    return result


def create():
    """Creates a query.

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {}
    }
