from copy import deepcopy


class USDAAccountFavorite:
    def __init__(self, row):
        """USDA Account Favorite Constructor.
        
        Params:
            row: A row dictionary of USDA Account Favorite data
        """
        self._row = deepcopy(row)

    def account(self):
        return self._row['account']

    def id(self):
        return self._row['id']

    def state(self):
        return self._row['state']

    def city_id(self):
        return self._row['city_id']

    def city_name(self):
        return self._row['city_name']
