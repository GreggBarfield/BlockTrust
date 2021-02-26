import re
from . import profile as profile

setup = profile.setup
get_orders = profile.get_orders
cb_running = profile.cb_running
cb_processed = profile.cb_processed


ENDPOINT = "https://api.dev.blocktrustnetwork.com/api"
ACCOUNT = 604
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
    if re.fullmatch("HealthTrackAnimal.*\\.csv", file_name):
        base["Insert Type"] = "AnimalsCSV"
    if re.fullmatch("HealthTrackProcessing.*\\.csv", file_name):
        base["Insert Type"] = "ProcessingCSV"
    if re.fullmatch("HealthTrackTreatment.*\\.csv", file_name):
        base["Insert Type"] = "TreatmentCSV"
    if "Insert Type" in base and base["Insert Type"] is not None:
        return base
    return None


profile.prep_order = prep_order
