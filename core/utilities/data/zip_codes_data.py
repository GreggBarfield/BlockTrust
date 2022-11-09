import json
import os
from ..spatial_math import lla_wgs84_to_ecef
RAW_ZIP_CODES_FILE_PATH = "./us-zip-code-latitude-and-longitude.json"
dir_path = os.path.dirname(os.path.realpath(__file__))
raw_zip_codes = json.load(open(os.path.join(dir_path,RAW_ZIP_CODES_FILE_PATH)))

ZIP_CODES = {
    int(data["fields"]["zip"]): {
        "ecef": lla_wgs84_to_ecef(data["fields"]["latitude"], data["fields"]["longitude"]),
        "lat": data["fields"]["latitude"],
        "lon": data["fields"]["longitude"]
    }
    for data in raw_zip_codes
}
