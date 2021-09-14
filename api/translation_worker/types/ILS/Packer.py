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

    partner_account = insert["account"]
    eid = int(fields["EIDNum"])
    api_insert = insert["id"]

    feeder_account_link = None
    if fields["Company"] != "":
        feeder_account_link = db.account_links.get_by_affiliate_id(fields["Company"].strip().upper(), partner_account=partner_account, api_insert=api_insert,
                                                                        sector=sectors_by_name["Feedlot"], insert=True)[0]
        if feeder_account_link.account_id() is not None:
            feeder = db.accounts.get_by_id(feeder_account_link.account_id())
        else:
            # See if account is present but not linked and if so link the account. This case should never happen because:
            # 1. Let's say we got the affiliate account from the api. Then we insert without an account. And in such a case the account will also not exist in accounts table
            # 2. The affiliate account first comes from the sign up. This case we will create the link and it will be ready for the api to use.
            # 3. The affiliate account comes form a SQL insert query... that is when this code will run. That is the case for our feeders/packers currently. However, this 
            # might change once the staff portal is up and running. But still probably good to keep this logic
            feeder = db.accounts.get_by_partner_affiliate_id(feeder_account_link.partner_account(), feeder_account_link.affiliate_id())
            if feeder is not None:
                db.account_links.update_account_link_with_account(feeder.partner_account(), feeder.affiliate_id(), feeder.sector_id(), feeder.company(), feeder.id())

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
                    lat, lon = db.zip_codes.get_lat_lon(int(f5))
                    # add feedyard sighting for one day before
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate'])-86400,
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=feeder_account_link.id(),
                        api_insert=api_insert
                    )

        # add sighting at packer using plant id
        packer_account_link = db.account_links.get_by_affiliate_id(fields["PlantID"], partner_account=partner_account, sector=sectors_by_name["Packer"], 
                                                                        api_insert=api_insert, insert=True)[0]
        if packer_account_link.account_id() is not None:
            packer = db.accounts.get_by_id(packer_account_link.account_id())
        else:
            packer = db.accounts.get_by_partner_affiliate_id(packer_account_link.partner_account(), packer_account_link.affiliate_id())
            if packer is not None:
                db.account_links.update_account_link_with_account(packer.partner_account(), packer.affiliate_id(), packer.sector_id(), packer.company(), packer.id())

        if packer is not None:
            zipcode = str(packer.zip())
            if len(zipcode) >= 5:
                f5 = zipcode[0:5]
                for d in f5:
                    if d not in "0123456789":
                        break
                else:
                    lat, lon = db.zip_codes.get_lat_lon(int(f5))
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate']),
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=packer_account_link.id(),
                        api_insert=api_insert
                    )

        # USDAYieldGrade
        db.matches.types.insert_usda_yield_grade(
            int(float(fields["USDAYieldGrade"])),
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert
        )

        # USDAQualityGrade
        db.matches.types.insert_usda_quality_grade(
            fields["USDAQualityGrade"],
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert
        )

        # Packer, PlantID (Sighting, Packer)

        # if ";" in fields["Packer"] or ";" in str(fields["PlantID"]):
        #     raise ExecutionException("; not allowed in packer info")

        # db.matches.types.insert_packer(
        #     fields["Packer"].strip() + ";" + str(fields["PlantID"]).strip(),
        #     eid=eid,
        #     account=account,
        #     account_link=packer_account_link,
        #     api_insert=api_insert
        # )
    else:
        # Packer data not available and hence Add feed yard sighting
        if feeder is not None:
            zipcode = str(feeder.zip())
            if len(zipcode) >= 5:
                f5 = zipcode[0:5]
                for d in f5:
                    if d not in "0123456789":
                        break
                else:
                    lat, lon = db.zip_codes.get_lat_lon(int(f5))
                    db.matches.types.insert_sighting(
                        eid=eid,
                        time=all_to_unix(fields['EIDDate']),
                        lat=lat,
                        lon=lon,
                        partner_account=partner_account,
                        account_link=feeder_account_link.id(),
                        api_insert=api_insert
                    )
