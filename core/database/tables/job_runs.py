import json
from core.database.no_value import NoValue

NO_VALUE=NoValue()

class JobRuns:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, job_run_id):
        """Gets an Job Run by an ID.

        Params:
            id: the job run id
        
        Returns:
            An Dictionary object

        Raises:
            
        """
        job_run_rows = self._db.execute_d(
            """SELECT * FROM job_runs
                WHERE id=%(id)s
            """,
            {
                "id": job_run_id
            }
        )
        return job_run_rows

    def get_job_runs(self, name=NO_VALUE, routine=NO_VALUE, created_date=NO_VALUE, job_ended_successfully=False, selectColumns=(), sort_and_order="", limit=0):
        """
        Get an job run by the values specified.

        Returns:
            A list of job run records if found else an empty list
        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        base_query = "SELECT " + selectColumns + " FROM job_runs"

        query_conditions = []
        query_values = {}

        if name is not NO_VALUE:
            query_conditions.append("name = %(name)s")
            query_values["name"] = name

        if routine is not NO_VALUE:
            query_conditions.append("routine = %(routine)s")
            query_values["routine"] = routine
        
        if created_date is not NO_VALUE:
            query_conditions.append("created_timestamp >=  DATE(%(created_date)s) AND created_timestamp < (DATE(%(created_date)s) + INTERVAL 1 DAY)")
            query_values["created_date"] = created_date
        
        if job_ended_successfully != False:
            query_conditions.append("end_timestamp IS NOT NULL")

        if len(query_conditions) > 0:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        
        if sort_and_order != "":
            combined_query_condition += " ORDER BY "+ sort_and_order

        if limit != 0:
            combined_query_condition += " LIMIT "+ str(limit)

        query = base_query + combined_query_condition
        job_run_rows = self._db.execute_d(query, query_values)
        if len(job_run_rows) > 0:
            return job_run_rows
        else:
            return []

    def insert(self, name, file, routine):
        """Inserts a new row.

        Params:
            name: The owner of sales group
            file: A dictionary of the user's self-reported information

        Returns:
            The  job run ID inserted
        """
        self._db.execute(
            """INSERT INTO job_runs
                (name, file, routine)
                VALUES (%(name)s, %(file)s, %(routine)s)
            """,
            {
                "name": name,
                "file": file,
                "routine": routine
            }
        )
        return self._db.last_row_id()

    def update_job_run(self, id, end_timestamp, details=None):
        """Inserts a new row.

        Returns:
            The  job run ID inserted
        """
        self._db.execute(
            """UPDATE job_runs SET end_timestamp = %(end_timestamp)s, details = %(details)s WHERE id=%(id)s
            """,
            {
                "end_timestamp": end_timestamp,
                "details": json.dumps(details) if details is not None else None,
                "id": id
            }
        )
