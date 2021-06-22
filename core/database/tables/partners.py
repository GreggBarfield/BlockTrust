from ..objects.partner import Partner
from flask import g

class PartnersException(Exception):
    """Partner generic exception."""

    def __init__(self, reason):
        """Constructor for PartnerException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Partners:
    """
    This represents partners table and has operations related to that table. 
    This doesn't have a database object as an attribute. I am little concerned as to how db keeps growing in size with every table added
    db is also stored in g.db and g.db initialized on every request, hence it is not efficient to keep adding tables to it. 
    There is also a circular reference with db referring to the table object and the table object internally storing db
    Because of the above concerns I haven't added db attribute to this class and will be directly importing and using g.db here. 
    """

    def get_by_id(self, partner_id):
        """Gets a partner by an ID.

        Params:
            id: the partner id
        
        Returns:
            An Partner() object

        Raises:
            PartnersException on ID not found
        """
        partner_rows = g.db.execute_d(
            """SELECT * FROM partners
                WHERE partner_id=%(partner_id)s
            """,
            {
                "partner_id": partner_id
            }
        )
        if len(partner_rows) != 1:
            raise PartnersException("No partner found with that ID.")

        return Partner(partner_rows[0])

    def get_by_sector_id(self, sector_id):
        """Gets a partner by an sector id.

        Params:
            sector_id: the sector id
        
        Returns:
            Zero or more Partner() objects
        """
        partner_rows = g.db.execute_d(
            """SELECT * FROM partners
                WHERE sector_id=%(sector_id)s
            """,
            {
                "sector_id": sector_id
            }
        )
        
        return [
            Partner(partner_row)
            for partner_row in partner_rows
        ]