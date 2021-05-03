from core.database.database import Database
from api.database.inserts_model import InsertsModel
from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from .remapper import remap


from ...abstract_type import AbstractType


class TreatmentCSVType(AbstractType):

    NAMESPACE = "BTN1"
    TYPE = "TreatmentCSV"

    def block_key(self):
        return None

    def handle(self):
        db = self.db
        insert = self.insert
        insert["fields"] = fields = remap(insert["fields"], {
            "Symptoms": "symptoms",
            "LotNumber": "lot_no",
            "IsFatality": "fatality",
            "SequenceID": "sequence",
            "SysEndTime": "end_time",
            "ProductName": "prod_name",
            "CategoryName": "cat_name",
            "ElectronicID": "electronic",
            "LocationName": "loc_name",
            "SysStartTime": "st_time",
            "TreatmentDate": "treat_dt",
            "AdministrationRouteName": "admin_rt"
        })
        time = all_to_unix(fields["treat_dt"])
        account = insert["account"]
        eid = int(fields["electronic"])  # This might fail!

        if time is None:
            return

        medical_data = format_data(
            product=fields["prod_name"],
            method=fields["admin_rt"],
            location=fields["loc_name"],
            symptom=fields["symptoms"],
            fatal=fields["fatality"].strip().lower() == "true",
            category=fields["cat_name"],
        )

        if medical_data is None or medical_data == {}:
            return

        self.emit(db.matches.factory.create_medical(
            time=time,
            data=medical_data,
            eid=eid,
            account_id=account
        ))
