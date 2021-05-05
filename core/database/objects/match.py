from copy import deepcopy
import json
from hashlib import sha256
from ...match_types import match_types_by_id, match_types_by_name
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import database


class MatchException(Exception):
    """Generic match exception."""

    def __init__(self, reason):
        """Constructor for MatchException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class MatchFactory:
    """Match Factory

    A series of functions used to create Match objects, primarily to assist
    in creating different types.

    Each function has a **kwargs argument, which is the following:

        Required:
            eid: Required; the match EID

        Optional:
            account_id: An account ID
            account_link_id: An account link ID
            lat: A lattitude
            lon: A longitude
            time: Time it occurred
            created: The time the row was created in the database
                (generally don't pass this)

    Those are passed directly to the Match constructor.

    These Match.__init__ fields are handled per-create-function:
        type_id, data
    """

    def __init__(self, db: "database.Database"):
        """Creates a new match factory.

        Params:
            db: A Database object
        """
        self._db = db

    def create_sighting(self, **kwargs):
        return Match(
            db=self._db,
            type_id=match_types_by_name["Sighting"],
            **kwargs
        )

    def create_visual_id(self, visual_id, **kwargs):
        return Match(
            db=self._db,
            type_id=match_types_by_name["Visual ID"],
            data=str(visual_id),
            **kwargs
        )

    def create_weaned(self, **kwargs):
        return Match(
            db=self._db,
            type_id=match_types_by_name["Weaned"],
            **kwargs
        )

    def create_hot_weight(self, weight, **kwargs):
        """Create a hot weight match.

        Params:
            weight: The weight in pounds
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["Hot Weight"],
            data=float(weight),
            **kwargs
        )

    def create_born(self, **kwargs):
        return Match(
            db=self._db,
            type_id=match_types_by_name["Born"],
            **kwargs
        )

    def create_usda_yield_grade(self, grade, **kwargs):
        """Create a yield grade match.

        Params:
            grade: The yield grade
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["USDA Yield Grade"],
            data=grade,
            **kwargs
        )

    def create_usda_quality_grade(self, grade, **kwargs):
        """Create a quality grade match.

        Params:
            grade: The quality grade
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["USDA Quality Grade"],
            data=grade,
            **kwargs
        )

    def create_medical(self, data, **kwargs):
        """Create a medical match.

        Params:
            data: A dictionary of medical data.
                product
                location
                symptom
                method
                fatal
                category
        """
        if not isinstance(data, dict):
            raise ValueError("data should be a dictionary")
        if kwargs["time"] is None:
            raise ValueError("time should not be None")
        return Match(
            db=self._db,
            type_id=match_types_by_name["Medical"],
            data=data,
            **kwargs
        )

    def create_railed(self, **kwargs):
        return Match(
            db=self._db,
            type_id=match_types_by_name["Railed"],
            **kwargs
        )

    def create_packer(self, packer_str, **kwargs):
        """Create a packer match.

        Params:
            packer_str: Temporary string format, see FeederResultsCSV
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["Packer"],
            data=packer_str,
            **kwargs
        )

    def create_died(self, reason, **kwargs):
        """Create a died match.

        Params:
            reason: String or None
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["Died"],
            data=reason,
            **kwargs
        )

    def create_sold(self, **kwargs):
        """Create a sold match.

        Params:
            reason: String or None
        """
        return Match(
            db=self._db,
            type_id=match_types_by_name["Sold"],
            **kwargs
        )


