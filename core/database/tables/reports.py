from json import dumps, loads
from time import time
from core.database.no_value import NoValue
from core.sectors import SECTORS_NAME_TO_ID
from ...common_exceptions import DebugException
from ..frag import frag, frag_insert_into

from core.reports.query_types import (
    count_distribution, count_distribution_for_sector_at_account, count_eid_distinct_by_account,
    count_distribution_global, count_eid_distinct, annual_count_distribution_by_account,
    annual_count_eid_distinct_by_account
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

report_cols = ("id", "account_id", "priority", "query", "result", "status", "fulfilled", "created_timestamp", "last_updated_timestamp")

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

    def insert_query(self, account_id, query):
        """Insert a new query. Status is always pending.

        Params:
            owner: The Account ID of the owner or None for system
            query: The query (dictionary)
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
                    ORDER BY priority DESC, created_timestamp ASC
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

    def get_accounts_with_no_reports(self):
        for row in self._db.execute_d(
            f"""
            SELECT id,sector FROM accounts WHERE accounts.id NOT IN
            (SELECT account_id FROM reports WHERE account_id IS NOT NULL)
            AND is_partner=0 AND sector NOT IN ({SECTORS_NAME_TO_ID["Buyer"]})
            """
        ):
            yield {"account_id": row['id'], "sector_id": row['sector']}

    def make_reports_for_account(self, account_id, sector_id):
        if sector_id != SECTORS_NAME_TO_ID["Buyer"]:
            queries = [
                count_distribution.create(account_id, "USDA Yield Grade"),
                count_distribution.create(account_id, "USDA Quality Grade"),
                count_eid_distinct_by_account.create(account_id),
                annual_count_distribution_by_account.create(account_id, "USDA Yield Grade"),
                annual_count_distribution_by_account.create(account_id, "USDA Quality Grade"),
                annual_count_eid_distinct_by_account.create(account_id)
            ]

            if sector_id in (SECTORS_NAME_TO_ID["Feedlot"], SECTORS_NAME_TO_ID["Packer"], SECTORS_NAME_TO_ID["Auction"]):
                queries.append(count_distribution_for_sector_at_account.create(account_id, SECTORS_NAME_TO_ID["Cow-Calf"]))

            for query in queries:
                self.insert_query(account_id, query)

    def make_partner_reports(self, partner_id, sector_id):
        if sector_id in (
            SECTORS_NAME_TO_ID["Cow-Calf"], SECTORS_NAME_TO_ID["Packer"], SECTORS_NAME_TO_ID["Auction"],
            SECTORS_NAME_TO_ID["Feedlot"], SECTORS_NAME_TO_ID["Financial"], SECTORS_NAME_TO_ID["Producer Service"]
        ):
            queries = [
                count_distribution.create(partner_id, is_partner=True),
                count_distribution.create(partner_id, "USDA Yield Grade", is_partner=True),
                count_distribution.create(partner_id, "USDA Quality Grade", is_partner=True),
                count_eid_distinct_by_account.create(partner_id, is_partner=True),
                annual_count_distribution_by_account.create(partner_id, "USDA Yield Grade", is_partner=True),
                annual_count_distribution_by_account.create(partner_id, "USDA Quality Grade", is_partner=True),
                annual_count_eid_distinct_by_account.create(partner_id, is_partner=True)
            ]

            for query in queries:
                self.insert_query(partner_id, query)

    def make_global_reports(self):
        queries = [
            count_distribution_global.create("USDA Yield Grade"),
            count_distribution_global.create("USDA Quality Grade"),
            count_eid_distinct.create()
        ]
        for query in queries:
            self.insert_query(None, query)

    def mark_account_reports_for_reprocessing(self):
        """Marking reports linked to accounts for reprocessing. Reports need to be in ready state to be marked.

        """
        self._db.execute(
            """
                UPDATE reports SET status=%(status)s WHERE status IN (%(ready_status)s, %(error_status)s)
                AND account_id IS NOT NULL
            """,
            {
                "status": REPORT_STATUS["Pending"],
                "ready_status": REPORT_STATUS["Ready"],
                "error_status": REPORT_STATUS["Error"]
            }

        )
    
    def make_annual_reports_for_account(self, account_id, sector_id):
        """ Temporary routine to create annual reports for accounts """
        if sector_id != SECTORS_NAME_TO_ID["Buyer"]:
            queries = [
                annual_count_distribution_by_account.create(account_id, "USDA Yield Grade"),
                annual_count_distribution_by_account.create(account_id, "USDA Quality Grade"),
                annual_count_eid_distinct_by_account.create(account_id)
            ]
            for query in queries:
                self.insert_query(account_id, query)


    def get_reports(self, query=NO_VALUE, selectColumns=[]):
        """Generic get report routine

        """
        for selectColumn in selectColumns:
            if selectColumn not in report_cols:
                raise Exception("selectColumn " + selectColumn + " does not exist")
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
