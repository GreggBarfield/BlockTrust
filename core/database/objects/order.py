from copy import deepcopy


class Order:

    def __init__(self, db, row):
        """Order constructor.

        Params:
            db: Database object
            row: An 'orders' row dictionary
        """
        self._db = db
        self._row = deepcopy(row)

    def id(self):
        return self._row['id']

    def account(self):
        return self._row['account']

    def total_tax(self):
        return self._row['total_tax']

    def total_shipping(self):
        return self._row['total_shipping']

    def total_cart(self):
        return self._row['total_cart']

    def grand_total(self):
        return self._row['grand_total']

    def shipping_address(self):
        return self._row['shipping_address']

    def shipping_city(self):
        return self._row['shipping_city']

    def shipping_state(self):
        return self._row['shipping_state']

    def shipping_country(self):
        return self._row['shipping_country']

    def shipping_zip(self):
        return self._row['shipping_zip']

    def first_name(self):
        return self._row['first_name']

    def last_name(self):
        return self._row['last_name']

    def email(self):
        return self._row['email']

    def phone(self):
        return self._row['phone']

    def discount(self):
        return self._row['discount']

    def stripe_payment_intent(self):
        return self._row['stripe_payment_intent']

    def stripe_paid(self):
        return self._row['stripe_paid']

    def create_timestamp(self):
        return self._row['create_timestamp']