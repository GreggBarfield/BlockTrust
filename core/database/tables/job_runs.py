# from ..no_value import NoValue
# from ..frag import frag


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

    def get_by_date(self, date):
        """Gets an Job Run by an ID.

        Params:
            id: the job run id
        
        Returns:
            An Dictionary object

        Raises:
            
        """
        job_run_rows = self._db.execute_d(
            """SELECT * FROM job_runs WHERE create_timestamp >=  DATE(%(date)s) AND create_timestamp < (DATE(%(date)s) + INTERVAL 1 DAY);

            """,
            {
                "date": date
            }
        )
        return job_run_rows

    def insert(self, name, file, routine):
        """Inserts a new row.

        Params:
            name: The owner of sales group
            file: A dictionary of the user's self-reported information

        Returns:
            The  job run ID inserted
        """
        try:
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
        except Exception as e:
            print(e)