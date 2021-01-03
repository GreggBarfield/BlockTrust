import time as time_module
import json
from ..frag import frag
from ..objects.match import Match, MatchException


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

    @staticmethod
    def _load_json(rows):
        """Parses returned JSON from mysql."""
        for row in rows:
            if row['data'] is not None:
                row['data'] = json.loads(row['data'])
        return rows

    def __init__(self, db):
        self._db = db

    def get_by_id(self, match_id):
        """Gets a match by an ID.

        Params:
            id: the match id
        
        Returns:
            A Match object

        Raises:
            MatchesException
        """
        match_rows = Matches._load_json(self._db.execute_d(
            """SELECT * FROM matches
                WHERE id=%(id)s
            """,
            {
                "id": match_id
            }
        ))
        if len(match_rows) != 1:
            raise MatchesException("No match found with that ID.")
        return Match(self._db, match_rows[0])

    def get_by_eids(self, eids, restrict_types=(), ljoin_account_links=False):
        """Gets matches by eids.

        Params:
            eids: the eids to find
            restrict_types: List of ids of types
            ljoin_account_links: Whether to left join account links

        Returns:
            A list (possibly empty) of matches rows
        """
        return Matches._load_json(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._account_links_clause if ljoin_account_links else "",
                "FROM matches",
                frag(
                    "LEFT JOIN account_links ON matches.account_link = account_links.id",
                ) if ljoin_account_links else "",
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

        return Matches._load_json(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._account_links_clause if ljoin_account_links else "",
                "FROM matches",
                frag(
                    "LEFT JOIN account_links ON matches.account_link = account_links.id"
                ) if ljoin_account_links else "",
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

        self._db.execute(
            """
            INSERT INTO matches
                (eid, type, data, account, account_link, lat, lon, time, created, raw_identifier)
                VALUES
                (%(eid)s, %(type)s, %(data)s, %(account)s, %(account_link)s, %(lat)s, %(lon)s, %(time)s, %(created)s, %(raw_identifier)s)
            """,
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
        )


    def get_count_eid_distinct(self):
        """Count the number of distinct EIDs in the database.

        Returns:
            The value
        """
        self._db.execute(
            """
            SELECT 
                COUNT(DISTINCT eid)
            FROM
                matches
            """
        )
        return self._db.fetch_all()[0][0]


    def get_count_distribution(self, type_int, account_links=None, eid_distinct=True):
        """Gets the count of each data type

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
        #TODO: implement eid_distinct
        data_type_clause = "data"
        account_links_clause = ""
        if account_links:
            account_links_clause = """AND eid IN
                        (
                            SELECT eid
                            FROM matches
                            WHERE
                            account_link IN (""" +','.join([
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
        return Matches._load_json(self._db.execute_d(
            full_sql,
            {
                "type": type_int
            }
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

        return Matches._load_json(self._db.exec_frag_d(
            frag(
                "SELECT matches.*",
                Matches._account_links_clause if ljoin_account_links else "",
                """
                    FROM auction_sales
                    LEFT JOIN sales_groups ON sales_groups.auction_sale=auction_sales.id
                    LEFT JOIN sales_group_eids ON sales_group_eids.sales_group=sales_groups.id
                    LEFT JOIN matches ON sales_group_eids.eid=matches.eid
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