class Match:

    def __init__(
        self, db, row=None, row_id=None, eid=None,
        account_id=None, account_link_id=None, lat=None, lon=None,
        time=None, created=None, type_id=None, data=None,
        bc_record=None, bc_hash=None
    ):
        """Match constructor."""
        self._db = db

        self._id = row_id
        self._eid = eid
        self._account_id = account_id
        self._account_link_id = account_link_id
        self._lat = lat
        self._lon = lon
        self._time = time
        self._created = created
        self._type_id = type_id
        self._data = data
        self._bc_record = bc_record
        self._bc_hash = bc_hash

        if row is not None:
            init_row = deepcopy(row)
            self._id = init_row["id"]
            self._eid = init_row["eid"]
            self._account_id = init_row["account"]
            self._account_link_id = init_row['account_link']
            self._lat = init_row['lat']
            self._lon = init_row['lon']
            self._time = init_row["time"]
            self._created = init_row["created"]
            self._type_id = init_row["type"]
            self._data = init_row["data"]
            self._bc_record = init_row["bc_record"]
            self._bc_hash = init_row["bc_hash"]

    def __eq__(self, other):
        """Evaluate if two matches are equal.

        This is used for unit testing.
        """
        return (
            self._id == other._id and
            self._eid == other._eid and
            self._account_id == other._account_id and
            self._account_link_id == other._account_link_id and
            self._lat == other._lat and
            self._lon == other._lon and
            self._time == other._time and
            self._created == other._created and
            self._type_id == other._type_id and
            self._data == other._data and
            self._bc_record == other._bc_record and
            self._bc_hash == other._bc_hash and
            self._db is other._db
        )

    def __repr__(self):
        """Turn self into a printable string, for debugging."""
        return (
            "<Match object id: " + str(id(self)) +
            " type: " + match_types_by_id[self.type_id] + " (" + str(self.type_id) + ")>"
        )

    def __str__(self):
        """Turn self into a big printable string, for debugging."""
        d = self.to_dict()
        for k in d:
            if "Mock" in repr(d[k]):
                d[k] = repr(d[k])
        return (
            repr(self) + ": " + json.dumps(d)
        )

    @property
    def id(self):
        """Gets match ID

        Returns:
            The match ID
        """
        return self._id

    @id.setter
    def id(self, var):
        """Sets match ID

        Params:
            var: The match ID
        """
        self._id = var

    @property
    def account_id(self):
        """Gets match account ID

        (This is the data owner)

        Returns:
            The account ID
        """
        return self._account_id

    @account_id.setter
    def account_id(self, var):
        """Sets account_id

        Params:
            var: The account_id
        """
        self._account_id = var

    @property
    def account_link_id(self):
        """Gets match account link ID

        (This is the account link that the data is associated with)

        Returns:
            The account link ID
        """
        return self._account_link_id

    @account_link_id.setter
    def account_link_id(self, var):
        """Sets account_link_id

        Params:
            var: The account_link_id
        """
        self._account_link_id = var

    @property
    def eid(self):
        """Gets match EID

        Returns:
            The match EID
        """
        return self._eid

    @eid.setter
    def eid(self, var):
        """Sets eid

        Params:
            var: The eid
        """
        self._eid = var

    @property
    def lat(self):
        """Gets match lattitude, if it exists

        Returns:
            The match lattitude, or None
        """
        return self._lat

    @lat.setter
    def lat(self, var):
        """Sets lattitude

        Params:
            var: The lattitude
        """
        self._lat = var

    @property
    def lon(self):
        """Gets match longitude, if it exists

        Returns:
            The match longitude, or None
        """
        return self._lon

    @lon.setter
    def lon(self, var):
        """Sets longitude

        Params:
            var: The longitude
        """
        self._lon = var

    @property
    def time(self):
        """Gets match time, if it exists

        (This was when the data was originally generated, so likely when the animal was scanned)

        Returns:
            The match time, or None
        """
        return self._time

    @time.setter
    def time(self, var):
        """Sets time

        Params:
            var: The time
        """
        self._time = var

    @property
    def created(self):
        """Gets match time created

        (This was the time when it was uploaded to the system)

        Returns:
            The match time created
        """
        return self._created

    @created.setter
    def created(self, var):
        """Sets created

        Params:
            var: The created
        """
        self._created = var

    @property
    def type_str(self):
        """Gets the type string

        Returns:
            The type of data (as a string)
        """
        return match_types_by_id[self._type_id]

    @property
    def type_id(self):
        """Gets the type ID

        Returns:
            The type of data (as an int)
        """
        return self._type_id

    @type_id.setter
    def type_id(self, var):
        """Sets type_id

        Params:
            var: The type_id
        """
        self._type_id = var

    @property
    def data(self):
        """Gets the raw match data

        Returns:
            The raw match data as unencoded json
        """
        return self._data

    @data.setter
    def data(self, var):
        """Sets data

        Params:
            var: The data
        """
        self._data = var

    def to_dict(self):
        """Returns the Match object as a dictionary in the match row format."""
        return {
            "id": self.id,
            "eid": self.eid,
            "account": self.account_id,
            "account_link": self.account_link_id,
            "lat": self.lat,
            "lon": self.lon,
            "time": self.time,
            "created": self.created,
            "type": self.type_id,
            "data": self.data
        }

    @property
    def row(self):
        """Returns the row data."""
        return self.to_dict()

    @property
    def bc_hash(self):
        """Returns the blockchain hash, as reported by the database.

        This is not generated per-request! Use generate_bc_hash to make a new one!
        """
        return self._bc_hash

    def generate_bc_hash(self):
        """Generates the blockchain hash, overriding internal value.

        Side effects:
            Changes self.bc_hash

        Returns:
            The hash.
        """
        temp = {
            "eid": self.eid,
            "lat": self.lat,
            "lon": self.lon,
            "time": self.time,
            "type": self.type_id,
            "data": self.data
        }

        for key in tuple(temp.keys()):
            value = temp[key]
            if value is None:
                del temp[key]

        self._bc_hash = sha256(json.dumps(
            temp,
            sort_keys=True,
            separators=(',', ':'),
            indent=0
        ).encode()).hexdigest().lower()

        return self._bc_hash

    @property
    def bc_record(self):
        """Returns the blockchain transaction ID containing this match's hash."""
        return self._bc_record

    @bc_record.setter
    def bc_record(self, var):
        """Sets the blockchain transaction ID containing this match's hash.

        Params:
            var: The transaction ID to set (a string of length 64)
        """
        self._bc_record = var
