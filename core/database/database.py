import mysql.connector as mysql
from mysql.connector.errors import Error

from .tables.accounts import Accounts
from .tables.account_users import AccountUsers
from .tables.account_links import AccountLinks
from .tables.users import Users
from .tables.matches import Matches
from .tables.messages import Messages
from .tables.reports import Reports
from .tables.usda_reports import USDAReports

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
        self.account_links = AccountLinks(self)
        self.messages = Messages(self)
        self.reports = Reports(self)
        self.usda_reports = USDAReports(self)

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
        self._cursor = self._connection.cursor(dictionary=True)
        #print("SECURE:", self._connection._ssl_active)
        return self._cursor

    def execute(self, code, params=tuple(), allow_retry=True, multi=False):
        try:
            return self._cursor.execute(code, params, multi)
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
                    return self.execute(
                        code,
                        params=params,
                        allow_retry=False,
                        multi=multi
                    )
                else:
                    print("SQL Bad, quitting (not allowed to retry) after", error)
                    quit()  # TODO Find better solution in future
            raise error

    def execute_d(self, code, params=tuple()):
        """Executes a query with params provided.

        Returns:
            List of dictionaries possibly empty
        """
        self.execute(code, params)
        return self.fetch_all()

    def execute_fetch_one(self, code, params=tuple()):
        self.execute(code, params)
        return self._cursor.fetchone()

    def exec_frag_d(self, kvs):
        """Executes a frag() style return value.

        Params:
            kvs: The frag()'s return value.

        Returns:
            See execute_d
        """
        return self.execute_d(kvs[0], kvs[1])

    def exec_multi_frag_d(self, kvs):
        """Executes a frag() style return value.

        Enables multi.

        Params:
            kvs: The frag()'s return value.

        Returns:
            An iterator on the results, which are lists of dictionaries.
        """
        return Database._expand_multi(self.execute(kvs[0], kvs[1], multi=True))

    @staticmethod
    def _expand_multi(statement_results):
        """Helper for multi executes

        Params:
            statement_results: generator of MySQL DictCursor

        Returns:
            A list of lists of dictionaries
        """
        results = []
        try:
            for statement_result in statement_results:
                if statement_result.with_rows:
                    results.append(statement_result.fetchall())
                else:
                    results.append([])
        except RuntimeError as e:
            # https://www.python.org/dev/peps/pep-0479/
            if 'StopIteration' not in str(e):
                raise e
        return results

    def exec_frag(self, kvs):
        """Executes a frag() style return value.

        Params:
            kvs: The frag()'s return value.
        """
        self.execute(kvs[0], kvs[1])

    def fetch_all(self):
        return self._cursor.fetchall()

    def last_row_id(self):
        return self._cursor.lastrowid

    def row_count(self):
        return self._cursor.rowcount

    def execute_many(self, query, data):
        """Prepares a database operation (query or command) and executes it against all parameter sequences or mappings

        Params:
            data: list of tuples
            query: the SQL statement
        """
        self._cursor.executemany(query, data)

    def close(self):
        self._cursor.close()
        self._connection.close()