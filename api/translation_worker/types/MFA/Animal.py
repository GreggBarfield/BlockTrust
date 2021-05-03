from ...exceptions import ExecutionException
from .blocks import block_eid_from_animal_id
from ...all_to_unix import all_to_unix
from ...abstract_type import AbstractType


class AnimalType(AbstractType):

    NAMESPACE = "MFA"
    TYPE = "Animal"

    def _check_format(self):
        keys = ["AnimalID", "EID", "VisualID", "Birthdate", "WeanDate"]
        for key in keys:
            if key not in self.insert['fields']:
                raise ExecutionException("Key missing: " + key)

    def block_key(self):
        return None

    def handle(self):
        db = self.db
        insert = self.insert
        self._check_format()

        account = insert["account"]
        eid = int(insert["fields"]["EID"])
        visual_id = insert["fields"]["VisualID"]
        birth_date = all_to_unix(insert["fields"]["Birthdate"])
        wean_date = all_to_unix(insert["fields"]["WeanDate"])

        if (
            visual_id is not None and (
                isinstance(visual_id, str) and visual_id != "" or
                isinstance(visual_id, int) and visual_id != 0
            )
        ):
            self.emit(db.matches.factory.create_visual_id(
                account_id=account,
                visual_id=visual_id,
                eid=eid
            ))

        if birth_date is not None:
            self.emit(db.matches.factory.create_born(
                account_id=account,
                time=birth_date,
                eid=eid
            ))

        if wean_date is not None:
            self.emit(db.matches.factory.create_weaned(
                account_id=account,
                time=wean_date,
                eid=eid
            ))

        self.emit_block(
            block_eid_from_animal_id(
                insert['account'],
                insert['fields']['AnimalID']
            ),
            insert['fields']['EID']
        )
