import requests

from core.config import (USDA_API_KEY, USDA_MANDATORY_ENDPOINT, USDA_PUBLIC_ENDPOINT, USDA_GET_DATA, USDA_CUTOFF_PERIOD_IN_DAYS)
from core.database.objects.usda_report import USDAReport
from core.database.tables.debug_logs import DebugLogs
from core.database.tables.error_logs import ErrorLogs
import traceback
import datetime


class UsdaDataRetriever:
    """Class that gets the Data from the USDA APIs and adds them to the database"""

    def __init__(self, db):
        self._db = db

    def get_mandatory_reports(self):
        """Gets the 'mandatory reports' from API and adds to database"""

        if USDA_GET_DATA:
            response = requests.get(USDA_MANDATORY_ENDPOINT, auth=(USDA_API_KEY, ''))
            json_response = response.json()

            cattleReports = dict()
            published_dates = self._db.usda_reports.get_unique_published_dates_and_slug_id()

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

            print("USDADataRetriever.get_mandatory_reports(): Size of unique new cattle reports: " + str(len(cattleReports)))
            debug_logs  =  "Size of unique new cattle reports: " + str(len(cattleReports))
            for slug_id in cattleReports:
                response = requests.get(USDA_MANDATORY_ENDPOINT + str(slug_id) + '/national', 
                    auth=(USDA_API_KEY, ''))
                json_response = response.json()

                if type(json_response) is str:
                    print('USDADataRetriever thread: Got smaller data for: ' + str(slug_id))
                    debug_logs += "Got smaller data for: " + str(slug_id)
                    response = requests.get(USDA_MANDATORY_ENDPOINT + str(slug_id), 
                        auth=(USDA_API_KEY, ''))
                    json_response = response.json()

                reportsAddedCounter = 0
                for row in json_response['results']:
                    age_of_report = datetime.datetime.now() - datetime.datetime.strptime(row['published_date'],"%m/%d/%Y %H:%M:%S")

                    # only add data that is within the cutoff period
                    if age_of_report.days <= USDA_CUTOFF_PERIOD_IN_DAYS:
                        try:
                            report = USDAReport(row)
                            self._db.usda_reports.create_report(report)
                            reportsAddedCounter += 1
                        except Exception as e:
                            print("USDADataRetreiver.get_mandatory_reports(): Result Row excepted. Row: ", row)
                            print(e)
                            raise Exception(e, row)

                # for each report id (slug_id) we are getting possibly a couple hundred rows. Since for each report id (slug_id) there are multiple reports each day/week/etc.
                print("USDADataRetriever.get_mandatory_reports(): Added reports for cattle slug_id " + str(slug_id) 
                    + ": " + str(reportsAddedCounter))
                debug_logs +=  "Added reports for cattle slug_id " + str(slug_id) + ": " + str(reportsAddedCounter)
        else:
            print("USDADataRetreiver.get_mandatory_reports(): USDA get data is turned off")
            debug_logs = "USDA get data is turned off"
        DebugLogs(self._db).insert_debug_log("USDADataRetreiver.get_mandatory_reports()", "Run logs", "", {"details":debug_logs})

    def get_public_reports(self):
        """Gets the public report data from API and adds it to the database"""
        try:
            debug_logs = ""
            if USDA_GET_DATA:
                # query market type for livestock. Should give 500ish results
                marketTypeIDs = [1000, 1010, 1011, 1012, 1013, 1031, 1085]

                reports = dict()
                published_dates = self._db.usda_reports.get_unique_published_dates_and_slug_id()
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

                print("USDADataRetriever.get_public_reports(): Size of unique new reports: " + str(len(reports)))
                debug_logs += " Size of unique new cattle reports: " + str(len(reports))

                for slug_id in reports:
                    response = requests.get(USDA_PUBLIC_ENDPOINT + 'reports/' + str(slug_id), auth=(USDA_API_KEY, ''))
                    debug_logs += f" Getting /reports response for slug id: {slug_id}"
                    json_response = response.json()

                    reportsAddedCounter = 0
                    for row in json_response['results']:
                        try:
                            published_date = row['published_date'] if 'published_date' in row else row['published_Date']
                            age_of_report = datetime.datetime.now() - datetime.datetime.strptime(published_date,"%m/%d/%Y %H:%M:%S")
                        except Exception as e:
                            print("USDADataRetreiver.get_public_reports(): Problem with row['published_date']. Row: ", row)
                            print(e)
                            raise Exception(e, row)

                        # only add data that is within the cutoff period
                        if age_of_report.days <= USDA_CUTOFF_PERIOD_IN_DAYS:
                            try:
                                report = USDAReport(row)
                                self._db.usda_reports.create_report(report)
                                reportsAddedCounter += 1
                            except Exception as e:
                                print("USDADataRetreiver.get_public_reports(): Result Row excepted. Row: ", row)
                                print(e)
                                raise Exception(e, row)

                    # for each report id (slug_id) we are getting possibly a couple hundred rows. Since for each report id (slug_id) there are multiple reports each day/week/etc.
                    print("USDADataRetriever.get_public_reports(): Added reports for slug_id " + str(slug_id) 
                        + ": " + str(reportsAddedCounter))
                    debug_logs += " Added reports for slug_id " + str(slug_id) + ": " + str(reportsAddedCounter)
            else:
                print("USDADataRetreiver.get_public_reports():  USDA get data is turned off")
                debug_logs = "USDA get data is turned off"
        except Exception as e:
            raise e
        finally:
            DebugLogs(self._db).insert_debug_log("USDADataRetreiver.get_public_reports()", "Run logs", "", {"details":debug_logs})

    def delete_old_reports(self):
        rowCount = self._db.usda_reports.delete_reports_older_than(USDA_CUTOFF_PERIOD_IN_DAYS)
        # print("USDADataRetriever.delete_old_reports(): Reports deleted: " + str(rowCount))
        DebugLogs(self._db).insert_debug_log("USDADataRetriever.delete_old_reports()", "Reports deleted: " + str(rowCount))

def get_usda_data(db):
    try:
        retriever = UsdaDataRetriever(db)
        retriever.delete_old_reports()
        retriever.get_mandatory_reports()
        retriever.get_public_reports()
        print("USDADataRetreiver.get_usda_data(): Exiting. Current time: ", datetime.datetime.now().time())
    except Exception as e:
        if len(e.args) > 1:
            ErrorLogs(db).insert_error_log("USDA Data Retreiver", e.__class__.__name__ + ": " + str(e.args[0]), traceback.format_exc(), e.args[1])
        else:
            ErrorLogs(db).insert_error_log("USDA Data Retreiver", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        db.close()
