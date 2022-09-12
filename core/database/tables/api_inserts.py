import json
from ..no_value import NoValue

NO_VALUE = NoValue()

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

    def get_partner_api_inserts_count(self, partner_comapny_name=NO_VALUE, interval=NO_VALUE):
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
                "company": partner_comapny_name,
                "interval": interval
            }
        )
        return latest_api_inserts_count[0]["api_inserts_count"]

