from ...match_types import match_types_by_name


class MatchTypes:
    """Helpers for handling matches, specifically relating to various types."""

    def __init__(self, matches):
        self._matches = matches

    def insert_sighting(self, **kwargs):
        """Insert a sighting match.

        Params:
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Sighting"],
            **kwargs
        )

    def insert_visual_id(self, visual_id, **kwargs):
        """Insert a visual ID.

        Params:
            visual_id: A number or string of the visual ID
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Visual ID"],
            data=str(visual_id),
            **kwargs
        )

    def insert_born(self, unix, **kwargs):
        """Insert a 'born' match.

        Params:
            unix: The unix timestamp when the animal was born
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Born"],
            time=unix,
            **kwargs
        )

    def insert_weaned(self, unix, **kwargs):
        """Insert a 'weaned' match.

        Params:
            unix: The unix timestamp when the animal was weaned
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Weaned"],
            time=unix,
            **kwargs
        )

    def _generic_insert(
        self, eid, type_int, account, data=None, account_link=None, lat=None,
        lon=None, time=None, raw_identifier=None
    ):
        """Passes data to Matches.insert
        
        """
        self._matches.insert(
            eid=eid,
            type_int=type_int,
            data=data,
            account=account,
            account_link=account_link,
            lat=lat,
            lon=lon,
            time=time,
            raw_identifier=raw_identifier
        )
