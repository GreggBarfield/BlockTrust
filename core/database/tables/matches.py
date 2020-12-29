import time as time_module
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
        match_rows = self._db.execute_d(
            """SELECT * FROM matches
                WHERE id=%(id)s
            """,
            {
                "id": match_id
            }
        )
        if len(match_rows) != 1:
            raise MatchesException("No match found with that ID.")
        return Match(self._db, match_rows[0])


    def get_by_eid(self, eid, restrict_types=(), ljoin_account_links=False, ljoin_data_str=False):
        """Gets matches by an eid.

        Params:
            eid: the eid to find
            restrict_types: List of ids of types
            ljoin_account_links: Whether to left join account links
            ljoin_data_str: Whether to left join data string (will be set as data_str)
        
        Returns:
            A list (possibly empty) of Match objects
        """

        restrict_types_clause = ""

        params = {
            "eid": eid
        }
        if restrict_types:
            restrict_types_clause = ' AND type IN (' + ','.join(('%(restrict_' + str(t_itr) + ')s' for t_itr in range(len(restrict_types)))) + ')'
            for t_itr, t in enumerate(restrict_types):
                params["restrict_" + str(t_itr)] = t


        account_links_cols = ("id", "account", "uid_type", "uid", "company", "sector")
        account_links_clause = ""
        left_join_clause = ""
        if ljoin_account_links:
            account_links_clause = ', ' + ', '.join('account_links.' + a + ' AS "account_links.' + a + '"' for a in account_links_cols)
            left_join_clause = """
                LEFT JOIN
                    account_links ON matches.account_link = account_links.id"""

        ljoin_data_str_select = ""
        ljoin_data_str_clause = ""
        if ljoin_data_str:
            ljoin_data_str_select = ", matches_data_strings.data AS data_str"
            ljoin_data_str_clause = "LEFT JOIN matches_data_strings ON matches_data_strings.id = matches.data"

        full_sql = """SELECT matches.* """ + account_links_clause + """ """ + ljoin_data_str_select + """  FROM matches
                """ + left_join_clause + """
                """ + ljoin_data_str_clause + """
                WHERE eid=%(eid)s
                    """ + restrict_types_clause + """
            """
        match_rows = self._db.execute_d(
            full_sql,
            params
        )
        return [Match(self._db, match_row) for match_row in match_rows]
    

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
        ids = [account_link.id() for account_link in account_links]
        where_clause = ' OR '.join(('account_link=%s' for _id in ids))
        restrict_types_clause = ""
        if restrict_types:
            restrict_types_clause = ' AND type IN (' + ','.join(('%s' for t in restrict_types)) + ')'


        account_links_cols = ("id", "account", "uid_type", "uid", "company", "sector")
        account_links_clause = ""
        left_join_clause = ""
        if ljoin_account_links:
            account_links_clause = ', ' + ', '.join('account_links.' + a + ' AS "account_links.' + a + '"' for a in account_links_cols)
            left_join_clause = """
                LEFT JOIN
                    account_links ON matches.account_link = account_links.id
            """

        full_sql = """SELECT matches.* """ + account_links_clause + """ FROM matches
                """ + left_join_clause + """
                WHERE
                    eid IN
                        (
                            SELECT eid
                            FROM matches
                            WHERE
                            """ + where_clause + """
                        )
                    """ + restrict_types_clause + """
            """
            

        match_rows = self._db.execute_d(
            full_sql,
            ids + restrict_types
        )
        return [Match(self._db, match_row) for match_row in match_rows]

    
    def insert(
        self, eid, type_int, data=None, account=None, account_link=None, lat=None, lon=None, time=None, raw_identifier=None
    ):
        """Insert a new row into matches.

        Params:
            eid: The animal ID, int (required)
            type_int: The match type, int (required)
            data: The match data (optional)
                If an int is provided, it is inserted directly
                If None is provided (default), NULL is inserted
                If a string is provided, Matches.insert will use
                    MatchesDataStrings.get_by_data to get the ID of this string
            account: The data owner, int (optional)
            account_link: The account link, int (optional)
            lat: The lattitude of the data scan, int (optional)
            lon: The longitude of the data scan, int (optional)
            time: The time of the data scan, int (optional)
            raw_identifier: debug usage, str (optional)
        Raises:
            MatchesException
        """

        # Convert data to an ID
        if isinstance(data, str):
            data = self._db.matches_data_strings.get_by_data(data)
    
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
                "data": data,
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


    def get_count_distribution(self, type_int, account_links=None, join_str=False, eid_distinct=True):
        """Gets the count of each data type

        Params:
            type_int: The type as an int
            account_links: Query on only a set of account links (spread)
            join_str: Optional, default false, whether to report data as a string
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
        inner_join_clause = ""
        if join_str:
            data_type_clause = "matches_data_strings.data"
            inner_join_clause = """
                INNER JOIN
                    matches_data_strings ON matches.data = matches_data_strings.id
            """
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
                    """ + data_type_clause + """, COUNT(*) as 'count'
                FROM
                    matches
                """ + inner_join_clause + """
                WHERE
                    type=%(type)s
                    """ + account_links_clause + """
                GROUP BY
                    data
            """
        return self._db.execute_d(
            full_sql,
            {
                "type": type_int
            }
        )

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
        # TODO: Do ljoin_account_links, restrict_types
        return [Match(self._db, row) for row in self._db.execute_d(
            """
            SELECT matches.*, account_links.company AS 'account_links.company',
                    account_links.sector AS 'account_links.sector'
                FROM auction_sales
                LEFT JOIN sales_groups ON sales_groups.auction_sale=auction_sales.id
                LEFT JOIN sales_group_eids ON sales_group_eids.sales_group=sales_groups.id
                LEFT JOIN matches ON sales_group_eids.eid=matches.eid
                LEFT JOIN account_links ON matches.account_link=account_links.id
                WHERE auction_sales.account=%(account_id)s
            """,
            {
                "account_id": account_id
            }
        )]
