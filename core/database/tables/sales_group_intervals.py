import json

class SalesGroupIntervalsException(Exception):
    """SalesGroupIntervals generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupIntervalsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class SalesGroupIntervals:

    def __init__(self, db):
        self._db = db

    def remove_intervals(self, sales_group_id):
        """Removes all intervals for a sales group.

        Params:
            sales_group_id: The ID of the sales group to remove intervals for.
        """
        self._db.execute(
            """
                DELETE FROM sales_group_intervals
                    WHERE sales_group=%(sales_group)s
            """,
            {
                "sales_group": sales_group_id
            }
        )

    def set_intervals(self, sales_group_id, intervals):
        """Sets the intervals for a sales group.

        Params:
            sales_group_id: The sales group ID to set intervals for
            intervals: A list of
                Dictionaries that contain
                    start: The start time (unix epoch)
                    end: The end time (unix epoch)
                    zip: The zip code
                    data: json serializable object
        """
        self.remove_intervals(sales_group_id)
        if len(intervals) > 0:
            sql_single_value = "(%s, %s, %s, %s, %s)"
            sql_values = ','.join([sql_single_value for i in intervals])
            sql = """INSERT INTO sales_group_intervals
                (sales_group, start, end, zip, data)
                VALUES (""" + sql_values + """)
            """
            values = [
                (
                    interval["sales_group"],
                    interval["start"],
                    interval["end"],
                    interval["zip"],
                    json.dumps(interval["data"])
                )
                for interval in intervals
            ]
            self._db.execute(sql, values)

    def search_intervals_within(self, zip_code, miles, skip=0, limit=10):
        """Searches for sales group intervals with filters.

        Ordered by how close the results are.

        Params:
            zip_code: The origin ZIP code
            miles: radius in miles
            skip: Records to skip (after applying order)
            limit: Records to select
        
        Returns:
            A list of
                Dictionaries of
                    intervals: Applicable intervals. A list of
                        Dictionaries of
                            start, end, data, zip, sales_group
                    sales_group
                    
        """
        pass
