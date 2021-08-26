from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import sectors_by_name


def block_key(insert):
    return None


def handle(db: Database, inserts_model: InsertsModel, insert, block_value):
    fields = insert["fields"]
    time = all_to_unix(fields["killdate"])
    account = insert["account"]
    eid = int(fields["eid"])
    api_insert = insert["id"]

    # account_link = db.account_links.get_by_company(
    #     fields["packer"].strip(),
    #     insert_sector=sectors_by_name["Packer"],
    #     insert=True
    # )[0].id()

    died = False
    if int(float(fields["hotwt"])) != 0:
        died = True
        db.matches.types.insert_hot_weight(
            weight=int(float(fields["hotwt"])),
            eid=eid,
            time=time,
            account=account,
            api_insert=api_insert
        )

    if fields["grade1"].strip() != "":
        died = True
        db.matches.types.insert_usda_quality_grade(
            grade=fields["grade1"].strip(),
            eid=eid,
            time=time,
            account=account,
            api_insert=api_insert
        )

    if int(fields["side1yiel1"]) != 0:
        died = True
        db.matches.types.insert_usda_yield_grade(
            grade=int(fields["side1yiel1"]),
            eid=eid,
            time=time,
            account=account,
            api_insert=api_insert
        )

    if int(fields["railedind"]) != 0:
        db.matches.types.insert_railed(
            eid=eid,
            time=time,
            account=account,
            api_insert=api_insert
        )

    if fields["packer"].strip() != "":
        packer_str = fields["packer"].strip() + ";" + fields["plantid"].strip()
        db.matches.types.insert_packer(
            eid=eid,
            time=time,
            account=account,
            packer_str=packer_str,
            api_insert=api_insert
        )
    if died:
        db.matches.types.insert_died(
            eid=eid,
            time=time,
            account=account,
            reason=None,
            api_insert=api_insert
        )
    elif int(fields["deadind"]) != 0:
        s = "Died before being packed"
        if int(fields["treat_cnt"]) != 0:
            s += " after being treated " + fields["treat_cnt"] + " times"
        db.matches.types.insert_died(
            eid=eid,
            time=time,
            account=account,
            reason=s,
            api_insert=api_insert
        )
