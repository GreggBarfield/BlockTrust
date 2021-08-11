from flask import g
import requests
from ..database.tables.usda_reports import USDAReports
from ..database.objects.usda_report import USDAReport
from ..database.database import Database
from ..config import USDA_API_KEY


class UsdaDataRetriever:
    """Class that gets the Data from the USDA APIs and adds them to the database"""

    def getMandatoryReports(self):
        """Gets the 'mandatory reports' from API and adds to database"""

        API_ENDPOINT = 'https://mpr.datamart.ams.usda.gov/services/v1.1/reports/'
        response = requests.get(API_ENDPOINT, auth=(USDA_API_KEY, ''))
        json_response = response.json()

        cattleReports = dict()
        for item in json_response:
            if 'Cattle' in item['market_types'][0]:
                cattleReports[item['slug_id']] = item

        print("Size of unique cattle reports: " + str(len(cattleReports)))

        for item in cattleReports:
            response = requests.get(API_ENDPOINT + str(item) + '/Detail', 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            if 'message' in json_response:
                print('Got smaller data for: ' + str(item))
                response = requests.get(API_ENDPOINT + str(item), 
                    auth=(USDA_API_KEY, ''))
                json_response = response.json()

            print("Size of cattle report id " + str(item) 
                + ": " + str(len(json_response['results'])))

            for row in json_response['results']:
                try:
                    report = USDAReport(row)
                    g.db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)

    def getPublicReports(self):
        """Gets the public report data from API and adds it to the database"""
        # query market type for livestock. Should give 500ish results
        marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]
        API_ENDPOINT = 'https://marsapi.ams.usda.gov/services/v1.2/'

        reports = dict()
        for id in marketTypeIDs:
            response = requests.get(API_ENDPOINT + 'marketTypes/' + str(id), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            for row in json_response['results']:
                reports[row['slug_id']] = row
        
        print("Size of unique reports: " + str(len(reports)))

        for item in reports:
            response = requests.get(API_ENDPOINT + 'reports/' + str(item), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            print("Size of report id " + str(item) + ": " + str(len(json_response['results'])))

            for row in json_response['results']:
                try:
                    report = USDAReport(row)
                    g.db.usda_reports.create_report(report)
                except Exception as e:
                    print(row)
                    raise Exception(e)

    def getUsdaData(self):
        """Encapsulates the different report calls and calls everything once"""
        self.getPublicReports()
        self.getMandatoryReports()


if __name__ == "__main__":
    if False:
        UsdaDataRetriever.getUsdaData()
    print("Testing, got to the main! it worked")
