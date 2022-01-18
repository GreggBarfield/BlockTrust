from copy import deepcopy


class Notification:
    def __init__(self, db, row):
        """
        Notification constructor

        Params:
            db: Database Object
            row: A product row dictionary
        """

        self._db = db
        self._row = deepcopy(row)

    def id(self):
        return self._row['id']

    def message_subject(self):
        return self._row['message_subject']

    def message(self):
        return self._row['message']

    def is_archived(self):
        return self._row['is_archived']

    def created_timestamp(self):
        return self._row['created_timestamp']