from copy import deepcopy
from ...match_types import match_types_by_id

class AnimalException(Exception):
    """Generic animal exception."""

    def __init__(self, reason):
        """Constructor for AnimalException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Animal:

    def __init__(self, db, eid, matches):
        """Animal constructor.

        Params:
            db: Database object
            eid: The animal's EID
            matches: A list of all match row(s) for the animal.
                This can be empty.
                Conflicts are resolved by using a later match.
                Note these are not deepcopied.

        Raises:
            AnimalException
        """
        self._db = db
        self._eid = eid
        self._matches_by_type = {}
        self._matches = matches

        for match in self._matches:
            if match["eid"] != eid:
                raise AnimalException("'matches' should have all been for the animal (EID mismatch)")

            self._matches_by_type[match['type']] = match

    def eid(self):
        """Gets animal EID

        Returns:
            The match ID
        """
        return self._eid

    def matches(self):
        """Gets animal Match(s)

        Returns:
            A (possibly empty) list of Match(s)
        """
        return self._matches

    def data(self, type_id):
        """Get a type's data by ID.

        Returns:
            The type's data, or None.
        """
        return self._matches_by_type[type_id] if type_id in self._matches_by_type else None

    def match(self, type_id):
        """Get a type's Match object by ID.

        Returns:
            The type's Match object, or None.
        """
        return self._matches_by_type[type_id] if type_id in self._matches_by_type else None
