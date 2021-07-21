from flask import g
import requests
from ..database.tables.usda_reports import USDAReports
from ..database.objects.usda_report import USDAReport
from ..database.database import Database
from ..config import USDA_API_KEY
from datetime import datetime


class UsdaDataRetriever:
    """Class that gets the Data from the USDA APIs and adds them to the database"""

    def __init__(self):
        super().__init__()
        self.current_year = str(datetime.today().year)
        self.last_year = str(int(self.current_year) - 1)

    def canSkipRow(self, row):
        """Checks if the row has data we care about"""
        return self.isWithinAYear(row) and self.hasData(row)

    def isWithinAYear(self, row):
        """Checks if the report_date is within a year old.

        Returns:
        True if it is younger than a year, or False if not.
        """
        if (self.last_year in row['report_date'] 
            or self.current_year in row['report_date']):
            return True
        return False

    def hasData(self, row):
        """Checks if the row has a head_count and thus more information.

        Returns:
        True if the row has data in 'head_count', or False if not.
        """
        if (row['head_count'] != None 
            and row['report_date'] != ''):
            return True
        return False

    def getMandatoryReports(self):
        """Gets the 'mandatory reports' from API and adds to database"""

        API_ENDPOINT = 'https://mpr.datamart.ams.usda.gov/services/v1.1/reports/'
        response = requests.get(API_ENDPOINT, auth=(USDA_API_KEY, ''))
        json_response = response.json()

        cattleReports = dict()
        report_dates = g.db.usda_reports.get_all_report_dates()
        for row in json_response:
            if 'Cattle' in row['market_types'][0]:
                item = {
                    'report_date' : row['report_date'],
                    'slug_id' : int(row['slug_id'])
                    }
                if item not in report_dates:
                    cattleReports[row['slug_id']] = row

        print("Size of unique new cattle reports: " + str(len(cattleReports)))

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

            count = 0
            for row in json_response['results']:
                if self.canSkipRow(row):
                    try:
                        report = USDAReport(row)
                        g.db.usda_reports.create_report(report)
                        count += 1
                    except Exception as e:
                        print(row)
                        raise Exception(e)
            
            print("Size of report id " + str(item) + " added: " + str(count))


    def getPublicReports(self):
        """Gets the public report data from API and adds it to the database"""
        # query market type for livestock. Should give 500ish results
        marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]
        API_ENDPOINT = 'https://marsapi.ams.usda.gov/services/v1.2/'

        reports = dict()
        report_dates = g.db.usda_reports.get_all_report_dates()
        for id in marketTypeIDs:
            response = requests.get(API_ENDPOINT + 'marketTypes/' + str(id), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            for row in json_response['results']:
                item = {
                    'report_date' : row['report_date'],
                    'slug_id' : int(row['slug_id'])
                    }
                
                if item not in report_dates:
                    reports[row['slug_id']] = row
        
        print("Size of unique new reports: " + str(len(reports)))

        for item in reports:
            response = requests.get(API_ENDPOINT + 'reports/' + str(item), 
                auth=(USDA_API_KEY, ''))
            json_response = response.json()

            print("Size of report id " + str(item) + ": " + str(len(json_response['results'])))

            count = 0
            for row in json_response['results']:
                if self.canSkipRow(row):
                    try:
                        report = USDAReport(row)
                        g.db.usda_reports.create_report(report)
                        count += 1
                    except Exception as e:
                        print(row)
                        raise Exception(e)

            print("Size of report id " + str(item) + " added: " + str(count))

    def getUsdaData(self):
        """Encapsulates the different report calls and calls everything once"""
        g.db.usda_reports.delete_old_reports()
        self.getPublicReports()
        self.getMandatoryReports()
