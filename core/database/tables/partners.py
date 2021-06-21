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

    def get_no_partner(self):
        """Gets the no partner entry in database. No partner record only has a partner id , partner name and nothing else. 
        
        Returns:
            One Partner() object
        """
        partner_rows = self._db.execute_d(
            """SELECT * FROM partners
                WHERE sector_id IS NULL
            """
        )
        if len(partner_rows) > 0:
            return Partner(self._db, partner_rows[0])
        else:
            raise PartnersException("No Partner partner doesn't exist in the database and needs to be added.")