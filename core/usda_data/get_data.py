from flask import g
import requests
import csv
from ..database.tables.usda_reports import USDAReports
from ..database.objects.usda_report import USDAReport
from ..database.database import Database
from ..config import USDA_API_KEY


def getUsdaData():
    # query market type for livestock. Should give 500ish results
    marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]

    reports = dict()
    for id in marketTypeIDs:
        response = requests.get('https://marsapi.ams.usda.gov/services/v1.2/marketTypes/' + str(id), auth=(USDA_API_KEY, ''))
        json_response = response.json()

        for row in json_response['results']:
            reports[row['slug_id']] = row
    
    print("Size of unique reports: " + str(len(reports)))

    for item in reports:
        response = requests.get('https://marsapi.ams.usda.gov/services/v1.2/reports/' + str(item), auth=(USDA_API_KEY, ''))
        json_response = response.json()

        print("Size of report id " + str(item) + ": " + str(len(json_response['results'])))

        for row in json_response['results']:
            report = USDAReport(row)
            g.db.usda_reports.create_report(report)

