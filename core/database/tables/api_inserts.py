import json
import time
from ..no_value import NoValue

NO_VALUE = NoValue()

STATUS_IDS_TO_NAMES = {
    0: "Pending",
    1: "Done",
    2: "Blocked",
    3: "Running",
    4: "Bad Namespace",
    5: "Bad Type",
    6: "Exception",
    7: "Duplicate"
}
STATUS_NAMES_TO_IDS = {b: a for a, b in STATUS_IDS_TO_NAMES.items()}

class ApiInserts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id, namespace, type, data):
        """Inserts data into table.

        Params:
            data: the data to be added
        """
        self._db.execute(
            """INSERT INTO api_inserts
                (account, namespace, type, fields)
                VALUES
                    (%(account)s, %(namespace)s, %(type)s, %(fields)s)
            """,
            {
                "account": account_id,
                "namespace": namespace,
                "type": type,
                "fields": json.dumps(data)
            }
        )

    def get_partner_api_inserts_count(self, partner_company_name, interval):
        """
        Returns the count of API inserts by a particular partner in a specified interval of time

        Params:
            partner_company_name: Name of the partner company
            interval: Number of days over which count of API inserts is required

        Returns:
            Count of API inserts withtin the specified period by the partner
        """
        latest_api_inserts_count = self._db.execute_d(
            """
            SELECT count(ai.id) as api_inserts_count FROM api_inserts ai INNER JOIN accounts a ON ai.account = a.id AND a.company = %(company)s
            WHERE created BETWEEN date_sub(now(),INTERVAL %(interval)s DAY) AND now()
            """, {
                "company": partner_company_name,
                "interval": interval
            }
        )
        return latest_api_inserts_count[0]["api_inserts_count"]


    def get_api_inserts(self, id=NO_VALUE, account=NO_VALUE, namespace=NO_VALUE, type=NO_VALUE, row=NO_VALUE,
                        block=NO_VALUE, status=NO_VALUE, created_start_time=NO_VALUE):
        
        """
        Returns the list API inserts based on attributes provided

        Params:
            id: ID of the insert
            account: Account ID of account performing the insert
            namespace: Insert namespace
            type: Type of Insert
            status: Status of Insert

        Returns:
            List of API inserts
        """
        
        base_query = "SELECT * FROM api_inserts"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account is not NO_VALUE:
            query_conditions.append("account = %(account)s")
            query_values["account"] = account
        if namespace is not NO_VALUE:
            query_conditions.append("namespace = %(namespace)s")
            query_values["namespace"] = namespace
        if type is not NO_VALUE:
            query_conditions.append("type = %(type)s")
            query_values["type"] = type
        if row is not NO_VALUE:
            query_conditions.append("row = %(row)s")
            query_values["row"] = row
        if block is not NO_VALUE:
            query_conditions.append("block = %(block)s")
            query_values["block"] = block
        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status
        if created_start_time is not NO_VALUE:
            query_conditions.append("created > %(created_start_time)s")
            query_values["created_start_time"] = created_start_time

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        api_insert_rows = self._db.execute_d(query, query_values)
        if len(api_insert_rows) > 0:
            return api_insert_rows
        else:
            return []

    def get_daily_api_inserts_count_for_account(self, account=NO_VALUE, status=NO_VALUE):
        """
        Returns the list of daily API inserts count based on attributes provided

        Params:
            account: Account ID of account inserting the records
            status: Processing status of the Records  

        Returns:
            A list of API inserts count aggregated by date of insertion  
        """
        base_query = "SELECT DATE(created) as inserts_date, count(*) as inserts_count from api_inserts"

        query_conditions = []
        query_values = {}

        if account is not NO_VALUE:
            query_conditions.append("account = %(account)s")
            query_values["account"] = account
        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        group_by_clause = " group by DATE(created)"

        query = base_query + combined_query_condition + group_by_clause
        api_insert_counts = self._db.execute_d(query, query_values)
        if len(api_insert_counts) > 0:
            return api_insert_counts
        else:
            return []