from json import dumps
from time import time
from ...common_exceptions import DebugException
from ..frag import frag, frag_insert_into


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
        created

    """

    """Statuses"""
    REPORT_STATUSES = {
        0: "Pending",
        1: "Ready",
        2: "Dropped",
        3: "Running",
    }

    def __init__(self, db):
        self._db = db

    def get_by_query(self, query):
        """Gets a report by query.

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
                    query=dumps(query)
                ),
                "ORDER BY fulfilled DESC LIMIT 1"
            )
        )
        return results[0] if results else None

    def insert_query(self, owner, query, issuer=None, priority=30):
        """Insert a new query.

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
                        "priority": priority,
                        "owner": owner,
                        "issuer": issuer,
                        "query": dumps(query),
                        "status": 0,
                        "created": time()
                    }
                ]
            )
        )

    def work_report(self):
        """Gets the next report to work and marks it as running.

        Returns:
            A standard report dictionary, or None
        """
        results = self._db.exec_multi_frag_d(
            frag(
                """
                LOCK TABLES reports WRITE;
                SET @work_report_id = (
                    SELECT id FROM reports WHERE status=:pending_status
                    ORDER BY priority DESC, created ASC
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
        return results[0] if results else None

    def fulfill_report(self, report_id, result):
        """Fulfills a report.

        Params:
            report_id: The report ID
            result: The result (dictionary)
        """
        self._db.exec_frag(
            frag(
                "UPDATE reports",
                frag(
                    "SET",
                    "result=:result",
                    "status=:ready_status",
                    "fulfilled=:fulfilled",
                    result=result,
                    ready_status=1,
                    fulfilled=time()
                ),
                frag(
                    "WHERE",
                    "id=:id",
                    id=report_id
                )
            )
        )
