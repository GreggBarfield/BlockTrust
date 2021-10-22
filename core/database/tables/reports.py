from json import dumps, loads
from time import time
from core.database.no_value import NoValue
from ...common_exceptions import DebugException
from ..frag import frag, frag_insert_into

from core.reports.query_types import (
    count_distribution, count_distribution_global, count_eid_distinct,
    count_eid_distinct_by_account
)
import json

NO_VALUE = NoValue()

REPORT_STATUS = {
    "Pending": 0,
    "Ready": 1,
    "Dropped": 2,
    "Running": 3,
    "Error": 4,  # Note that errors may also be uncaught, leading to infinite running
}

class Reports:
    """Model for reports.

    Good reference:
    https://docs.google.com/document/d/1jyW4uzsuygfAKeGK4LeR8CftMriONFPh_ZM0rehYH8g/edit
    (Internal Planning 4)

    Standard report dictionary:
        id
        priority
        owner
        issuer
        query
        result
        status
        fulfilled
        created_timestamp
        last_updated_timestamp
    """

    """Statuses"""

    def __init__(self, db):
        self._db = db

    def get_ready_by_query(self, query):
        """Gets ready reports by query.

        If multiple reports match the query, the most recent (by fulfilled) is returned.

        Params:
            query: The query (dictionary)

        Returns:
            A standard report dictionary, or None.
        """
        results = self._db.exec_frag_d(
            frag(
                "SELECT * FROM reports",
                frag(
                    "WHERE query=CAST(:query AS JSON)",
                    "AND status=:ready_status",
                    query=dumps(query),
                    ready_status=1
                ),
                "ORDER BY fulfilled DESC LIMIT 1"
            )
        )
        return Reports._process_row(results[0]) if results else None

    def insert_query(self, account_id, query, priority=30):
        """Insert a new query. Status is always pending.

        Params:
            owner: The Account ID of the owner or None for system
            query: The query (dictionary)
            issuer: The Account ID of the issuer or None for system
                (optional, default None)
            priority: Priority of the query (default 30)
        """

        self._db.exec_frag(
            frag_insert_into(
                "reports",
                [
                    {
                        "account_id": account_id,
                        "query": dumps(query),
                        "status": 0
                    }
                ]
            )
        )

    def work_report(self):
        """Gets the next report to work and marks it as running.

        Returns:
            A standard report dictionary, or None
        """
        # gets reports row where status is pending (0), sets it to running (3) and returns the row
        results = self._db.exec_multi_frag_d(
            frag(
                """
                LOCK TABLES reports WRITE;
                SET @work_report_id = (
                    SELECT id FROM reports WHERE status=:pending_status
                    ORDER BY priority DESC, create_timestamp ASC
                    LIMIT 1
                );
                UPDATE reports SET status=:running_status WHERE id=@work_report_id;
                SELECT * FROM reports WHERE id=@work_report_id;
                UNLOCK TABLES;
                """,
                pending_status=0,
                running_status=3
            )
        )[3]
        return Reports._process_row(results[0]) if results else None

    def fulfill_report(self, report_id, result, status=1):
        """Fulfills a report.

        Params:
            report_id: The report ID
            result: The result (dictionary)
            status: The status (default 1, success)
        """
        self._db.exec_frag(
            frag(
                "UPDATE reports",
                frag(
                    "SET",
                    "result=:result,",
                    "status=:status,",
                    "fulfilled=:fulfilled",
                    result=dumps(result),
                    status=status,
                    fulfilled=time()
                ),
                frag(
                    "WHERE",
                    "id=:id",
                    id=report_id
                )
            )
        )

    def make_reports_for_account(self, account_id):
        queries = [
            count_distribution.create(account_id, "USDA Yield Grade"),
            count_distribution.create(account_id, "USDA Quality Grade"),
            count_eid_distinct_by_account.create(account_id)
        ]

        for query in queries:
            self.insert_query(account_id, query)

    def mark_account_reports_for_reprocessing(self):
        """Marking reports linked to accounts for reprocessing. Reports need to be in ready state to be marked.

        """
        self._db.execute(
            """
                UPDATE reports SET status=%(status)s WHERE status IN (%(ready_status)s) AND account_id IS NOT NULL

            """,
            {
                "status": REPORT_STATUS["Pending"],
                "ready_status": REPORT_STATUS["Ready"]
            }

        )

    def get_report(self, query=NO_VALUE, selectColumns=[]):
        """Generic get report routine

        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        base_query = "SELECT " + selectColumns + " FROM reports"

        query_conditions = []
        query_values = {}

        if query is not NO_VALUE:
            query_conditions.append(" query = CAST(%(query)s AS JSON)")
            query_values["query"] = json.dumps(query)

        if len(query_conditions) > 0:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        report_rows = self._db.execute_d(query, query_values)
        if len(report_rows) > 0:
            return report_rows
        else:
            return []

    def update_report(self, id, status=NO_VALUE):
        """Generic update report routine

        """
        if status is not NO_VALUE:
            self._db.execute(
                """
                    UPDATE reports SET status=%(status)s WHERE id=%(id)s

                """,
                {
                    "status": status,
                    "id": id
                }

            )

    @staticmethod
    def _process_row(row):
        """Takes in a raw row (dict) and converts it in-place to be more python like."""
        json_cols = ['query', 'result']
        for col in json_cols:
            if row[col] is not None:
                row[col] = loads(row[col])
        return row
