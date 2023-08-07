import time as time_module
import json
from datetime import datetime
from core.database.no_value import NoValue
from ..frag import frag
from core.match_types import MATCH_TYPES_NAME_TO_ID
from ..objects.animal import Animal
from core.sectors import SECTORS_NAME_TO_ID

THREE_YEARS = 60 * 60 * 24 * 365 * 3
NO_VALUE = NoValue()


class MatchesException(Exception):
    """Matches generic exception."""

    def __init__(self, reason):
        """Constructor for MatchesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class Matches:

    _account_links_cols = ("id", "account", "affiliate_id", "company", "name", "sector", "partner_account")
    _account_links_clause = (
        ', ' + ', '.join(
            'account_links.' + a + ' AS "account_links.' + a + '"'
            for a in _account_links_cols
        )
    )

    def __init__(self, db):
        self._db = db
        self.types = MatchTypes(self)
        self._match_cols = ("id", "partner_account", "account_link", "eid", "visual_id", "grouping_id", "lat", "lon", "time", "created", "type"
                            "data", "bc_transaction_id", "bc_hash", "bc_upload")

    def get_animal_by_eid(self, eid):
        """Gets an animal object by their EID.

        Params:
            eid: the eid

        Returns:
            An Animal object
                Keep in mind that this object could be empty

        Raises:
            AnimalsException
        """
        return Animal(self._db, eid, self.get_matches_with_account_links(matches_eid=eid))

    def get_by_eids(self, eids, restrict_types=(), ljoin_account_links=False, ljoin_animals=False):
        """Gets matches by eids.

        Params:
            eids: the eids to find
            restrict_types: List of ids of types
            ljoin_account_links: Whether to left join account links

        Returns:
            A list (possibly empty) of matches rows
        """

        if not all(isinstance(t, int) for t in restrict_types):
            return MatchesException("Type should be integer")

        if not all(isinstance(eid, int) for eid in eids):
            return MatchesException("EID should be integer")

        query = (
            "SELECT matches.*" + (", animals.*" if ljoin_animals else "")
            + (Matches._account_links_clause if ljoin_account_links else "")
            + " FROM matches"
            + (" LEFT JOIN animals ON matches.eid = animals.eid" if ljoin_animals else "")
            + (" LEFT JOIN account_links on matches.account_link = account_links.id" if ljoin_account_links else "")
            + f" WHERE matches.eid IN ({','.join(str(eid) for eid in eids)})"
            + (f" AND matches.type IN ({','.join(str(t) for t in restrict_types)})" if restrict_types else "")
        )

        result = self._db.execute_d(query)
        return Matches._load_rows(result)

    def get_sightings_in_auction_house_feedlot_packer_stocker(self, account_ids, is_partner=False, as_count=False):
        if not all(isinstance(id, int) for id in account_ids):
            raise Exception("Incorrect input for account ids")

        if as_count:
            select_clause = "SELECT COUNT(DISTINCT m1.eid) AS count"
            third_matches_clause = ""
        else:
            select_clause = "SELECT m3.*"
            third_matches_clause = "LEFT JOIN matches m3 on m1.eid = m3.eid"

        sectors_clause = f"""({SECTORS_NAME_TO_ID['Auction']},{SECTORS_NAME_TO_ID['Feedlot']},
                              {SECTORS_NAME_TO_ID['Packer']},{SECTORS_NAME_TO_ID['Stocker/Backgrounder']})"""

        first_account_link_clause = ""
        if not is_partner:
            first_account_link_clause = f"al1.account = {account_ids[0]}"
        else:
            if len(account_ids) > 0:
                first_account_link_clause = f"al1.account IN ({','.join([str(id) for id in account_ids])})"

        if first_account_link_clause:
            match_rows = self._db.execute_d(
                f"""
                {select_clause} FROM matches m1
                INNER JOIN account_links al1 on al1.id = m1.account_link
                INNER JOIN matches m2 ON m1.eid = m2.eid
                INNER JOIN account_links al2 on al2.id = m2.account_link
                {third_matches_clause}
                WHERE {first_account_link_clause} AND m1.type = %(sighting_type)s AND m2.type = %(sighting_type)s
                AND al2.sector IN {sectors_clause}
                ORDER BY m1.eid
                """,
                {
                    "sighting_type": MATCH_TYPES_NAME_TO_ID["Sighting"]
                }
            )
        else:
            match_rows = []

        if as_count:
            return match_rows[0]["count"] if match_rows else 0
        else:
            return [x for x in Matches._convert_eid_data_for_export(match_rows).values()]

    def get_distinct_match_locations_for_account(self, account_id, restrict_types=(), is_partner=False):
        query_statements = [
            """
            SELECT DISTINCT m1.lat, m1.lon, al1.name AS 'account_links.name',
            al1.sector AS 'account_links.sector' FROM matches m1
            INNER JOIN account_links al1 ON m1.account_link = al1.id
            INNER JOIN matches m2 ON m1.eid=m2.eid
            INNER JOIN account_links al2 ON m2.account_link=al2.id
            """
        ]

        if is_partner:
            account_link_clause = "WHERE al2.partner_account = %s"
        else:
            account_link_clause = "WHERE al2.account = %s"
        query_statements.append(account_link_clause)
        args = [account_id]

        if len(restrict_types) > 0:
            in_clause = ', '.join(list(map(lambda x: '%s', restrict_types)))
            type_clause = f"AND m1.type IN ({in_clause})"
            query_statements.append(type_clause)
            args += restrict_types

        query = " ".join(query_statements)
        matches = self._db.execute_d(query, args)
        return matches

    def get_sighted_match_accounts_for_account_link(self, account_link_id, sector_id=NO_VALUE):
        """Gets all the accounts that were matched to account_link_id based on given type

        Params:
            account_link_id: The user's account link ID
            type: Type based on 'match_types.py' file

        Returns:
            A list of all the accounts that were matched for an account with given type.
        """
        query_statements = ["""
            SELECT al.account as account_id, al.id as account_link_id,
            min(m1.created_timestamp) as date, al.sector as account_sector_id,
            min(m1.eid) AS eid, al.name as account_name, count(m2.eid) as 'count' FROM matches AS m1
            INNER JOIN account_links AS al ON m1.account_link=al.id
            INNER JOIN matches m2 ON m1.eid = m2.eid
            WHERE m2.account_link = %(account_link_id)s and m2.type=%(type)s
            AND m1.type=%(type)s AND al.account IS NOT NULL
        """]
        query_values = {
                "type": MATCH_TYPES_NAME_TO_ID['Sighting'],
                "account_link_id": account_link_id
        }

        if sector_id is not NO_VALUE:
            query_statements.append("AND al.sector=%(sector_id)s")
            query_values["sector_id"] = sector_id

        query_statements.append("""
            GROUP BY al.account, al.sector, al.name, al.id
            ORDER BY al.sector, date
        """)
        query = " ".join(query_statements)
        return self._db.execute_d(query, query_values)

    def get_common_eid_data(self, first_account_link_id, second_account_link_id):
        """Gets the EIDs sighted at two accounts

        Params:
            first_account_link_id: account link of 1st account
            second_account_link_id: account link of 2nd account

        Returns:
            A list of dictionaries
        """
        # m3 will contain all match rows for the eids
        match_rows = self._db.execute_d(
            """
            SELECT m3.* FROM matches m1 INNER JOIN matches m2 ON m1.eid = m2.eid
            LEFT JOIN matches m3 ON m1.eid = m3.eid
            WHERE m1.type = %(match_type_id)s AND m1.account_link = %(first_account_link_id)s
            AND m2.account_link = %(second_account_link_id)s AND m2.type = %(match_type_id)s
            """,
            {
                "match_type_id": MATCH_TYPES_NAME_TO_ID["Sighting"],
                "first_account_link_id": first_account_link_id,
                "second_account_link_id": second_account_link_id
            }
        )
        return [x for x in Matches._convert_eid_data_for_export(match_rows).values()]

    def get_count_distribution_two_accounts(self, match_type_id, first_account_link_id, second_account_link_id):
        """Gets the count of each data type for eids sighted at two accounts

        Params:
            match_type_id: The type as an int
            first_account_link_id: account link of 1st account
            second_account_link_id: account link of 2nd account

        Returns:
            A list of dictionaries
                Keys
                    data: value of data
                    count: The number of times data existed
        """

        return Matches._load_rows(self._db.execute_d(
            """
                SELECT m1.data, count(distinct m1.eid) as 'count' from matches m1
                INNER JOIN matches m2 on m1.eid = m2.eid
                INNER JOIN matches m3 on m1.eid = m3.eid
                WHERE m1.type=%(match_type_id)s AND m2.account_link = %(first_account_link_id)s
                AND m3.account_link = %(second_account_link_id)s
                GROUP BY m1.data
            """,
            {
                "match_type_id": match_type_id,
                "first_account_link_id": first_account_link_id,
                "second_account_link_id": second_account_link_id
            }
        ))

    def get_matches(self, eid=NO_VALUE, visual_id=NO_VALUE, restrict_type=NO_VALUE, grouping_id=NO_VALUE, partner_account=NO_VALUE,
        account_link=NO_VALUE, lat=NO_VALUE, lon=NO_VALUE, visual_id_has_value=NO_VALUE, data=NO_VALUE, time=NO_VALUE, use_distinct=False,
        selectColumns=()):
        """
        Get an account by the values specified.

        Returns:
            A list of account(s) record if found else []
        """

        if len(selectColumns) > 0:
            incorrect_cols = [col for col in selectColumns if col not in self._match_cols]

            if len(incorrect_cols) > 0:
                raise MatchesException("Selected column(s) " + ",".join(incorrect_cols) + " don't exist in match table")

            base_query = "SELECT "
            if use_distinct:
                base_query += "DISTINCT "
            base_query += ",".join(selectColumns) + " FROM matches"
        else:
            base_query = "SELECT * FROM matches"

        query_conditions = []
        query_values = {}

        if eid is not NO_VALUE:
            query_conditions.append("eid = %(eid)s" if eid is not None else "eid IS %(eid)s")
            query_values["eid"] = eid

        if visual_id is not NO_VALUE:
            query_conditions.append("visual_id = %(visual_id)s" if visual_id is not None else "visual_id IS %(visual_id)s")
            query_values["visual_id"] = visual_id

        if visual_id_has_value != NO_VALUE:
            if visual_id_has_value is True:
                query_conditions.append("visual_id IS NOT NULL")
            elif visual_id_has_value is False:
                query_conditions.append("visual_id IS NULL")

        if restrict_type is not NO_VALUE:
            query_conditions.append("type = %(restrict_type)s" if restrict_type is not None else "type IS %(restrict_type)s")
            query_values["restrict_type"] = restrict_type

        if grouping_id is not NO_VALUE:
            query_conditions.append("grouping_id = %(grouping_id)s" if grouping_id is not None else "grouping_id IS %(grouping_id)s")
            query_values["grouping_id"] = grouping_id

        if partner_account is not NO_VALUE:
            query_conditions.append("partner_account = %(partner_account)s" if partner_account is not None else "partner_account IS %(partner_account)s")
            query_values["partner_account"] = partner_account

        if account_link is not NO_VALUE:
            query_conditions.append("account_link = %(account_link)s" if account_link is not None else "account_link IS %(account_link)s")
            query_values["account_link"] = account_link

        if lat is not NO_VALUE:
            query_conditions.append("lat = %(lat)s" if lat is not None else "lat IS %(lat)s")
            query_values["lat"] = lat

        if lon is not NO_VALUE:
            query_conditions.append("lon = %(lon)s" if lon is not None else "lon IS %(lon)s")
            query_values["lon"] = lon 
        
        if data is not NO_VALUE:
            query_conditions.append("data = CAST(%(data)s AS JSON)" if data is not None else "data IS %(data)s")
            query_values["data"] = json.dumps(data) if data is not None else None

        if time is not NO_VALUE:
            query_conditions.append("time = %(time)s" if time is not None else "time IS %(time)s")
            query_values["time"] = time

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        match_rows = self._db.execute_d(query, query_values)
        if len(match_rows) > 0:
            for row in match_rows:
                if "data" in row:
                    row["data"] = json.loads(row["data"]) if row["data"] else None
                if "debug" in row:
                    row["debug"] = json.loads(row["debug"]) if row["debug"] else None
            return match_rows
        else:
            return []

    def get_matches_with_account_links(self, matches_eid=NO_VALUE, matches_eids=NO_VALUE, matches_visual_id=NO_VALUE,
                                       matches_restrict_type=NO_VALUE, matches_order_by=NO_VALUE,
                                       matches_sort_by=NO_VALUE, account_links_sector=NO_VALUE,
                                       account_links_account_id=NO_VALUE, matches_partner_account_id=NO_VALUE,
                                       is_distinct=False, matches_cols=(), account_links_multiple_account_ids=(),
                                       account_links_partner_account=NO_VALUE):
        """
        Get matches with account_links (if any) by the values specified. If no account_links exist for a match,
        only the match is returned

        Returns:
            A list of matches and account_links record if found else []
        """

        if is_distinct:
            base_query = "SELECT distinct"
        else:
            base_query = "SELECT"

        if len(matches_cols) > 0:
            incorrect_cols = [col for col in matches_cols if col not in self._match_cols]

            if len(incorrect_cols) > 0:
                raise MatchesException("Selected column(s) " + ",".join(incorrect_cols) + " don't exist in matches table")

            base_query += " " + ",".join("m." + c for c in matches_cols)
        else:
            base_query += " *"

        base_query += " FROM matches m LEFT JOIN account_links al ON m.account_link=al.id "

        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if matches_eid is not NO_VALUE:
            query_conditions.append("m.eid = %(matches_eid)s" if matches_eid is not None else "m.eid IS %(matches_eid)s")
            query_values["matches_eid"] = matches_eid
        elif matches_eids is not NO_VALUE:
            if not all(isinstance(eid, int) for eid in matches_eids):
                raise MatchesException("Not all EIDs are integers") 
            query_conditions.append(f"m.eid IN ({','.join([str(match) for match in matches_eids])})")
        if matches_visual_id is not NO_VALUE:
            query_conditions.append("m.visual_id = %(matches_visual_id)s" if matches_visual_id is not None else "m.visual_id IS %(matches_visual_id)s")
            query_values["matches_visual_id"] = matches_visual_id

        if matches_restrict_type is not NO_VALUE:
            query_conditions.append("m.type = %(matches_restrict_type)s" if matches_restrict_type is not None else "m.type IS %(matches_restrict_type)s")
            query_values["matches_restrict_type"] = matches_restrict_type

        if matches_partner_account_id is not NO_VALUE:
            query_conditions.append("m.partner_account = %(matches_partner_account_id)s" if matches_partner_account_id is not None else "m.partner_account IS %(matches_partner_account_id)s")
            query_values["matches_partner_account_id"] = matches_partner_account_id

        if account_links_sector is not NO_VALUE:
            query_conditions.append("al.sector = %(account_links_sector)s" if account_links_sector is not None else "al.sector IS %(account_links_sector)s")
            query_values["account_links_sector"] = account_links_sector

        if account_links_partner_account is not NO_VALUE:
            query_conditions.append("al.partner_account = %(account_links_partner_account)s" if account_links_partner_account is not None else "al.partner_account IS %(account_links_partner_account)s")
            query_values["account_links_partner_account"] = account_links_partner_account

        # cannot pass values for both account_links_account_id AND account_links_multiple_account_ids
        if account_links_account_id is not NO_VALUE:
            query_conditions.append("al.account = %(account_links_account_id)s" if account_links_account_id is not None else "al.account IS %(account_links_account_id)s")
            query_values["account_links_account_id"] = account_links_account_id
        elif len(account_links_multiple_account_ids) > 0:
            if all(isinstance(i, int) for i in account_links_multiple_account_ids):
                query_conditions.append("al.account IN (" + ",".join(str(i) for i in account_links_multiple_account_ids) + ")")
            else:
                raise MatchesException("Not all the Account Ids in account_links_multiple_account_ids are integers")

        if matches_order_by is not NO_VALUE:
            if matches_order_by not in self._match_cols:
                raise MatchesException("order_by column doesn't exist")
            order_by_clause = "ORDER BY m." + matches_order_by
            if matches_sort_by is not NO_VALUE:
                if matches_sort_by not in ("ASC", "DESC"):
                    raise MatchesException("Incorrect value for sort_by")
                order_by_clause += " " + matches_sort_by

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions) + " " + order_by_clause
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        result_rows = self._db.execute_d(query, query_values)
        if len(result_rows) > 0:
            return result_rows
        else:
            return []

    def insert(
        self, eid, type_int, visual_id=None, grouping_id=None, data=None, partner_account=None, account_link=None,
        lat=None, lon=None, time=None, debug=None, api_insert=None, bc_transaction_id=None, bc_hash=None, zip=None
    ):
        """Insert a new row into matches.

        Params:
            eid: The animal ID, int (required)
            type_int: The match type, int (required)
            data: The match data (optional)
                If None is provided (default), NULL is inserted
                Else it is json-encoded and put in the record
            partner_account: The data owner, int (optional)
            account_link: The account link, int (optional)
            lat: The lattitude of the data scan, int (optional)
            lon: The longitude of the data scan, int (optional)
            time: The time of the data scan, int (optional)
            debug: debug usage, str (optional)
        """

        self._db.execute(
            """INSERT INTO matches
                (eid, type, visual_id, grouping_id, data, partner_account, account_link, lat, lon, time, created, debug, api_insert, bc_transaction_id, bc_hash, zip)
                VALUES
                    (%(eid)s, %(type)s, %(visual_id)s, %(grouping_id)s, %(data)s, %(partner_account)s, %(account_link)s, %(lat)s, %(lon)s, %(time)s,
                     %(created)s, %(debug)s, %(api_insert)s, %(bc_transaction_id)s, %(bc_hash)s, %(zip)s
                    )
            """,
            {
                "eid": eid,
                "type": type_int,
                "visual_id": visual_id,
                "grouping_id": grouping_id,
                "data": None if data is None else json.dumps(data),
                "partner_account": partner_account,
                "account_link": account_link,
                "lat": lat,
                "lon": lon,
                "time": time,
                "created": int(time_module.time()),
                "debug": None if debug is None else json.dumps(debug),
                "api_insert": api_insert,
                "bc_transaction_id": bc_transaction_id,
                "bc_hash": bc_hash,
                "zip": zip
            }
        )

        return self._db.last_row_id()

    def update_match(self, id, visual_id=NO_VALUE, grouping_id=NO_VALUE, data=NO_VALUE, zip_code=NO_VALUE,
                     lat=NO_VALUE, lon=NO_VALUE, partner_account=NO_VALUE, time=NO_VALUE, debug=NO_VALUE,
                     api_insert=NO_VALUE):
        """
        Updates an match.
        """
        base_query = "UPDATE matches"

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if visual_id is not NO_VALUE:
            query_conditions.append("visual_id = %(visual_id)s")
            query_values["visual_id"] = visual_id
        if grouping_id is not NO_VALUE:
            query_conditions.append("grouping_id = %(grouping_id)s")
            query_values["grouping_id"] = grouping_id
        if data is not NO_VALUE:
            query_conditions.append("data = %(data)s")
            query_values["data"] = json.dumps(data) if data is not None else None
        if partner_account is not NO_VALUE:
            query_conditions.append("partner_account = %(partner_account_id)s")
            query_values["partner_account_id"] = partner_account
        if time is not NO_VALUE:
            query_conditions.append("time = %(time)s")
            query_values["time"] = time
        if debug is not NO_VALUE:
            query_conditions.append("debug = %(debug)s")
            query_values["debug"] = json.dumps(debug) if debug is not None else None
        if api_insert is not NO_VALUE:
            query_conditions.append("api_insert = %(api_insert)s")
            query_values["api_insert"] = api_insert
        if zip_code is not NO_VALUE:
            query_conditions.append("zip = %(zip_code)s")
            query_values["zip_code"] = zip_code
        if lat is not NO_VALUE:
            query_conditions.append("lat = %(lat)s")
            query_values["lat"] = lat
        if lon is not NO_VALUE:
            query_conditions.append("lon = %(lon)s")
            query_values["lon"] = lon

        if len(query_conditions) >= 1:
            combined_query_condition = f" SET {', '.join(query_conditions)}  WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Account")

    def get_count_eid_distinct(self):
        """Count the number of distinct EIDs in the database.

        Returns:
            The value
        """
        self._db.execute(
            """
            SELECT
                COUNT(DISTINCT eid) AS 'count'
            FROM
                matches
            """
        )
        return self._db.fetch_all()[0]['count']

    def get_count_eid_distinct_sighted(self):
        """Count the number of distinct EIDs in the database which have been sighted at either feedlot, auction,
        packer, buyer, stocker/backgrounder.

        Returns:
            The value
        """
        sectors_clause = f"""({SECTORS_NAME_TO_ID['Auction']},{SECTORS_NAME_TO_ID['Feedlot']},
                              {SECTORS_NAME_TO_ID['Packer']}, {SECTORS_NAME_TO_ID['Stocker/Backgrounder']})"""
        rows = self._db.execute_d(
            f"""
            SELECT COUNT(DISTINCT m1.eid) AS count FROM matches m1
            INNER JOIN matches m2 ON m1.eid = m2.eid
            INNER JOIN account_links al1 on al1.id = m1.account_link
            INNER JOIN account_links al2 on al2.id = m2.account_link
            WHERE  m1.type = 1 AND (al1.sector = {SECTORS_NAME_TO_ID["Cow-Calf"]} OR al1.sector IS NULL)
            AND m2.type = 1 AND al2.sector IN {sectors_clause}
            """
        )
        return rows[0]['count']

    def get_ils_eids(self):
        """Get EIDs that ILS still needs to process in the database.

        Returns:
            Tuple of the eids
        """
        self._db.exec_frag(
            frag(
                """
                SELECT
                    eid
                FROM
                    matches
                GROUP BY eid
                """,
                frag(
                    "HAVING",
                    frag(
                        "MAX(created) >= :window_start",
                        window_start=time_module.time() - THREE_YEARS
                    ),
                    "AND",
                    frag(
                        """
                            MAX(IF(type=:usda_quality_grade_type,1,0))=0
                        """,
                        usda_quality_grade_type=MATCH_TYPES_NAME_TO_ID[
                            "USDA Quality Grade"
                        ]
                    )
                )
            )
        )

        # Data from last 3 years, and USDAQualityGrade
        return tuple(
            row['eid'] for row in
            self._db.fetch_all()
        )

    def get_distinct_eids_and_visual_ids_by_account(self, account_id, number_of_years):
        """Return the distinct EIDs in the database for an account.

        Params:
            account_id: The account to generate data on
            number_of_years: Age of records

        Returns:
            The array of distinct eids
        """
        return self._db.execute_d(
                """
                SELECT DISTINCT eid, visual_id
                FROM matches
                WHERE account_link IN (
                    SELECT id FROM account_links WHERE account=%(account)s
                ) AND YEAR(current_timestamp) > YEAR(current_date())-%(number_of_years)s
                """, {
                    "account": account_id,
                    "number_of_years": number_of_years
                }
        )

    def get_count_eid_distinct_for_accounts(self, account_ids=(), is_partner=False):
        """Count the number of distinct EIDs in the database for an account.

        Params:
            account_ids: The account(s) to generate data on

        Returns:
            The value
        """
        if not all(isinstance(id, int) for id in account_ids):
            raise Exception("Incorrect input for account ids")

        query = """
            SELECT COUNT(DISTINCT eid) AS 'count'
            FROM matches m INNER JOIN account_links al ON m.account_link = al.id
        """
        condition = ""
        if not is_partner:
            condition = f" AND al.account = {account_ids[0]}"
        else:
            if len(account_ids) > 0:
                condition = f" AND al.account IN ({','.join([str(id) for id in account_ids])})"

        if condition:
            return self._db.execute_d(
                query + " WHERE m.type= %(sighting_type)s" + condition,
                {
                    "sighting_type": MATCH_TYPES_NAME_TO_ID["Sighting"]
                }
            )[0]["count"]
        else:
            return 0

    def get_count_distribution(self, type_int=None, account_id=None, is_partner=False, affiliated_accounts=()):
        """Gets the count of each data type for an account

        Params:
            type_int: The type as an int
            account_links: Query on only a set of account links (spread)
            partner_id: partner id if any
            is_partner: whether report is generated for a partner account

        Returns:
            A list of dictionaries
                Keys
                    data: Int value of data or string if join_str is set
                    count: The number of times data existed
        """
        if type_int:
            account_link_condition = ""
            if is_partner:
                if len(affiliated_accounts) > 0:
                    account_link_condition = f"""
                        AND al.account IN ({','.join([str(account['id']) for account in affiliated_accounts])})
                    """
            else:
                account_link_condition = " AND al.account = %(account_id)s"

            if account_link_condition:
                return Matches._load_rows(self._db.execute_d(
                    """
                    SELECT m1.data, COUNT(distinct m1.eid) as 'count' FROM matches m1
                    INNER JOIN matches m2 ON m1.eid = m2.eid
                    INNER JOIN account_links al ON m2.account_link = al.id
                    WHERE m1.type = %(type_id)s""" + account_link_condition + """
                    GROUP BY m1.data
                    """,
                    {
                        "type_id": type_int,
                        "account_id": account_id
                    }
                ))
            else:
                return []
        else:
            if is_partner:
                # get yield, quality and sightings
                result = {}
                for account in affiliated_accounts:
                    account_result = {}
                    quality_distribution = self.get_count_distribution(MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"], account_id=account["id"])
                    account_result["quality_distribution"] = {x['data']: x['count'] for x in quality_distribution}
                    yield_distribution = self.get_count_distribution(MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"], account_id=account["id"])
                    account_result["yield_distribution"] = {x['data']: x['count'] for x in yield_distribution}
                    account_result["sightings"] = self.get_sightings_in_auction_house_feedlot_packer_stocker(
                        (account["id"],), False, True
                    )
                    account_result["account_id"] = account["id"]
                    result[account["name"]] = account_result
                return result

    def get_count_distribution_global(self, type_int):
        """Gets the count of each data type for global

        Params:
            type_int: The type as an int

        Returns:
            A list of dictionaries
                Keys
                    data: Int value of data or string if join_str is set
                    count: The number of times data existed
        """
        return Matches._load_rows(self._db.exec_frag_d(
            frag(
                """
                    SELECT
                        data, COUNT(*) as 'count'
                    FROM
                        matches
                    WHERE
                        type=:type
                    GROUP BY
                        data
                """,
                type=type_int
            )
        ))

    def get_by_auction_sale_account(self, account_id, restrict_types, ljoin_account_links):
        """Gets matches associated with an auction sale.

        Params:
            account_id: Account ID to get auction sales from
            restrict_types: Types to restrict results to
            ljoin_account_links: Whether to ljoin account links (ignored)

        Returns:
            A list of rows

            Enhances with account_links.company, account_links.sector
        """

        return Matches._load_rows(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._account_links_clause if ljoin_account_links else "",
                """
                    FROM auction_sales
                    LEFT JOIN sales_groups ON sales_groups.auction_sale=auction_sales.id
                    LEFT JOIN eid_group_eids ON eid_group_eids.eid_group=sales_groups.eid_group
                    LEFT JOIN matches ON eid_group_eids.eid=matches.eid
                    LEFT JOIN account_links ON matches.account_link=account_links.id
                """,
                frag(
                    "WHERE auction_sales.account=:account_id",
                    account_id=account_id
                ),
                frag(
                    "AND matches.type IN :types",
                    types=restrict_types
                ) if restrict_types else ""
            )
        ))

    def get_matches_by_eid_or_visual_id(self, eid_or_visual_id, account_ids=()):
        """Gets matches data associated with a eid or visual id if it belongs to any of the accounts passed in account_ids.

        Params:
            eid_or_visual_id: The eid or visual id to look up
            account_ids: list of account(s)

        Returns:
            All the matches joined with account_links table rows
        """
        matches = []

        if len(account_ids) == 0:
            matches = self.get_matches_with_account_links(matches_eid=eid_or_visual_id, is_distinct=True, matches_cols=("eid",))

            if len(matches) == 0:
                matches = self.get_matches_with_account_links(matches_visual_id=eid_or_visual_id, is_distinct=True, matches_cols=("eid", "visual_id"))

        else:
            matches = self.get_matches_with_account_links(
                matches_eid=eid_or_visual_id, account_links_multiple_account_ids=account_ids,
                is_distinct=True, matches_cols=("eid",)
            )

            if len(matches) == 0:
                matches = self.get_matches_with_account_links(
                    matches_visual_id=eid_or_visual_id, account_links_multiple_account_ids=account_ids,
                    is_distinct=True, matches_cols=("eid", "visual_id")
                )
        return matches

    def get_count_distribution_for_sector_at_account(self, account_id, sector_id):
        """
        Used by report
        Returns:
            A dictionary of dictionaries
                Keys
                    both: result for both accounts (can be empty)
                    self: result for single account (can be empty)
        """
        result = {}
        sighted_eid_data = {}
        all_eid_data = {}
        if len(account_links := self._db.account_links.get_account_links(account_id=account_id)) > 0:
            related_account_details = self.get_sighted_match_accounts_for_account_link(
                account_link_id=account_links[0]['id'], sector_id=sector_id
            )

            for account_detail in related_account_details:
                account_result = {}
                account_result["quality_distribution"] = {x['data']: x['count'] for x in
                                                          self.get_count_distribution_two_accounts(
                                                            MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"],
                                                            account_links[0]['id'],
                                                            account_detail["account_link_id"])}
                account_result["yield_distribution"] = {x['data']: x['count'] for x in
                                                        self.get_count_distribution_two_accounts(
                                                            MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"],
                                                            account_links[0]['id'],
                                                            account_detail["account_link_id"])}
                account_result["account_id"] = account_detail["account_id"]
                account_result["sightings"] = account_detail["count"]
                sighted_eid_data[account_detail["account_name"]] = account_result

                account_result = {}
                quality_distribution = self.get_count_distribution(MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"], account_id=account_detail["account_id"])
                account_result["quality_distribution"] = {x['data']: x['count'] for x in quality_distribution}
                yield_distribution = self.get_count_distribution(MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"], account_id=account_detail["account_id"])
                account_result["yield_distribution"] = {x['data']: x['count'] for x in yield_distribution}
                account_result["sightings"] = self.get_sightings_in_auction_house_feedlot_packer_stocker(
                    (account_detail["account_id"],), False, True
                )
                account_result["account_id"] = account_detail["account_id"]
                all_eid_data[account_detail["account_name"]] = account_result

        result['matched_data'] = sighted_eid_data
        result['all_data'] = all_eid_data
        return result

    @staticmethod
    def _load_rows(rows):
        """Parses returned JSON from mysql"""
        for row in rows:
            if row['data'] is not None:
                row['data'] = json.loads(row['data'])
        return rows

    @staticmethod
    def _convert_eid_data_for_export(match_rows):
        all_eid_data = {}
        for row in match_rows:
            if row["eid"] not in all_eid_data.keys():
                current_eid_data = {"eid": row["eid"]}
            else:
                current_eid_data = all_eid_data[row["eid"]]
            if row["type"] == MATCH_TYPES_NAME_TO_ID["Sighting"] and row["visual_id"]:
                current_eid_data["visual_id"] = row["visual_id"]

            if row["type"] == MATCH_TYPES_NAME_TO_ID["Weaned"]:
                current_eid_data["wean_date"] = datetime.utcfromtimestamp(row['time']).strftime('%Y-%m-%d %H:%M:%S')
                data = json.loads(row["data"]) if row["data"] is not None else {}
                current_eid_data["creep_feed"] = data.get("creep_feed", None)
                current_eid_data["first_14_day_feed_method"] = data.get("first_14_method", None)
                current_eid_data["second_31_day_feed_method"] = data.get("second_31_method", None)
                current_eid_data["weaning_strategy"] = data.get("at", None)
                current_eid_data["wean_weight"] = data.get("wean_weight", None)

            if row["type"] == MATCH_TYPES_NAME_TO_ID["Sold"]:
                current_eid_data["marketing_date"] = datetime.utcfromtimestamp(row['time']).strftime('%Y-%m-%d %H:%M:%S') if row["time"] is not None else ""
                data = json.loads(row["data"]) if row["data"] is not None else {}
                current_eid_data["marketing_method_name"] = data.get("method", None)
                current_eid_data["sale_location"] = data.get("location", None)
                current_eid_data["number_of_calves"] = data.get("group_size", None)

            if row["type"] == MATCH_TYPES_NAME_TO_ID["Hot Weight"]:
                current_eid_data["hot_weight"] = row['data']

            if row["type"] == MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"]:
                current_eid_data["quality_grade"] = row['data']

            if row["type"] == MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"]:
                current_eid_data["yield_grade"] = row['data']

            all_eid_data[row["eid"]] = current_eid_data
        return all_eid_data


class MatchTypes:
    """Helpers for handling matches, specifically relating to various types.

    In general, **kwargs indicates:
        account, eid, lat, lon,

    """

    def __init__(self, matches: 'Matches'):
        self._matches = matches
        self._db = matches._db

    def insert_sighting(self, **kwargs):
        """Insert a sighting match.

        Params:
            kwargs: See _generic_insert
        """
        match = self._matches.get_matches(eid=kwargs["eid"], restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
                                        account_link=kwargs["account_link"], lat=kwargs["lat"], lon=kwargs["lon"], selectColumns=["id"])
        if len(match) > 0:
            print("Sighting match exists. Match ID: ", match[0]["id"])
            return 0
        else:
            return self._generic_insert(
                type_int=MATCH_TYPES_NAME_TO_ID["Sighting"],
                **kwargs
            )

    def insert_weaned(self, **kwargs):
        """Insert a 'weaned' match.

        Params:
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Weaned"],
            **kwargs
        )

    def insert_hot_weight(self, weight, **kwargs):
        """Insert a hot weight record (from the packer).

        Params:
            weight: The weight in pounds (number)
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Hot Weight"],
            data=float(weight),
            **kwargs
        )

    def insert_born(self, **kwargs):
        """Insert a born record.

        Params:
            kwargs: See _generic_insert
                Recommended: time
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Born"],
            **kwargs
        )

    def insert_usda_yield_grade(self, grade, **kwargs):
        """Insert a yield grade record.

        Params:
            grade: The yield grade (number)
            kwargs: See _generic_insert
        """
        assert isinstance(grade, (float, int))

        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"],
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
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"],
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
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Medical"],
            time=time,
            data=data,
            **kwargs
        )

    def insert_railed(self, **kwargs):
        """Insert a railed record.

        Params:
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Railed"],
            **kwargs
        )

    def insert_packer(self, packer_str, **kwargs):
        """Insert a packer record.

        Params:
            packer_str: Temporary string format, see FeederResultsCSV
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Packer"],
            data=packer_str,
            **kwargs
        )

    def insert_died(self, reason, **kwargs):
        """Insert a died record.

        Params:
            reason: String or None
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Died"],
            data=reason,
            **kwargs
        )

    def insert_sold(self, **kwargs):
        """Insert a sold record.

        Params:
            kwargs: See _generic_insert
        """
        return self._generic_insert(
            type_int=MATCH_TYPES_NAME_TO_ID["Sold"],
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
            return 0
        else:
            # Insert a match only if match doesn't already exist
            return self._matches.insert(
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
