from .data.zip_codes_data import ZIP_CODES
from .spatial_math import distance, miles_to_meters
from ..common_exceptions import ExportException
from pyzipcode import ZipCodeDatabase


def get_lat_lon(zip_code):

    """Gets the lattitude and longitude for a zip code.

    Params:
        zip_code: The zip code (integer)

    Returns:
        Tuple float (lat, lon)

    """

    if zip_code not in ZIP_CODES:
        raise ExportException("ZIP Code not recognized.")

    return ZIP_CODES[zip_code]["lat"], ZIP_CODES[zip_code]["lon"]

def zips_nearby_zip(zip_code, dist):
    """Gets ZIP codes nearby a ZIP code.

    Important: the given ZIP code will always be returned.

    Params:
        zip: The origin ZIP code
        dist: The distance to search within (radius, miles)
    """
    results = []

    if zip_code not in ZIP_CODES:
        raise ExportException(f"ZIP Code not recognized: {zip_code}")

    for itr_zip_code in ZIP_CODES:
        if distance(ZIP_CODES[itr_zip_code]["ecef"], ZIP_CODES[zip_code]["ecef"]) < miles_to_meters(dist):
            results.append(itr_zip_code)

    if zip_code not in results:
        results.append(zip_code)

    return results

def get_locations(zip_code):    
    zcdb = ZipCodeDatabase()
    info = zcdb[zip_code]
    result = info.city+","+info.state
    return result

def does_zip_exist(zip_code):
    if zip_code in ZIP_CODES:
        return True
    return False
