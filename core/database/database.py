import mysql.connector as mysql
from mysql.connector.errors import Error

from .tables.accounts import Accounts
from .tables.account_users import AccountUsers
from .tables.account_links import AccountLinks
from .tables.users import Users
from .tables.matches import Matches
from .tables.animals import Animals
from .tables.matches_data_strings import MatchesDataStrings
from .tables.sales_groups import SalesGroups
from .tables.sales_group_eids import SalesGroupEIDs
from .tables.sales_group_intervals import SalesGroupIntervals
from .tables.files import Files
from .tables.zip_codes import ZIPCodes

# all SQL should be in tables/ and in this file
# objects/ can use tables/ but can't use SQL

class Database:
    """Access to the database on a given SQL connection.
    This should be initialized PER APPLICATION CONTEXT.
    """

    def __init__(self, sql_config):
        """Constructor for Database.

        Params:
            sql_config: a dictionary that will be unpacked and passed to mysql.connect
        """  
        self._sql_config = sql_config
        self._connection = None
        self._cursor = None

        # Functions expect self._connection and self._cursor to not be None
        self.connect()

        # Instantiate tables
        self.accounts = Accounts(self)
        self.account_users = AccountUsers(self)
        self.users = Users(self)
        self.matches = Matches(self)
        self.animals = Animals(self)
        self.account_links = AccountLinks(self)
        self.matches_data_strings = MatchesDataStrings(self)
        self.sales_groups = SalesGroups(self)
        self.sales_group_eids = SalesGroupEIDs(self)
        self.files = Files(self)
        self.zip_codes = ZIPCodes(self)


    def connect(self):
        try:
            if self._cursor is not None:
                self._cursor.close()
        except Exception as e:
            pass
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception as e:
            pass
        self._connection = mysql.connect(**self._sql_config)
        self._cursor = self._connection.cursor()
        return self._cursor


    def execute(self, code, params=tuple(), allow_retry=True):
        try:
            return self._cursor.execute(code, params)
        except Error as error:
            # SQL server can sometimes kick us off after a period of time,
            # see if that's the case and attempt reconnect
            if (
                not self._connection.is_connected() or
                error.errno == 2006
            ):
                if allow_retry:
                    print("Attempting reconnection after", error)
                    self.connect()
                    return self.execute(code, params=params, allow_retry=False)
                else:
                    print("SQL Bad, quitting (not allowed to retry) after", error)
                    quit()  # TODO Find better solution in future
            raise error


    def execute_d(self, *wargs):
        self._cursor.execute(*wargs)
        return self.fetch_all_d()
        

    def fetch_all(self):
        return self._cursor.fetchall()
        

    def fetch_all_d(self):
        # Should we just use MySQLCursorDict?
        columns = self._cursor.column_names
        return [
            {
                columns[col_i]: row[col_i]
                for col_i in range(len(columns))
            }
            for row in self._cursor
        ]
    

    def last_row_id(self):
        return self._cursor.lastrowid

    def row_count(self):
        return self._cursor.rowcount
