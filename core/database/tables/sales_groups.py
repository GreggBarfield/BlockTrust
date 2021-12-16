import json
from core.database.no_value import NoValue
from ..tables import zip_codes

NO_VALUE = NoValue()

class SalesGroupsException(Exception):
    """Sales groups generic exception."""

    def __init__(self, reason):
        """Constructor for SalesGroupsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


"""
Sales group "reported" column is for user-reported information, aka untrustworthy
The object is NOT sanitized whatsoever
It comes directly from clients
For convention purposes, the following details how to use the reported column

{
    "count": Number cows,
    "breeds": List of breed names,
    "weight": base weight,
    "weight_variance": weight variance from base weight (string),
    https://cdn-ext.agnet.tamu.edu/wp-content/uploads/2018/10/E-192-texas-adapted-genetic-strategies-for-beef-cattle-x-frame-score-frame-size-and-weight.pdf
    "usda_frame_size": USDA Frame Size (Small, Medium, or Large),
    "muscling": muscling score, "Light" or "Heavy",
    "horns": "Horns" or "No Horns",
    "preconditioning_program": string,
    "vaccinations": List of vaccination names,
    "implants": List of implant names,
    "castrated": Method name, or "Not Castrated",
    "process_verified_program": name or "None",
    "feeding_programs": list of strings,
    "comments": plaintext field
}
"""


class SalesGroups:
    """Handler for sales groups.
    """

    _STANDARD_SELECT = """
        SELECT sales_groups.*, accounts.name AS account_name,
                auction_sales.name AS auction_sale_name
            FROM sales_groups
            LEFT JOIN accounts ON sales_groups.account=accounts.id
            LEFT JOIN auction_sales ON sales_groups.auction_sale=auction_sales.id
    """

    def __init__(self, db):
        self._db = db

    def _translate_json(self, d):
        to_process = d

        if not isinstance(d, list):
            to_process = [d]

        for d_actual in to_process:
            if d_actual is not None:
                if d_actual["reported"] is not None:
                    d_actual["reported"] = json.loads(d_actual["reported"])
        return d

    def get_sales_group_by_id(self, row_id):
        """Gets a sales group row by an ID.

        Params:
            row_id: the row id

        Returns:
            A dictionary (w/ JSON pre-converted)

            Enhanced with account_name, auction_sale_name

        Raises:
            SalesGroupsException
        """
        sales_groups = self._db.execute_d(
            SalesGroups._STANDARD_SELECT + """
                WHERE sales_groups.id=%(id)s
            """,
            {
                "id": row_id
            }
        )
        if len(sales_groups) != 1:
            raise SalesGroupsException("No sales group found with that ID.")
        return self._translate_json(sales_groups[0])

    def get_sales_groups(self, account_id=NO_VALUE, is_archived=NO_VALUE):
        """Gets sales group rows.

        Params:
            account: the account id

        Returns:
            A list of dictionaries

            Enhanced with account_name, auction_sale_name

        Raises:
            SalesGroupsException
        """
        # base query
        base_query = SalesGroups._STANDARD_SELECT

        query_conditions = []
        query_values = {}

        if account_id is not NO_VALUE:
            query_conditions.append(" sales_groups.account = %(account_id)s")
            query_values["account_id"] = account_id
        
        if is_archived is not NO_VALUE:
            query_conditions.append(" sales_groups.is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        sales_groups = self._db.execute_d(query, query_values)
        return self._translate_json(sales_groups)

    def insert(self, account_id, reported):
        """Inserts a new row.

        Params:
            account_id: The owner of sales group
            reported: A dictionary of the user's self-reported information

        Returns:
            The sales group row inserted
        """

        self._db.execute(
            """INSERT INTO sales_groups
                (account, reported, eid_group)
                VALUES (%(account)s, %(reported)s, %(eid_group)s)
            """,
            {
                "account": account_id,
                "reported": json.dumps(reported),  # Does this need to be converted to a string first?
                "eid_group": self._db.eid_groups.new_group(owner=account_id)
            }
        )
        return self.get_sales_group_by_id(self._db.last_row_id())

    def update_sales_group(self, row_id, reported, published, zip_code, delivery_location, start, end, auction_sale, group_name, is_archived):
        """Updates a row.

        Params:
            row_id: The row ID
            reported: New data to be updated for reported col (dict)
            published: A number for the reported col
            zip_code: The zip code
            delivery_location: city and state of the zip code
            start: The start time
            end: The end time
            auction_sale: The auction sale ID
        """
        market_location = self._db.zip_codes.get_locations(zip_code)
        self._db.execute(
            """UPDATE sales_groups
                SET reported=%(reported)s, published=%(published)s,
                    start=%(start)s, end=%(end)s, zip=%(zip)s, market_location = %(market_location)s, delivery_location =  %(delivery_location)s,
                    auction_sale=%(auction_sale)s, group_name=%(group_name)s , is_archived=%(is_archived)s
                WHERE id=%(id)s
            """,
            {
                "reported": json.dumps(reported),
                "published": published,
                "id": row_id,
                "start": start,
                "end": end,
                "zip": zip_code,
                "market_location": market_location,
                "delivery_location": delivery_location,
                "auction_sale": auction_sale,
                "group_name": group_name,
                "is_archived":is_archived
            }
        )

    def search_within(
        self, zip_code, miles, start, end, skip=0, limit=10, is_archived=0,
        breed=None, minimum_weight=None, preconditioning_program=None, process_verified_program=None
    ):
        """Searches for sales groups.

        Params:
            zip_code: Origin zip code
            miles: Radius in miles
            start: Start time
            end: End time
            skip: Number of records to skip
            limit: Number of records to select
            breed, minimum_weight, preconditioning_program, process_verified_program:
                Searches in reported, None (default) to disable

        Returns:
            A list of sales group rows

            Enhanced with account_name, auction_sale_name
        """
        zip_codes = self._db.zip_codes.zips_nearby_zip(zip_code, miles)

        # TODO: Optimize
        # TODO: Add skip, limit

        additionals = []
        sql_additionals_total = ""

        if breed is not None:
            sql_additionals_total += "AND JSON_CONTAINS(reported, %s, '$.breeds')"
            additionals.append(json.dumps(breed))

        if preconditioning_program is not None:
            sql_additionals_total += "AND JSON_CONTAINS(reported, %s, '$.preconditioning_program')"
            additionals.append(json.dumps(preconditioning_program))

        if process_verified_program is not None:
            sql_additionals_total += "AND JSON_CONTAINS(reported, %s, '$.process_verified_program')"
            additionals.append(json.dumps(process_verified_program))

        if minimum_weight is not None:
            sql_additionals_total += "AND JSON_EXTRACT(reported, '$.weight') >= %s"
            additionals.append(minimum_weight)

        sql_zip_codes = ','.join(("%s" for i in zip_codes))
        sql = SalesGroups._STANDARD_SELECT + """
                WHERE
                    (
                        %s <= start AND start <= %s OR
                        %s <= end AND end <= %s
                    )
                    AND sales_groups.is_archived = %s
                    AND sales_groups.published > 0
                    AND sales_groups.zip IN (""" + sql_zip_codes + """)
                    """ + sql_additionals_total + """
        """

        sales_groups = self._db.execute_d(
            sql,
            [start, end, start, end, is_archived] + zip_codes + additionals
        )
        return self._translate_json(sales_groups)
