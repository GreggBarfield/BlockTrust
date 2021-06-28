from copy import deepcopy


class Product:
    def __init__(self, db, row):
        """
        Product constructor

        Params:
            db: Database Object
            row: A product row dictionary
        """

        self._db = db
        self._row = deepcopy(row)

    def product_no(self):
        return self._row['prod_no']

    def menu1(self):
        return self._row['menu1']

    def m1_short(self):
        return self._row['m1_short']

    def menu2(self):
        return self._row['m2_short']

    def product(self):
        return self._row['product']

    def pic_1(self):
        return self._row['pic_1']

    def pic_2(self):
        return self._row['pic_2']

    def pic_3(self):
        return self._row['pic_3']

    def price(self):
        return self._row['price']

    def orders(self):
        return self._row['orders']

    def post(self):
        return self._row['post']

    def subheader(self):
        return self._row['subheader']

    def details(self):
        return self._row['details']

    def unit(self):
        return self._row['unit']

    def creditcard_charge(self):
        return self._row['cc_charge']

    def original_price(self):
        return self._row['orig_price']

    def number_y_n(self):
        return self._row['number_y_n']

    def start_no(self):
        return self._row['start_no']

    def end_no(self):
        return self._row['end_no']

    def num_text(self):
        return self._row['num_text']
