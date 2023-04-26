from core.database.tables.animals import Animals, AnimalsException
from core.utilities.zip_codes import get_lat_lon
from ...exceptions import ExecutionException
from core.database.database import Database
from core.database.tables.accounts import ILS_PARTNER_COMPANY
from api.database.inserts_model import InsertsModel
from ...all_to_unix import all_to_unix
from core.sectors import SECTORS_NAME_TO_ID
from core.database.combinations import perform_feeder_packer_data_received_actions

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


def handle(db: Database, insert):
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
    but expecting all fields in _check_format for ILS
    """
    partner_account = insert["account"]
    ils = db.accounts.get_partners(company=ILS_PARTNER_COMPANY)[0]
    if ils["id"] == partner_account:
        _check_format(insert)

    fields = insert['fields']

    eid = int(fields["EIDNum"])
    api_insert_id = insert["id"]

    feeder_account_link = None
    feeder = None
    if fields["Company"] != "":
        feeder_account_link = db.account_links.get_by_affiliate_id(fields["Company"].strip().upper(), partner_account=partner_account, api_insert=api_insert_id,
                                                                        sector=SECTORS_NAME_TO_ID["Feedlot"], insert=True)[0]
        if feeder_account_link.account_id() is not None:
            feeder = db.accounts.get_account_by_id(feeder_account_link.account_id())
        else:
            # See if account is present but not linked to account_links and if so link the account.
            feeder = db.accounts.get_by_partner_affiliate_id(feeder_account_link.partner_account_id(), feeder_account_link.affiliate_id())
            if feeder is not None:
                db.account_links.update_account_link_with_account(feeder.partner_account_id(), feeder.affiliate_id(), feeder.sector_id(), feeder.company(), feeder.name(), feeder.id())
    elif fields.get("FeederId", None):
        feeder = db.accounts.get_account_by_id(fields["FeederId"])
        feeder_account_link = db.account_links.get_by_account_id(fields["FeederId"])[0]

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

        if feeder is not None:      
            zipcode = str(feeder.zip())
            if len(zipcode) >= 5:
                f5 = zipcode[0:5]
                for d in f5:
                    if d not in "0123456789":
                        break
                else:
                    lat, lon = get_lat_lon(int(f5))
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate'])-86400,
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=feeder_account_link.id(),
                        api_insert=api_insert_id,
                        zip=zipcode
                    )

        if ";" in fields["Packer"] or ";" in str(fields["PlantID"]):
            raise ExecutionException("; not allowed in packer info")

        # add sighting at packer using plant id

        if fields["PlantID"].isdigit():
            fields["PlantID"] = fields["PlantID"].lstrip("0")

        packer_account_link = db.account_links.get_by_affiliate_id(fields["PlantID"], partner_account=partner_account, sector=SECTORS_NAME_TO_ID["Packer"], 
                                                                        api_insert=api_insert_id, insert=True)[0]
        if packer_account_link.account_id() is not None:
            packer = db.accounts.get_account_by_id(packer_account_link.account_id())
        else:
            packer = db.accounts.get_by_partner_affiliate_id(packer_account_link.partner_account_id(), packer_account_link.affiliate_id())
            if packer is not None:
                db.account_links.update_account_link_with_account(packer.partner_account_id(), packer.affiliate_id(), packer.sector_id(), packer.company(), packer.name(), packer.id())

        if packer is not None:
            zipcode = str(packer.zip())
            if len(zipcode) >= 5:
                f5 = zipcode[0:5]
                for d in f5:
                    if d not in "0123456789":
                        break
                else:
                    lat, lon = get_lat_lon(int(f5))
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate']),
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=packer_account_link.id(),
                        api_insert=api_insert_id,
                        zip=zipcode
                    )

        # USDAYieldGrade
        db.matches.types.insert_usda_yield_grade(
            int(float(fields["USDAYieldGrade"])),
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert_id
        )

        # USDAQualityGrade
        id = db.matches.types.insert_usda_quality_grade(
            fields["USDAQualityGrade"],
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert_id
        )

        perform_feeder_packer_data_received_actions(db, eid, schedule_email=bool(id), feeder_account_id=feeder.id() if feeder is not None else None,
                                                    packer_account_id=packer.id() if packer is not None else None, api_insert_id=api_insert_id)

        # Hot Weight
        if fields["CarcassWeight"] != "" and float(fields["CarcassWeight"]) != 0:
            db.matches.types.insert_hot_weight(
                weight=float(fields["CarcassWeight"]),
                eid=eid,
                partner_account=partner_account,
                account_link=packer_account_link.id(),
                api_insert=api_insert_id
            )

        # Ribeye Area. These are commented out because we don't know the keys that packer will send us
        # packer_data = {}
        # if fields["RibEyeArea"] != "" and float(fields["RibEyeArea"]) != 0:
        #     packer_data["RibEyeArea"] = float(fields["RibEyeArea"])

        # Marbling Score
        # if fields["MarblingScore"] != "" and int(fields["MarblingScore"]) != 0:
        #     packer_data["MarblingScore"] = int(fields["MarblingScore"])

        # Fat Thickness
        # if fields["FatThickness"] != "" and float(fields["FatThickness"]) != 0:   
        #     packer_data["FatThickness"] = float(fields["FatThickness"])
            
        # if packer_data:
        #     db.matches.types.insert_packer(
        #         packer_str = packer_data,
            # eid=eid,
            # partner_account=partner_account,
            # account_link=packer_account_link.id(),
            # api_insert=api_insert
        #     )

    else:
        # Packer data not available and hence Add feed yard sighting
        if feeder is not None:
            feeder_data = {}
            if fields.get("LotNumber", None):
                feeder_data["lot_number"] = fields["LotNumber"]
            if fields.get("PenNumber", None):
                feeder_data["pen_number"] = fields["PenNumber"]
            if fields.get("FeederInternalAccountId", None):
                feeder_data["feeder_account_number"] = fields["FeederInternalAccountId"]
            if fields.get("FeederWeight", None):
                feeder_data["feeder_weight"] = fields["FeederWeight"]
            if fields.get("TerminalReImplantWeight", None):
                feeder_data["terminal_reimplant_weight"] = fields["TerminalReImplantWeight"]
            if fields.get("TerminalReImplantDate", None):
                feeder_data["terminal_reimplant_date"] = fields["TerminalReImplantDate"]

            if feeder_data:
                try:
                    Animals(db).create_or_fail_animal(eid=eid, **feeder_data)
                except AnimalsException as e:
                    Animals(db).update_animal(eid=eid, **feeder_data)
                    print(f"{e}. It has been updated")

            zipcode = str(feeder.zip())
            if len(zipcode) >= 5:
                f5 = zipcode[0:5]
                for d in f5:
                    if d not in "0123456789":
                        break
                else:
                    lat, lon = get_lat_lon(int(f5))
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate']),
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=feeder_account_link.id(),
                        api_insert=api_insert_id,
                        zip=zipcode
                    )

            perform_feeder_packer_data_received_actions(db, eid, schedule_email=False, feeder_account_id=feeder.id(),
                                                        api_insert_id=api_insert_id)
