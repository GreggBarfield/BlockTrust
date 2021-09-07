from ...exceptions import ExecutionException
from core.database.database import Database
from api.database.inserts_model import InsertsModel
from ...all_to_unix import all_to_unix
from core.sectors import sectors_by_name


def _check_format(insert):
    keys = [
        "EIDNum", "EIDDate", "Company", "TreatmentCount",
        "DeadInd", "DeathCause", "RailedInd", "RailCause",
        "USDAYieldGrade", "USDAQualityGrade", "CarcassWeight",
        "Packer", "PlantID"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def block_key(insert):
    return None


def handle(db: Database, inserts_model: InsertsModel, insert, block_value):
    """Handle a Packer insert from ILS.

    Currently processing fields like
        {
            "EIDNum": "982000423956846",
            "Packer": "Tyson",
            "Company": "gbf",
            "EIDDate": "9/30/2020 12:00:00 AM",
            "PlantID": "010",
            "CarcassWeight": "859",
            "USDAYieldGrade": "5.0",
            "USDAQualityGrade": "Choice"
        }
    but expecting all fields in _check_format
    """
    _check_format(insert)

    fields = insert['fields']

    account = insert["account"]
    eid = int(fields["EIDNum"])
    api_insert = insert["id"]

    account_link = None
    # if company is specified, animal is located at the company else it is assumed to be located at partner ILS
    if fields["Company"] != "":
        account_link = db.account_links.get_by_affiliate_id(fields["Company"].strip().upper(), partner_account=account, api_insert=api_insert, insert=True)[0].id()

    db.matches.types.insert_sighting(
        eid=eid,
        account=account,
        account_link=account_link,
        api_insert=api_insert
    )
    # Born
    # EIDDate is not a birthday!
    # birth_date = all_to_unix(insert["fields"]["EIDDate"])
    # db.matches.types.insert_born(account=account, time=birth_date, eid=eid)

    # Death
    # NEI, no examples

    # Railed
    # NEI, no examples


    # Packer data ready?
    if fields["Packer"] != "":
        # Packer data ready
        # USDAYieldGrade

        db.matches.types.insert_usda_yield_grade(
            int(float(fields["USDAYieldGrade"])),
            eid=eid,
            account=account,
            account_link=account_link,
            api_insert=api_insert
        )

        # USDAQualityGrade

        db.matches.types.insert_usda_quality_grade(
            fields["USDAQualityGrade"],
            eid=eid,
            account=account,
            account_link=account_link,
            api_insert=api_insert
        )

        # Packer, PlantID (Sighting, Packer)

        if ";" in fields["Packer"] or ";" in str(fields["PlantID"]):
            raise ExecutionException("; not allowed in packer info")

        db.matches.types.insert_packer(
            fields["Packer"].strip() + ";" + str(fields["PlantID"]).strip(),
            eid=eid,
            account=account,
            account_link=account_link,
            api_insert=api_insert
        )
