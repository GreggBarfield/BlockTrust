from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import sectors_by_name


from ...abstract_type import AbstractType


class FeederResultsCSVType(AbstractType):

    NAMESPACE = "BTN1"
    TYPE = "FeederResultsCSV"

    def block_key(self):
        return None

    def handle(self):
        db = self.db
        insert = self.insert
        fields = insert["fields"]
        time = all_to_unix(fields["killdate"])
        account = insert["account"]
        eid = int(fields["eid"])

        account_link = db.account_links.get_by_company(
            fields["packer"].strip(),
            insert_sector=sectors_by_name["Packer"],
            insert=True
        )[0].id()

        died = False
        if int(float(fields["hotwt"])) != 0:
            died = True
            self.emit(db.matches.factory.create_hot_weight(
                weight=int(float(fields["hotwt"])),
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
            ))

        if fields["grade1"].strip() != "":
            died = True
            self.emit(db.matches.factory.create_usda_quality_grade(
                grade=fields["grade1"].strip(),
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
            ))

        if int(fields["side1yiel1"]) != 0:
            died = True
            self.emit(db.matches.factory.create_usda_yield_grade(
                grade=int(fields["side1yiel1"]),
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
            ))

        if int(fields["railedind"]) != 0:
            self.emit(db.matches.factory.create_railed(
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
            ))

        if fields["packer"].strip() != "":
            packer_str = fields["packer"].strip() + ";" + fields["plantid"].strip()
            self.emit(db.matches.factory.create_packer(
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
                packer_str=packer_str
            ))
        if died:
            self.emit(db.matches.factory.create_died(
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
                reason=None
            ))
        elif int(fields["deadind"]) != 0:
            s = "Died before being packed"
            if int(fields["treat_cnt"]) != 0:
                s += " after being treated " + fields["treat_cnt"] + " times"
            self.emit(db.matches.factory.create_died(
                eid=eid,
                time=time,
                account_link_id=account_link,
                account_id=account,
                reason=s
            ))
