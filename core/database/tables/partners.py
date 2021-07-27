from ..objects.partner import Partner

class PartnersException(Exception):
    """Partner generic exception."""

    def __init__(self, reason):
        """Constructor for PartnerException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Partners:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, partner_id):
        """Gets a partner by an ID.

        Params:
            id: the partner id
        
        Returns:
            An Partner() object

        Raises:
            PartnersException on ID not found
        """
        partner_rows = self._db.execute_d(
            """SELECT * FROM partners
                WHERE partner_id=%(partner_id)s
            """,
            {
                "partner_id": partner_id
            }
        )
        if len(partner_rows) != 1:
            raise PartnersException("No partner found with that ID.")
        return Partner(self._db, partner_rows[0])

    def get_by_sector_id(self, sector_id):
        """Gets a partner by an sector id.

        Params:
            sector_id: the sector id
        
        Returns:
            Zero or more Partner() objects
        """
        partner_rows = self._db.execute_d(
            """SELECT * FROM partners
                WHERE sector_id=%(sector_id)s
            """,
            {
                "sector_id": sector_id
            }
        )
        
        return [
            Partner(self._db, partner_row)
            for partner_row in partner_rows
        ]

    def get_discount_percentage(self, coupon_code):
        """
        Gets the discount percentage for a particular coupon code(Related to each partner)

        Params:
            coupon_code: The coupon code entered by the user

        Returns:
            discount: The discount percentage to be applied to the users cart amount
        Raises:
            PartnersException on ID not found
        """
        try:
            discount = self._db.execute_d(
                """SELECT discount_percentage FROM partners
                    WHERE coupon_code=%(coupon_code)s
                """,
                {
                    "coupon_code": coupon_code
                }
            )
            if len(discount) != 1:
                raise PartnersException("Coupon code invalid")
            return discount[0]
        except PartnersException as e:
            raise e
