from copy import deepcopy
from ...sectors import sectors_by_id

class Partner:

    def __init__(self, db, row):
        """User constructor.

        Params:
            db: Database object
            row: A 'users' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)

    def id(self):
        return self._row['id']

    def partner_id(self):
        return self._row['partner_id']

    def partner_name(self):
        return self._row['partner_name']

    def sector_id(self):
        return self._row['sector']

    def sector_name(self):
        return sectors_by_id[self._row['sector']]

    def contact_name(self):
        return self._row['contact_name']

    def email(self):
        return self._row['email']
    
    def phone(self):
        return self._row['phone']
    
    def address(self):
        return self._row['address']
    
    def city(self):
        return self._row['city']
    
    def state(self):
        return self._row['state']
    
    def zip(self):
        return self._row['zip']