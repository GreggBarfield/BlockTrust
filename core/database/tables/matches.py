import time as time_module
import json
from ..frag import frag, frag_insert_into
from ..objects.match import Match, MatchException
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

    _account_links_cols = ("id", "account", "uid_type", "uid", "company", "sector")
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
            matches.account=matches_type_visibility.account AND
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

    def insert(
        self, eid, type_int, data=None, account=None, account_link=None,
        lat=None, lon=None, time=None, raw_identifier=None
    ):
        """Insert a new row into matches.

        Params:
            eid: The animal ID, int (required)
            type_int: The match type, int (required)
            data: The match data (optional)
                If None is provided (default), NULL is inserted
                Else it is json-encoded and put in the record
            account: The data owner, int (optional)
            account_link: The account link, int (optional)
            lat: The lattitude of the data scan, int (optional)
            lon: The longitude of the data scan, int (optional)
            time: The time of the data scan, int (optional)
            raw_identifier: debug usage, str (optional)
        Raises:
            MatchesException
        """

        if not isinstance(type_int, int):
            raise MatchesException("type_int should be an int")

        self._db.exec_frag(
            frag_insert_into(
                'matches',
                [
                    {
                        "eid": eid,
                        "type": type_int,
                        "data": None if data is None else json.dumps(data),
                        "account": account,
                        "account_link": account_link,
                        "lat": lat,
                        "lon": lon,
                        "time": time,
                        "created": int(time_module.time()),
                        "raw_identifier": raw_identifier
                    }
                ]
            )
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
        a
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
                    LEFT JOIN sales_group_eids ON sales_group_eids.sales_group=sales_groups.id
                    LEFT JOIN matches ON sales_group_eids.eid=matches.eid
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
        return self._db.exec_frag_d(
            frag(
                """
                SELECT count(eid) as 'count'
                FROM matches
                """,
                Matches._left_join_visibility,
                frag(
                    "WHERE matches_type_visibility.visibility > 0 AND matches.eid=:eid_number",
                    eid_number=eid_number
                )
            ),
        )[0]['count']

    @staticmethod
    def _load_rows(rows):
        """Parses returned JSON from mysql and applies booleans."""
        for row in rows:
            if row['data'] is not None:
                row['data'] = json.loads(row['data'])
            if 'visibility' in row:
                if row['visibility'] is None:
                    if row['account'] is None:
                        row['visibility'] = True  # Visible if nobody owns it
                    else:
                        row['visibility'] = None
                else:
                    row['visibility'] = row['visibility'] > 0
        return rows
