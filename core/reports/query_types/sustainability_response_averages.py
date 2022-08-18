from ...database.tables.sustainability_responses import SustainabilityResponses
from ...sectors import sectors_by_name

TYPE_NAME = "sustainability_response_averages"


def execute(db, query):
    """Execute the query."""
    sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages()
    result1 = {
        "air_average": float(sustainability_response_averages["air_average"]),
        "land_average": float(sustainability_response_averages["land_average"]),
        "water_average": float(sustainability_response_averages["water_average"]),
        "animal_average": float(sustainability_response_averages["animal_average"]),
        "safety_average": float(sustainability_response_averages["safety_average"]),
        "efficiency_average": float(sustainability_response_averages["efficiency_average"]),
        "improvement_average": float(sustainability_response_averages["improvement_average"])
    }
    cow_calf_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Cow-Calf"])
    feedlot_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Feedlot"])
    auction_house_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Auction House"])
    packer_sustainability_response_averages = SustainabilityResponses(db).get_sustainability_response_averages(sector_id=sectors_by_name["Packer"])

    result = {
        "Cow-Calf": {
            "air_average": float(cow_calf_sustainability_response_averages["air_average"]),
            "land_average": float(cow_calf_sustainability_response_averages["land_average"]),
            "water_average": float(cow_calf_sustainability_response_averages["water_average"]),
            "animal_average": float(cow_calf_sustainability_response_averages["animal_average"]),
            "safety_average": float(cow_calf_sustainability_response_averages["safety_average"]),
            "efficiency_average": float(cow_calf_sustainability_response_averages["efficiency_average"]),
            "improvement_average": float(cow_calf_sustainability_response_averages["improvement_average"])
        },
        "Feedlot": {
            "air_average": float(feedlot_sustainability_response_averages["air_average"]),
            "land_average": float(feedlot_sustainability_response_averages["land_average"]),
            "water_average": float(feedlot_sustainability_response_averages["water_average"]),
            "animal_average": float(feedlot_sustainability_response_averages["animal_average"]),
            "safety_average": float(feedlot_sustainability_response_averages["safety_average"]),
            "efficiency_average": float(feedlot_sustainability_response_averages["efficiency_average"]),
            "improvement_average": float(feedlot_sustainability_response_averages["improvement_average"])
        },
        "Auction House": {
            "air_average": float(auction_house_sustainability_response_averages["air_average"]),
            "land_average": float(auction_house_sustainability_response_averages["land_average"]),
            "water_average": float(auction_house_sustainability_response_averages["water_average"]),
            "animal_average": float(auction_house_sustainability_response_averages["animal_average"]),
            "safety_average": float(auction_house_sustainability_response_averages["safety_average"]),
            "efficiency_average": float(auction_house_sustainability_response_averages["efficiency_average"]),
            "improvement_average": float(auction_house_sustainability_response_averages["improvement_average"])
        },
        "Packer": {
            "air_average": float(packer_sustainability_response_averages["air_average"]),
            "land_average": float(packer_sustainability_response_averages["land_average"]),
            "water_average": float(packer_sustainability_response_averages["water_average"]),
            "animal_average": float(packer_sustainability_response_averages["animal_average"]),
            "safety_average": float(packer_sustainability_response_averages["safety_average"]),
            "efficiency_average": float(packer_sustainability_response_averages["efficiency_average"]),
            "improvement_average": float(packer_sustainability_response_averages["improvement_average"])
        }
    }
    print(result)
    return result1


def create():
    """Creates a query.

    Returns:
        A dictionary of the query
    """
    return {
        'type': TYPE_NAME,
        'params': {}
    }
