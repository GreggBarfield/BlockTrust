import re
from . import profile as profile

setup = profile.setup
get_orders = profile.get_orders
cb_running = profile.cb_running
cb_processed = profile.cb_processed


ENDPOINT = "https://api.dev.blocktrustnetwork.com/api"
ACCOUNT = 605
TOKEN = ""
NAMESPACE = "BTN1"


def prep_order(file_name):
    base = {
        "File Name": file_name,
        "Insert Namespace": NAMESPACE,
        "Account": ACCOUNT,
        "Token": TOKEN,
        "Endpoint": ENDPOINT
    }
    if re.fullmatch("treatment\\.csv", file_name):
        base["Insert Type"] = "TreatmentCSV"
        return base
    if re.fullmatch("feeder_results.*\\.csv", file_name):
        base["Insert Type"] = "FeederResultsCSV"
        return base
    if re.fullmatch("match_table.*\\.csv", file_name):
        base["Insert Type"] = "MatchTableCSV"
        return base
    if re.fullmatch("processing.*\\.csv", file_name):
        base["Insert Type"] = "ProcessingCSV"
        return base
    if re.fullmatch("all_animals.*\\.csv", file_name):
        base["Insert Type"] = "AnimalsCSV"
        return base
    return None


profile.prep_order = prep_order
