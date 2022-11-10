from core.utilities.zip_codes import get_lat_lon
from ...exceptions import ExecutionException
from ...all_to_unix import all_to_unix
from core.sectors import sectors_by_name


def _check_format(insert):
    keys = [
        "EID", "KillDate", "USDAYieldGrade", "USDAQualityGrade", "CarcassWeight", "PlantID"
    ]
    for key in keys:
        if key not in insert['fields']:
            raise ExecutionException("Key missing: " + key)


def handle(db, insert):
    """Handle data from Packer file exported to us.
    """
    _check_format(insert)

    fields = insert['fields']

    partner_account = insert["account"]
    eid = int(fields["EID"])
    api_insert = insert["id"]

    feeder_account_link = None
    if "FeederCode" in fields and fields["FeederCode"] != "":
        feeder_account_link = db.account_links.get_by_affiliate_id(fields["FeederCode"].strip().upper(), partner_account=partner_account, api_insert=api_insert,
                                                                        sector=sectors_by_name["Feedlot"], insert=True)[0]
        if feeder_account_link.account_id() is not None:
            feeder = db.accounts.get_account_by_id(feeder_account_link.account_id())
        else:
            # See if account is present but not linked to account_links and if so link the account.
            feeder = db.accounts.get_by_partner_affiliate_id(feeder_account_link.partner_account_id(), feeder_account_link.affiliate_id())
            if feeder is not None:
                db.account_links.update_account_link_with_account(feeder.partner_account_id(), feeder.affiliate_id(), feeder.sector_id(), feeder.company(), feeder.name(), feeder.id())

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
                    time=all_to_unix(fields['KillDate'])-86400,
                    lat=lat,
                    lon=lon,
                    partner_account=partner_account,
                    account_link=feeder_account_link.id(),
                    api_insert=api_insert,
                    zip=zipcode
                )

    # add sighting at packer using plant id
    if isinstance(fields["PlantID"], str) and fields["PlantID"].isdigit():
        fields["PlantID"] = fields["PlantID"].lstrip("0")

    packer_account_link = db.account_links.get_by_affiliate_id(fields["PlantID"], partner_account=partner_account, sector=sectors_by_name["Packer"], 
                                                                    api_insert=api_insert, insert=True)[0]
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
                    time=all_to_unix(fields['KillDate']),
                    lat=lat,
                    lon=lon,
                    partner_account=partner_account,
                    account_link=packer_account_link.id(),
                    api_insert=api_insert,
                    zip=zipcode
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

    # Hot Weight
    if fields["CarcassWeight"] and float(fields["CarcassWeight"]) != 0:
        db.matches.types.insert_hot_weight(
            weight=float(fields["CarcassWeight"]),
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert
        )

    # Ribeye Area.
    packer_data = {}
    if "RibeyeArea" in fields and fields["RibeyeArea"] and float(fields["RibeyeArea"]) != 0:
        packer_data["RibeyeArea"] = float(fields["RibeyeArea"])

    # Marbling Score
    if "MarblingScore" in fields and fields["MarblingScore"] and int(fields["MarblingScore"]) != 0:
        packer_data["MarblingScore"] = int(fields["MarblingScore"])

    # Fat Thickness
    if "FatThickness" in fields and fields["FatThickness"] and float(fields["FatThickness"]) != 0:
        packer_data["FatThickness"] = float(fields["FatThickness"])
        
    if packer_data:
        db.matches.types.insert_packer(
            packer_str=packer_data,
            eid=eid,
            partner_account=partner_account,
            account_link=packer_account_link.id(),
            api_insert=api_insert
        )
