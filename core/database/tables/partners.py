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
            AccountsException on ID not found
        """
        partner_rows = self._db.execute_d(
            """SELECT * FROM partners
                WHERE id=%(id)s
            """,
            {
                "id": partner_id
            }
        )
        if len(partner_rows) != 1:
            raise PartnersException("No partner found with that ID.")
        return Partner(self._db, partner_rows[0])