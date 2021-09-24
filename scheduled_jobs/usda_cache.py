import json
from core.database.tables.error_logs import ErrorLogs
import traceback

class UsdaDataCache:
    """Class that gets the state and city data cached so frontend response
    time will be much faster"""

    def __init__(self, db):
        self._db = db

    def cache_states(self):
        data = {}
        changed = False
        with open('./core/tools/other/market_data_cache.json', 'r+') as json_file:
            data = json.load(json_file)

            db_data = self._db.usda_reports.get_all_states()

            for item in db_data:
                if item['market_location_state'] not in data['states']:
                    data['states'].append(item['market_location_state'])
                    changed = True
                    print("USDACache: Added state: " + str(item))
            
            if changed:
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate() # deletes previous data in file

    def cache_cities(self):
        data = {}
        changed = False
        with open('./core/tools/other/market_data_cache.json', 'r+') as json_file:
            data = json.load(json_file)

            states = self._db.usda_reports.get_all_states()

            # Go through each state and get all cities
            for state in states:
                state = state['market_location_state']
                db_data = self._db.usda_reports.get_all_city_by_state(state)

                for item in db_data:
                    if state not in data['cities_per_state']:
                        data['cities_per_state'][state] = {}
                        changed = True

                    if item['slug_id'] not in data['cities_per_state'][state]:
                        data['cities_per_state'][state][item['slug_id']] = item
                        changed = True
                        print("USDACache: Added city: " + str(item))
            
            if changed:
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate() # deletes previous data in file


def get_cached_data(db):
    try:
        cacher = UsdaDataCache(db)
        cacher.cache_states()
        cacher.cache_cities()
    except Exception as e:
        ErrorLogs(db).insert_error_log("USDA Data Cacher", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        db.close()


if __name__ == "__main__":
    get_cached_data()