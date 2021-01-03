from ..objects.animal import Animal, AnimalException

class AnimalsException(Exception):
    """Animals generic exception."""

    def __init__(self, reason):
        """Constructor for AnimalsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Animals:

    def __init__(self, db):
        self._db = db


    def get_by_eid(self, eid):
        """Gets an animal by their EID.

        Params:
            eid: the eid
        
        Returns:
            An Animal object
                Keep in mind that this object could be empty
            
        Raises:
            AnimalsException
        """
        return Animal(self._db, eid, self._db.matches.get_by_eids((eid,)))


    def get_by_account_id(self, account):
        """Gets animals that should be included in the account's statistics.

        Params:
            account: The account to get animals on

        Returns:
            A list of Animal objects (could be empty)
        """
        # Get animals by account link
        # TODO: Get animals by watch table that are included in statistics
        # TODO: switch this entirely to watch list? might make database search easier
        matches = g.db.matches.get_by_account_links_spread(account.account_links())
        
        # Do this locally to take off pressure on the database
        eids = []
        for match in matches:
            if match.eid() not in eids:
                eids[match.eid()] = []
            eids[match.eid()].append(match)

        return [Animal(self._db, eid, eids[eid]) for eid in eids]
