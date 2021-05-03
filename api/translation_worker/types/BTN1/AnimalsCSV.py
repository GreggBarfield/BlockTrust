from api.translation_worker.all_to_unix import all_to_unix
from .medical_helper import format_data
from core.sectors import sectors_by_name
from ...exceptions import ExecutionException
from .remapper import remap


from ...abstract_type import AbstractType


class AnimalsCSVType(AbstractType):

    NAMESPACE = "BTN1"
    TYPE = "AnimalsCSV"

    def block_key(self):
        return None

    def handle(self):
        db = self.db
        insert = self.insert
        account = insert["account"]
        insert["fields"] = fields = remap(insert["fields"], {
            "Sex": "sex",
            "FarmID": "farmid",
            "ZipCode": "zipcode",
            "PatronID": "patronid",
            "VisualID": "visualid",
            "WeanDate": "weandate",
            "CreepFeed": "creepfeed",
            "SequenceID": "sequence",
            "SysEndTime": "end_time",
            "WeanWeight": "weanweight",
            "BirthWeight": "birthweigh",
            "ElectronicID": "electronic",
            "SysStartTime": "st_time",
            "ApplicationID": "applicatio",
            "CalfBirthDate": "calfbirthd",
            "MarketingDate": "marketingd",
            "FirstBirthDate": "firstbirth",
            "IsVetProcessed": "isvetproce",
            "NumberOfCalves": "numberofca",
            "ApplicationDate": "appdate",
            "CalfDescription": "calfdescri",
            "First14DateFeed": "first14day",
            "Second31DayFeed": "second31da",
            "WeaningStrategy": "weaningstr",
            "SaleLocationName": "salelocati",
            "MarketingMethodName": "marketingm",
            "EstimatedSaleWeaight": "estimateds",
            "EstimatedSaleWeight": "estimateds",
            "First14DayFeedMethod": "first14da1",
            "Second31DayFeedMethod": "second31d1",
        })

        try:
            patronid = int(fields["patronid"])
        except ValueError as e:
            raise ExecutionException("while converting patron id: " + str(e))
        account_link = db.account_links.get_by_uid(patronid, 0, insert=True)[0].id()
        eid = int(fields["electronic"])

        self.emit(db.matches.factory.create_visual_id(
            visual_id=fields["visualid"],
            account_id=account,
            account_link_id=account_link,
            eid=eid,
        ))

        weaned_object = {}

        weaned_object_tags = [
            ("at", "weaningstr"),
            ("creep_feed", "creepfeed"),
            ("first_14_feed", "first14day"),
            ("first_14_method", "first14da1"),
            ("second_31_feed", "second31da"),
            ("second_31_method", "second31d1")
        ]

        for tag in weaned_object_tags:
            if fields[tag[1]].strip() != "":
                weaned_object[tag[0]] = fields[tag[1]].strip()

        if fields["weaningstr"].strip() != "":
            weaned_object["at"] = fields["weaningstr"].strip()

        if weaned_object == {}:
            weaned_object = None

        self.emit(db.matches.factory.create_weaned(
            time=all_to_unix(fields["weandate"]),
            account_id=account,
            account_link_id=account_link,
            data=weaned_object,
            eid=eid
        ))

        self.emit(db.matches.factory.create_born(
            time=all_to_unix(fields["firstbirth"]),
            account_id=account,
            account_link_id=account_link,
            eid=eid
        ))

        sold_object = {}
        if fields['marketingm'].strip().lower() not in ('', "unknown"):
            sold_object["method"] = fields['marketingm'].strip()
        if fields['salelocati'].strip() != '':
            sold_object["location"] = fields['salelocati'].strip()

        if int(fields['numberofca']) != 0:
            sold_object["group_size"] = int(fields['numberofca'])

        if sold_object != {}:
            self.emit(db.matches.factory.create_sold(
                account_id=account,
                account_link_id=account_link,
                eid=eid,
                time=all_to_unix(fields["marketingd"]),
                data=sold_object
            ))
