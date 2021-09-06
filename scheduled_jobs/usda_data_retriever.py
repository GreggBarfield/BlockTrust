import requests

from core.config import (USDA_API_KEY, USDA_MANDATORY_ENDPOINT,
                      USDA_PUBLIC_ENDPOINT)
from core.database.objects.usda_report import USDAReport
from core.database.tables.usda_reports import USDAReports
from core.database.tables.error_logs import ErrorLogs
import traceback


class UsdaDataRetriever:
    """Class that gets the Data from the USDA APIs and adds them to the database"""

    def __init__(self, db):
        self._db = db

    def get_mandatory_reports(self):
        """Gets the 'mandatory reports' from API and adds to database"""

        response = requests.get(USDA_MANDATORY_ENDPOINT, auth=(USDA_API_KEY, ''))
        json_response = response.json()

        cattleReports = dict()
        published_dates = self._db.usda_reports.get_all_published_dates()
        
        for row in json_response:
            if 'Cattle' in row['market_types'][0]:
                item = {
                    'published_date' : row['published_date'],
                    'slug_id' : int(row['slug_id'])
                    }
                if published_dates is None:
                    cattleReports[row['slug_id']] = row
                elif item not in published_dates:
                    cattleReports[row['slug_id']] = row

        print("Size of unique new cattle reports: " + str(len(cattleReports)))

        for item in cattleReports:
            response = requests.get(USDA_MANDATORY_ENDPOINT + str(item) + '/Detail', 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            if 'message' in json_response:
                print('Got smaller data for: ' + str(item))
                response = requests.get(USDA_MANDATORY_ENDPOINT + str(item), 
                    auth=(USDA_API_KEY, ''))
                json_response = response.json()

            print("Size of cattle report id " + str(item) 
                + ": " + str(len(json_response['results'])))

            for row in json_response['results']:
                try:
                    report = USDAReport(row)
                    self._db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)

    def get_public_reports(self):
        """Gets the public report data from API and adds it to the database"""
        # query market type for livestock. Should give 500ish results
        marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]

        reports = dict()
        published_dates = self._db.usda_reports.get_all_published_dates()
        for id in marketTypeIDs:
            response = requests.get(USDA_PUBLIC_ENDPOINT + 'marketTypes/' + str(id), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            for row in json_response['results']:
                item = {
                    'published_date' : row['published_date'],
                    'slug_id' : int(row['slug_id'])
                    }

                if published_dates is None:
                    reports[row['slug_id']] = row
                elif item not in published_dates:
                    reports[row['slug_id']] = row
        
        print("Size of unique new reports: " + str(len(reports)))

        for item in reports:
            response = requests.get(USDA_PUBLIC_ENDPOINT + 'reports/' + str(item), auth=(USDA_API_KEY, ''))
            json_response = response.json()

            print("Size of report id " + str(item) + ": " + str(len(json_response['results'])))

            for row in json_response['results']:
                try:
                    report = USDAReport(row)
                    self._db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)


def get_usda_data(db):
    try:
        retriever = UsdaDataRetriever(db)
        retriever.get_public_reports()
        retriever.get_mandatory_reports()
    except Exception as e:
        ErrorLogs(db).insert_error_log("USDA Data Retreiver", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        db.close()


if __name__ == "__main__":
    get_usda_data()
