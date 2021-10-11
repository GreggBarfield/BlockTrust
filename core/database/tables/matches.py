import time as time_module
import json
from ..frag import frag
from .match_types import MatchTypes
from core.match_types import match_types_by_name


THREE_YEARS = 60 * 60 * 24 * 365 * 5


class MatchesException(Exception):
    """Matches generic exception."""

    def __init__(self, reason):
        """Constructor for MatchesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class Matches:

    _account_links_cols = ("id", "account", "affiliate_id", "company", "sector", "partner_account")
    _account_links_clause = (
        ', ' + ', '.join(
            'account_links.' + a + ' AS "account_links.' + a + '"'
            for a in _account_links_cols
        )
    )

    _select_visibility = """
        ,matches_type_visibility.visibility
    """
    _left_join_visibility = """
        LEFT JOIN matches_type_visibility ON
            matches.partner_account=matches_type_visibility.account AND
                matches.type=matches_type_visibility.type
    """

    def __init__(self, db):
        self.types = MatchTypes(self)
        self._db = db

    def get_by_eids(self, eids, restrict_types=(), ljoin_account_links=False):
        """Gets matches by eids.

        Params:
            eids: the eids to find
            restrict_types: List of ids of types
            ljoin_account_links: Whether to left join account links

        Returns:
            A list (possibly empty) of matches rows
        """
        return Matches._load_rows(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._select_visibility,
                Matches._account_links_clause if ljoin_account_links else "",
                "FROM matches",
                frag(
                    "LEFT JOIN account_links ON matches.account_link = account_links.id",
                ) if ljoin_account_links else "",
                Matches._left_join_visibility,
                frag(
                    "WHERE matches.eid IN (:eid)",
                    eid=eids
                ),
                frag(
                    "AND matches.type IN (:types)",
                    types=restrict_types
                ) if restrict_types else ""
            )
        ))
    
    def get_animals_with_data_for_account(self, account_link_id=0): 
        if account_link_id > 0:
            matches = self._db.execute_d(
                """
                SELECT DISTINCT m1.eid, m3.visual_id FROM matches m1 
                INNER JOIN matches m2 ON m1.eid = m2.eid 
                LEFT JOIN matches m3 ON m1.eid = m3.eid AND m3.visual_id IS NOT NULL
                WHERE m1.account_link = %(account_link_id)s AND m2.type = %(type)s
                """,
                {
                    "account_link_id": account_link_id,
                    "type": match_types_by_name["USDA Quality Grade"]
                }
            )
            return matches
        else:
            return []

    def get_all_matches_for_an_account(self, account_link_id=0, restrict_types=(), ljoin_account_links=False, match_cols=[]):
        """Gets all matches by an account.

        Params:
            account_links: all the account links of an account (should be 1)
            restrict_types: match types
            ljoin_account_links: Whether to left join account links
            match_cols: optional specify the columns needed from the matches table

        Returns:
            A list of dictionaries containing matches and account_links data if joined (possibly empty)
            No duplicates
        """
        if account_link_id > 0:
            match_columns_query = ",".join(list(map(lambda c: "matches." + c, match_cols)))
            #account_link_ids = [al.id() for al in account_links]

            query_statements = []
            query_statements.append("SELECT " + ("matches.*" if match_columns_query == "" else match_columns_query))
            query_statements.append(Matches._account_links_clause if ljoin_account_links else "")
            query_statements.append("FROM matches" + (" LEFT JOIN account_links ON matches.account_link = account_links.id" if ljoin_account_links else ""))

            al_clause = "WHERE eid in (SELECT DISTINCT eid FROM matches WHERE account_link IN (%s))"
            query_statements.append(al_clause)
            args = [account_link_id]

            if len(restrict_types) > 0:
                type_clause = "AND matches.type IN (%s)"
                in_clause = ', '.join(list(map(lambda x: '%s', restrict_types)))
                type_clause = type_clause % in_clause
                query_statements.append(type_clause)
                args += restrict_types

            query = " ".join(query_statements)
            print(query, args)
            matches = self._db.execute_d(query, args)
            return matches
        else:
            return []

    #TODO: bad query since No sql parametrization. Will be removed, kept for testing.
    def get_all_matches_for_an_account_test(self, account_links=[], restrict_types=(), ljoin_account_links=False, match_cols=[]):
        """Gets all matches by an account.

        Params:
            account_links: all the account links of an account (should be 1)
            restrict_types: match types
            ljoin_account_links: Whether to left join account links
            match_cols: optional specify the columns needed from the matches table

        Returns:
            A list of dictionaries containing matches and account_links data if joined (possibly empty)
            No duplicates
        """
        if len(account_links) > 0:
            match_columns_query = ",".join(list(map(lambda c: "matches." + c, match_cols)))

            matches = self._db.execute_d(
                "SELECT " + ("matches.*" if match_columns_query == "" else match_columns_query) + " " + (Matches._account_links_clause if ljoin_account_links else "")
                + " FROM matches" + (" LEFT JOIN account_links ON matches.account_link = account_links.id" if ljoin_account_links else "")
                + " WHERE eid in (SELECT DISTINCT eid FROM matches WHERE account_link IN (" + ",".join([str(account_link.id()) for account_link in account_links]) + "))"
                + " AND matches.type IN (" + ",".join([str(t) for t in restrict_types]) + ")" if len(restrict_types) > 0 else ""
            )
            return matches
        else:
            return []

    def get_by_account_links_spread(self, account_links, restrict_types=(), ljoin_account_links=False):
        """Get matches by account links in spread form.

        'spread' means that any matches that have EIDs that match
            the original matches matched will be returned too.

        Params:
            account_links: A list of AccountLink objects
            restrict_types: List of ids of types
            ljoin_account_links: Whether to left join account links

        Returns:
            A list of unsorted, ungrouped Match objects (possibly empty)

            No duplicates.
        """
        # TODO: optimize (perhaps through watch table)
        if len(account_links) == 0:
            return []

        return Matches._load_rows(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._select_visibility,
                Matches._account_links_clause if ljoin_account_links else "",
                "FROM matches",
                frag(
                    "LEFT JOIN account_links ON matches.account_link = account_links.id"
                ) if ljoin_account_links else "",
                Matches._left_join_visibility,
                "WHERE eid IN (",
                frag(
                    "SELECT DISTINCT eid FROM matches",  # Need to look for other issues like this
                    "WHERE account_link IN :account_links",
                    account_links=[account_link.id() for account_link in account_links]
                ),
                ")",
                frag(
                    "AND matches.type IN :types",
                    types=restrict_types
                ) if restrict_types else ""
            )
        ))

    def get_match(self, eid, visual_id=None, type_int=None, grouping_id=None, data=None, partner_account=None, account_link=None, lat=None, lon=None,
                  time=None, selectColumns=[]):
        """Gets a match by the values specified. Columns api_insert, debug are not needed because those fields are for debugging purposes.

        Returns:
            The match record if found else None
        """
        if len(selectColumns) > 0:
            selectColumns = ", ".join(selectColumns)
        else:
            selectColumns = "*"

        query_string_list = ["SELECT " + selectColumns + " FROM matches WHERE eid= %(eid)s"]
        query_values = {"eid": eid}

        if(visual_id is not None):
            query_string_list.append("AND visual_id = %(visual_id)s")
            query_values["visual_id"] = visual_id

        if(type_int is not None):
            query_string_list.append("AND type = %(type)s")
            query_values["type"] = type_int

        if(grouping_id is not None):
            query_string_list.append("AND grouping_id = %(grouping_id)s")
            query_values["grouping_id"] = grouping_id

        if(data is not None):
            query_string_list.append("AND data = CAST(%(data)s AS JSON)")
            query_values["data"] = json.dumps(data)

        if(partner_account is not None):
            query_string_list.append("AND partner_account = %(partner_account)s")
            query_values["partner_account"] = partner_account

        if(account_link is not None):
            query_string_list.append("AND account_link = %(account_link)s")
            query_values["account_link"] = account_link

        if(lat is not None):
            query_string_list.append("AND lat = %(lat)s")
            query_values["lat"] = lat

        if(lon is not None):
            query_string_list.append("AND lon = %(lon)s")
            query_values["lon"] = lon

        if(time is not None):
            query_string_list.append("AND time = %(time)s")
            query_values["time"] = time

        query = ' '.join(query_string_list)

        match_rows = self._db.execute_d(query, query_values)
        if len(match_rows) > 0:
            return match_rows[0]
        else:
            return None

    def insert(
        self, eid, type_int, visual_id=None, grouping_id=None, data=None, partner_account=None, account_link=None,
        lat=None, lon=None, time=None, debug=None, api_insert=None, bc_transaction_id=None, bc_hash=None
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
                (eid, type, visual_id, grouping_id, data, partner_account, account_link, lat, lon, time, created, debug, api_insert, bc_transaction_id, bc_hash)
                VALUES
                    (%(eid)s, %(type)s, %(visual_id)s, %(grouping_id)s, %(data)s, %(partner_account)s, %(account_link)s, %(lat)s, %(lon)s, %(time)s,
                     %(created)s, %(debug)s, %(api_insert)s, %(bc_transaction_id)s, %(bc_hash)s
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
                "bc_hash": bc_hash
            }
        )

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

    def get_unique_eids(self):
        """Get the unique EIDs in the database.

        Returns:
            Tuple of the eids
        """
        self._db.execute(
            """
            SELECT DISTINCT
                eid
            FROM
                matches
            """
        )
        # Data from last 3 years, and USDAQualityGrade
        return tuple(
            row['eid'] for row in
            self._db.fetch_all()
        )

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
                        usda_quality_grade_type=match_types_by_name[
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

    def get_count_eid_distinct_by_account(self, account_id):
        """Count the number of distinct EIDs in the database for an account.

        Params:
            account_id: The account to generate data on

        Returns:
            The value
        """
        return self._db.exec_frag_d(
            frag(
                """
                SELECT
                    COUNT(DISTINCT eid) AS 'count'
                FROM
                    matches
                WHERE account_link IN (
                    SELECT id FROM account_links WHERE account=:account
                )
                """,
                account=account_id
            )
        )[0]['count']

    def get_count_distribution(self, type_int, account_links, eid_distinct=True):
        """Gets the count of each data type for an account

        Params:
            type_int: The type as an int
            account_links: Query on only a set of account links (spread)
            eid_distinct: Whether it should only count once per EID
                (as long as duplicate entries per type per eid don't exist, this doesn't matter)

        Returns:
            A list of dictionaries
                Keys
                    data: Int value of data or string if join_str is set
                    count: The number of times data existed
        """
        # TODO: implement eid_distinct

        if len(account_links) == 0:
            return []

        account_links_clause = """AND eid IN
                    (
                        SELECT DISTINCT eid
                        FROM matches
                        WHERE
                        account_link IN (""" + ','.join([
            str(int(account_link.id())) for account_link in account_links
        ]) + """))
            """

        full_sql = """
                SELECT 
                    data, COUNT(*) as 'count'
                FROM
                    matches
                WHERE
                    type=%(type)s
                    """ + account_links_clause + """
                GROUP BY
                    data
            """
        return Matches._load_rows(self._db.execute_d(
            full_sql,
            {
                "type": type_int
            }
        ))

    def get_count_distribution_global(self, type_int, eid_distinct=True):
        """Gets the count of each data type for global

        Params:
            type_int: The type as an int
            eid_distinct: Whether it should only count once per EID
                (as long as duplicate entries per type per eid don't exist, this doesn't matter)

        Returns:
            A list of dictionaries
                Keys
                    data: Int value of data or string if join_str is set
                    count: The number of times data existed
        """
        #TODO: implement eid_distinct
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
                Matches._select_visibility,
                Matches._account_links_clause if ljoin_account_links else "",
                """
                    FROM auction_sales
                    LEFT JOIN sales_groups ON sales_groups.auction_sale=auction_sales.id
                    LEFT JOIN eid_group_eids ON eid_group_eids.eid_group=sales_groups.eid_group
                    LEFT JOIN matches ON eid_group_eids.eid=matches.eid
                    LEFT JOIN account_links ON matches.account_link=account_links.id
                """,
                Matches._left_join_visibility,
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

    def get_count_by_eid_if_visible(self, eid_number):
        """Gets count of matches associated with an eid if visible.

        Params:
            eid_number: eid number

        Returns:
            One row indicating the count
        """
        # return self._db.exec_frag_d(
        #     frag(
        #         """
        #         SELECT count(eid) as 'count'
        #         FROM matches
        #         """,
        #         Matches._left_join_visibility,
        #         frag(
        #             "WHERE matches_type_visibility.visibility > 0 AND matches.eid=:eid_number",
        #             eid_number=eid_number
        #         )
        #     ),
        # )[0]['count']
        return self._db.exec_frag_d(
            frag(
                """
                SELECT count(eid) as 'count'
                FROM matches
                """,
                frag(
                    "WHERE eid=:eid_number",
                    eid_number=eid_number
                )
            ),
        )[0]['count']

    def get_visual_id_if_owner_and_visible(self, visual_id, account_id):
        """Gets matches data associated with an visual id if visible.

        Params:
            visual_id: The visual id to look up
            account_id: current active account

        Returns:
            All the matches table rows containing the visual id matches
        """
        #visual_id = str(visual_id)
        # return self._db.execute_d(
        #     """
        #         SELECT matches.*
        #         FROM matches
        #         LEFT JOIN account_links on matches.account_link=account_links.id
        #         LEFT JOIN matches_type_visibility ON matches.type=matches_type_visibility.type
        #         WHERE matches.type=%(visual_id_type)s 
        #         AND (
        #             (account_links.account=%(account_id)s AND matches_type_visibility.account=account_links.account AND matches_type_visibility.visibility > 0) 
        #             OR 
        #             (matches.partner_account=%(account_id)s)
        #         )
        #         AND matches.data=%(visual_id)s
        #     """,
        #     {
        #         "visual_id_type": match_types_by_name["Visual ID"],
        #         "account_id": account_id,
        #         "visual_id": visual_id
        #     }
        return self._db.execute_d(
            """
                SELECT distinct matches.eid, matches.visual_id
                FROM matches

                WHERE matches.visual_id=%(visual_id)s
            """,
            {
                "visual_id": visual_id
            }
        )

    @staticmethod
    def _load_rows(rows):
        """Parses returned JSON from mysql and applies booleans."""
        for row in rows:
            if row['data'] is not None:
                row['data'] = json.loads(row['data'])
            if 'visibility' in row:
                if row['visibility'] is None:
                    if row['partner_account'] is None:
                        row['visibility'] = True  # Visible if nobody owns it
                    else:
                        row['visibility'] = None
                else:
                    row['visibility'] = row['visibility'] > 0
        return rows
