from ...match_types import match_types_by_name
from . import matches


class MatchTypes:
    """Helpers for handling matches, specifically relating to various types.
    
    In general, **kwargs indicates:
        account, eid, lat, lon, 
    
    """

    def __init__(self, matches: 'matches.Matches'):
        self._matches = matches

    def insert_sighting(self, **kwargs):
        """Insert a sighting match.

        Params:
            kwargs: See _generic_insert
        """
        match = self._matches.get_matches(eid=kwargs["eid"], restrict_type=match_types_by_name["Sighting"],
                                        account_link=kwargs["account_link"], lat=kwargs["lat"], lon=kwargs["lon"], selectColumns=["id"])
        if len(match) > 0:
            print("Sighting match exists. Match ID: ", match[0]["id"])
        else:
            self._generic_insert(
                type_int=match_types_by_name["Sighting"],
                **kwargs
            )

    def insert_weaned(self, **kwargs):
        """Insert a 'weaned' match.

        Params:
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Weaned"],
            **kwargs
        )

    def insert_hot_weight(self, weight, **kwargs):
        """Insert a hot weight record (from the packer).

        Params:
            weight: The weight in pounds (number)
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Hot Weight"],
            data=float(weight),
            **kwargs
        )

    def insert_born(self, **kwargs):
        """Insert a born record.

        Params:
            kwargs: See _generic_insert
                Recommended: time
        """
        self._generic_insert(
            type_int=match_types_by_name["Born"],
            **kwargs
        )

    def insert_usda_yield_grade(self, grade, **kwargs):
        """Insert a yield grade record.

        Params:
            grade: The yield grade (number)
            kwargs: See _generic_insert
        """
        assert isinstance(grade, (float, int))
        self._generic_insert(
            type_int=match_types_by_name["USDA Yield Grade"],
            data=grade,
            **kwargs
        )

    def insert_usda_quality_grade(self, grade, **kwargs):
        """Insert a quality grade record.

        Params:
            grade: The quality grade (string)
            kwargs: See _generic_insert
        """
        assert isinstance(grade, str)
        self._generic_insert(
            type_int=match_types_by_name["USDA Quality Grade"],
            data=grade,
            **kwargs
        )

    def insert_medical(self, time, data, **kwargs):
        """Insert a medical record.

        Params:
            time: The time the medical event occurred (unix)
            data: A dictionary of medical data.
                product
                location
                symptom
                method
                fatal
                category
            kwargs: See _generic_insert
        """
        if not isinstance(data, dict):
            raise ValueError("data should be a dictionary")
        if time is None:
            raise ValueError("time should not be None")
        self._generic_insert(
            type_int=match_types_by_name["Medical"],
            time=time,
            data=data,
            **kwargs
        )

    def insert_railed(self, **kwargs):
        """Insert a railed record.

        Params:
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Railed"],
            **kwargs
        )

    def insert_packer(self, packer_str, **kwargs):
        """Insert a packer record.

        Params:
            packer_str: Temporary string format, see FeederResultsCSV
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Packer"],
            data=packer_str,
            **kwargs
        )

    def insert_died(self, reason, **kwargs):
        """Insert a died record.

        Params:
            reason: String or None
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Died"],
            data=reason,
            **kwargs
        )

    def insert_sold(self, **kwargs):
        """Insert a sold record.

        Params:
            kwargs: See _generic_insert
        """
        self._generic_insert(
            type_int=match_types_by_name["Sold"],
            **kwargs
        )

    def _generic_insert(
        self, eid, type_int, partner_account, visual_id=None, grouping_id=None, data=None, account_link=None, lat=None,
        lon=None, time=None, debug=None, api_insert=None, zip=None
    ):
        """Passes data to Matches.insert

        Params:
            data: json-serializable data
        """
        match = self._matches.get_matches(eid=eid, visual_id=visual_id, restrict_type=type_int, grouping_id=grouping_id, data=data, partner_account=partner_account,
                                            account_link=account_link, lat=lat, lon=lon, time=time, selectColumns=["id"])
        if len(match) > 0:
            print("Match exists. Match ID: ", match[0]["id"])
        else:
            # Insert a match only if match doesn't already exist
            self._matches.insert(
                eid=eid,
                visual_id=visual_id,
                type_int=type_int,
                grouping_id=grouping_id,
                data=data,
                partner_account=partner_account,
                account_link=account_link,
                lat=lat,
                lon=lon,
                time=time,
                zip=zip,
                debug=debug,
                api_insert=api_insert
            )
