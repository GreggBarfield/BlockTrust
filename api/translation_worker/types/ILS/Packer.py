from ...exceptions import ExecutionException
from ...all_to_unix import all_to_unix
from core.sectors import sectors_by_name


from ...abstract_type import AbstractType


class PackerType(AbstractType):

    NAMESPACE = "ILS"
    TYPE = "Packer"

    def _check_format(self):
        keys = [
            "EIDNum", "EIDDate", "Company", "TreatmentCount",
            "DeadInd", "DeathCause", "RailedInd", "RailCause",
            "USDAYieldGrade", "USDAQualityGrade", "CarcassWeight",
            "Packer", "PlantID"
        ]
        for key in keys:
            if key not in self.insert['fields']:
                raise ExecutionException("Key missing: " + key)

    def block_key(self):
        return None

    def handle(self):
        db = self.db
        insert = self.insert
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
        self._check_format()

        fields = insert['fields']

        account = insert["account"]
        eid = int(fields["EIDNum"])

        # Sighting
        self.emit(db.matches.factory.create_sighting(
            eid=eid,
            account_id=account,
            account_link_id=db.account_links.get_by_company(
                "ILS",
                insert_sector=sectors_by_name["Feedlot"],
                insert=True
            )[0].id()
        ))

        # Born
        # EIDDate is not a birthday!
        # birth_date = all_to_unix(insert["fields"]["EIDDate"])
        # self.emit(db.matches.factory.create_born(account=account, time=birth_date, eid=eid)

        # Death
        # NEI, no examples

        # Railed
        # NEI, no examples

        # Packer data ready?
        if fields["Packer"] != "":
            # Packer data ready

            self.emit(db.matches.factory.create_sighting(
                eid=eid,
                account_id=account,
                account_link_id=db.account_links.get_by_company(
                    fields["Company"],
                    insert_sector=sectors_by_name["Packer"],
                    insert=True
                )[0].id()
            ))

            # USDAYieldGrade

            self.emit(db.matches.factory.create_usda_yield_grade(
                int(float(fields["USDAYieldGrade"])),
                eid=eid,
                account_id=account
            ))

            # USDAQualityGrade

            self.emit(db.matches.factory.create_usda_quality_grade(
                fields["USDAQualityGrade"],
                eid=eid,
                account_id=account
            ))

            # Packer, PlantID (Sighting, Packer)

            if ";" in fields["Packer"] or ";" in str(fields["PlantID"]):
                raise ExecutionException("; not allowed in packer info")

            self.emit(db.matches.factory.create_packer(
                fields["Packer"].strip() + ";" + str(fields["PlantID"]).strip(),
                eid=eid,
                account_id=account
            ))
