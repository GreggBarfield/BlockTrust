from ..const.zip_codes_data import ZIP_CODES
from ..const.spatial_math import distance, miles_to_meters

class ZIPCodesException(Exception):
    """ZIPCodes generic exception."""

    def __init__(self, reason):
        """Constructor for ZIPCodesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class ZIPCodes:

    def __init__(self, db):
        self._db = db

    def zips_nearby_zip(self, zip_code, dist):
        """Gets ZIP codes nearby a ZIP code.

        Important: the given ZIP code will always be returned.

        Params:
            zip: The origin ZIP code
            dist: The distance to search within (radius, miles)
        """
        results = []

        for itr_zip_code in ZIP_CODES:
            if distance(ZIP_CODES[itr_zip_code]["ecef"], ZIP_CODES[zip_code]["ecef"]) < miles_to_meters(dist):
                results.append(itr_zip_code)

        if zip_code not in results:
            results.append(zip_code)
        
        return results
