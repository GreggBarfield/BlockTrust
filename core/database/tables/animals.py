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