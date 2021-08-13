import requests

from core.database.database import Database

from core.config import (USDA_API_KEY, USDA_MANDATORY_ENDPOINT,
                      USDA_PUBLIC_ENDPOINT, MYSQL_CONFIG)
from core.database.objects.usda_report import USDAReport
from core.database.tables.usda_reports import USDAReports


class UsdaDataRetriever:
    """Class that gets the Data from the USDA APIs and adds them to the database"""

    def __init__(self):
        super().__init__()
        self.db = Database(MYSQL_CONFIG)

    def getMandatoryReports(self):
        """Gets the 'mandatory reports' from API and adds to database"""

        response = requests.get(USDA_MANDATORY_ENDPOINT, auth=(USDA_API_KEY, ''))
        json_response = response.json()

        cattleReports = dict()
        for item in json_response:
            if 'Cattle' in item['market_types'][0]:
                cattleReports[item['slug_id']] = item

        print("Size of unique cattle reports: " + str(len(cattleReports)))

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
                    self.db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)

    def getPublicReports(self):
        """Gets the public report data from API and adds it to the database"""
        # query market type for livestock. Should give 500ish results
        marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]

        reports = dict()
        for id in marketTypeIDs:
            response = requests.get(USDA_PUBLIC_ENDPOINT + 'marketTypes/' + str(id), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            for row in json_response['results']:
                reports[row['slug_id']] = row
        
        print("Size of unique reports: " + str(len(reports)))

        for item in reports:
            response = requests.get(USDA_PUBLIC_ENDPOINT + 'reports/' + str(item), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            print("Size of report id " + str(item) + ": " + str(len(json_response['results'])))

            for row in json_response['results']:
                try:
                    report = USDAReport(row)
                    self.db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)

    def getUsdaData(self):
        """Encapsulates the different report calls and calls everything once"""
        self.getPublicReports()
        self.getMandatoryReports()


if __name__ == "__main__":
    retriever = UsdaDataRetriever()
    retriever.getUsdaData()
