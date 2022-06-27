import json
from core.database.no_value import NoValue
from core.database.tables.auction_sales import AuctionSales
from core.database.tables.files import Files
from core.database.const.zip_codes_data import ZIP_CODES

from ...common_exceptions import ExportException

NO_VALUE = NoValue()
sales_group_cols = ("id", "reported", "account", "published", "start", "end", "zip", "market_location",
                    "delivery_location", "auction_sale", "group_name", "is_archived", "delivery_location_type",
                    "price", "sold", "is_sold", "buyer_account_id", "accept_offers")


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
        SELECT sales_groups.*, accounts.name AS account_name, accounts.is_stripe_charges_enabled AS is_account_charges_enabled,
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

    def get_sales_groups_and_data(self, account_id=NO_VALUE, is_archived=NO_VALUE):
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
                (account, reported)
                VALUES (%(account)s, %(reported)s)
            """,
            {
                "account": account_id,
                "reported": json.dumps(reported)  # Does this need to be converted to a string first?
            }
        )
        return self.get_sales_group_by_id(self._db.last_row_id())

    def insert_new_sales_group(self, reported, published=None, zip_code=None, account=None,
                               delivery_location=None, start=None, end=None, auction_sale=None,
                               group_name=None, is_archived=None, delivery_location_type=None, price=None,
                               category=None, breed_comments=None, weighing_conditions=None,
                               are_annual_cattle_herd_vaccinations_given=None, accept_offers=None):
        """
        Inserts a new sales group into the table
        Params:
            account: Account owning the sales group
            reported: Data to be added in reported col (dict)
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            start: The start time
            end: The end time
            auction_sale: The auction sale ID
            is_archived: 0 for no, 1 for yes
            accept_offers: Accept offers or not
            category: Category of the sales group
            breed_comments: Breed comments for sales group
            weighing_conditions: Weighing conditions comment for sales group

        Returns:
            Sales group ID of new Sales group
        """
        self._db.execute(
            """
            INSERT INTO sales_groups (account, reported, published, zip, delivery_location, start, end, auction_sale,
            group_name, is_archived, delivery_location_type, price, category, breed_comments, weighing_conditions,
            are_annual_cattle_herd_vaccinations_given)
            VALUES
            (%(account)s, %(reported)s, %(published)s, %(zip_code)s, %(delivery_location)s, %(start)s, %(end)s,
            %(auction_sale)s, %(group_name)s, %(is_archived)s, %(delivery_location_type)s, %(price)s, %(category)s,
            %(breed_comments)s, %(weighing_conditions)s, %(are_annual_cattle_herd_vaccinations_given)s, %(accept_offers)s)
            """, {
                "account": account,
                "reported": json.dumps(reported),
                "published": published,
                "zip_code": zip_code,
                "delivery_location": delivery_location,
                "start": start,
                "end": end,
                "auction_sale": auction_sale,
                "group_name": group_name,
                "is_archived": is_archived,
                "delivery_location_type": delivery_location_type,
                "price": price,
                "accept_offers": accept_offers,
                "category": category,
                "breed_comments": breed_comments,
                "weighing_conditions": weighing_conditions,
                "are_annual_cattle_herd_vaccinations_given": are_annual_cattle_herd_vaccinations_given
            }
        )
        return self._db.last_row_id()

    def update_sales_group(self, id, reported=NO_VALUE, published=NO_VALUE,
        zip_code=NO_VALUE, delivery_location=NO_VALUE, start=NO_VALUE, end=NO_VALUE,
        auction_sale=NO_VALUE, group_name=NO_VALUE, is_archived=NO_VALUE,
        delivery_location_type=NO_VALUE, price=NO_VALUE, is_sold=NO_VALUE, buyer_account_id=NO_VALUE,
        category=NO_VALUE, breed_comments=NO_VALUE, weighing_conditions=NO_VALUE,
        are_annual_cattle_herd_vaccinations_given=NO_VALUE, accept_offers=NO_VALUE):
        """Updates a row.

        Params:
            id: The row ID
            reported: New data to be updated for reported col (dict)
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            start: The start time
            end: The end time
            auction_sale: The auction sale ID
            is_archived: 0 for no, 1 for yes
            category: Category of the sales group
            breed_comments: Breed comments for sales group
            weighing_conditions: Weighing conditions comment for sales group
        """

        # base query
        base_query = "UPDATE sales_groups "

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if reported is not NO_VALUE:
            query_conditions.append(" reported = %(reported)s")
            query_values["reported"] = json.dumps(reported)
        if published is not NO_VALUE:
            query_conditions.append(" published = %(published)s")
            query_values["published"] = published
        if zip_code is not NO_VALUE:
            query_conditions.append(" zip = %(zip_code)s")
            query_values["zip_code"] = zip_code
            market_location = self._db.zip_codes.get_locations(zip_code)
            query_conditions.append(" market_location = %(market_location)s")
            query_values["market_location"] = market_location
        if delivery_location is not NO_VALUE:
            query_conditions.append(" delivery_location = %(delivery_location)s")
            query_values["delivery_location"] = delivery_location
        if start is not NO_VALUE:
            query_conditions.append(" start = %(start)s")
            query_values["start"] = start
        if end is not NO_VALUE:
            query_conditions.append(" end = %(end)s")
            query_values["end"] = end
        if auction_sale is not NO_VALUE:
            query_conditions.append(" auction_sale = %(auction_sale)s")
            query_values["auction_sale"] = auction_sale
        if group_name is not NO_VALUE:
            query_conditions.append(" group_name = %(group_name)s")
            query_values["group_name"] = group_name
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if delivery_location_type is not NO_VALUE:
            query_conditions.append(" delivery_location_type = %(delivery_location_type)s")
            query_values["delivery_location_type"] = delivery_location_type
        if price is not NO_VALUE:
            query_conditions.append(" price = %(price)s")
            query_values["price"] = price
        if is_sold is not NO_VALUE:
            query_conditions.append(" is_sold = %(is_sold)s")
            query_values["is_sold"] = is_sold
        if buyer_account_id is not NO_VALUE:
            query_conditions.append(" buyer_account_id = %(buyer_account_id)s")
            query_values["buyer_account_id"] = buyer_account_id
        if accept_offers is not NO_VALUE:
            query_conditions.append(" accept_offers = %(accept_offers)s")
            query_values["accept_offers"] = accept_offers
        if category is not NO_VALUE:
            query_conditions.append(" category = %(category)s")
            query_values["category"] = category
        if breed_comments is not NO_VALUE:
            query_conditions.append(" breed_comments = %(breed_comments)s")
            query_values["breed_comments"] = breed_comments
        if weighing_conditions is not NO_VALUE:
            query_conditions.append(" weighing_conditions = %(weighing_conditions)s")
            query_values["weighing_conditions"] = weighing_conditions
        if are_annual_cattle_herd_vaccinations_given is not NO_VALUE:
            query_conditions.append(" are_annual_cattle_herd_vaccinations_given = %(are_annual_cattle_herd_vaccinations_given)s")
            query_values["are_annual_cattle_herd_vaccinations_given"] = are_annual_cattle_herd_vaccinations_given

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Sales Group")

    def search_within(
        self, zip_code, miles, start, end, skip=0, limit=10, is_archived=0,
        category=None, breed=None, minimum_weight=None, preconditioning_program=None, process_verified_program=None
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

        if category is not None:
            sql_additionals_total += "AND category = %s"
            additionals.append(category)

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

    def validate_or_fail_sales_group(self, group_name, zip, account_id, delivery_location_type, count, weight, weight_variance,
            breeds, start, end, auction_sale, delivery_location, auction_market_location, images, price, category):
        """
        Validates that the values received for a sales group is valid

        Params:
            group_name: Nickname for the sales group
            zip: Zip code of the sales group
            account_id: Account ID of the owner account
            delivery_location_type: Off ranch or auction market
            count: Cattle count
            weight: Average weight for cattle in group
            weight_variance: Variance of weight average
            breeds: Breeds of cattle in group
            usda_frame_size: Frame size
            muscling: Muscling type
            horns: Horns type
            start: Start date for sale
            end: End date for sale
            auction_sale: Auction sale
            delivery_location: Off ranch delivery location
            auction_market_location: Auction market value
            images: Images for sales group
            category: Category for the sales group

        Raises:
            ExportException if field is invalid
        """
        for image in images:
            if not Files(self._db).is_owner(None, account_id, image):
                raise ExportException("Image " + str(image) + " is not owned by the selected account.")
        # Checking if required values are present
        if len(group_name.strip()) == 0:
            raise ExportException("Sales group name cannot be blank")
        if count is None:
            raise ExportException("Total animals cannot be 0")
        if zip is None:
            raise ExportException("Zip code cannot be blank")
        if zip not in ZIP_CODES:
            raise ExportException("Sorry, that zip code could not be found.")
        if start is None or end is None:
            raise ExportException("Sorry, start or end date missing.")
        if start > end:
            raise ExportException("Sorry, check the market start and end dates (specifically the order).")
        if delivery_location_type is None:
            raise ExportException("Sale location type is not selected.")
        elif delivery_location_type == "Off Ranch":
            if len(delivery_location.strip()) == 0:
                raise ExportException("Delivery Location cannot be blank")
        elif delivery_location_type == "Auction":
            if auction_market_location == "None":
                raise ExportException("Please select an auction market location")
        if category == "":
            raise ExportException("Please select a category")
        if len(breeds) == 0:
            raise ExportException("Please select one or more breeds")
        if weight is None:
            raise ExportException("Base weight does not have a value")
        if len(weight_variance.strip()) == 0:
            raise ExportException("Weight variance does not have a value")
        if auction_sale is not None:
            # it was changed to a non-None value, verify new is published
            if not AuctionSales(self._db).auction_sales.get_auction_sale_by_id(auction_sale)["published"]:
                raise ExportException("Auction sale specified is not published yet.")
        if price == "0":
            raise ExportException("Sales Group price is not provided")

    def get_sales_groups(self, id=NO_VALUE, reported=NO_VALUE, published=NO_VALUE, zip_code=NO_VALUE,
                         delivery_location=NO_VALUE, start=NO_VALUE, end=NO_VALUE, auction_sale=NO_VALUE,
                         group_name=NO_VALUE, is_archived=NO_VALUE, delivery_location_type=NO_VALUE, price=NO_VALUE,
                         is_sold=NO_VALUE, buyer_account_id=NO_VALUE, account_id=NO_VALUE, category=NO_VALUE,
                         breed_comments=NO_VALUE, weighing_conditions=NO_VALUE, sales_group_cols=[]):
        """
        Gets the sales groups based on attributes provided
        
        Params:
            id: The sales group ID
            reported: Reported data for sales group
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            start: The start time
            end: The end time
            auction_sale: The auction sale ID
            is_archived: 0 for no, 1 for yes
            category: Category of the sales group
            breed_comments: Breed comments for sales group
            weighing_conditions: Weighing conditions comment for sales group

        Returns:
            A list of sales group dictionaries or an empty list
        """
        # base query
        base_query = "SELECT"
        if len(sales_group_cols) > 0:
            incorrect_cols = [col for col in sales_group_cols if col not in sales_group_cols]
            if len(incorrect_cols) > 0:
                raise Exception("Selected column(s) " + ",".join(incorrect_cols) + " don't exist in matches table")
            base_query += " " + ",".join(c for c in sales_group_cols)
        else:
            base_query += " *"
        base_query += " FROM sales_groups "
        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account = %(account_id)s")
            query_values["account_id"] = account_id
        if reported is not NO_VALUE:
            query_conditions.append(" reported = %(reported)s")
            query_values["reported"] = json.dumps(reported)
        if published is not NO_VALUE:
            query_conditions.append(" published = %(published)s")
            query_values["published"] = published
        if zip_code is not NO_VALUE:
            query_conditions.append(" zip = %(zip_code)s")
            query_values["zip_code"] = zip_code
            market_location = self._db.zip_codes.get_locations(zip_code)
            query_conditions.append(" market_location = %(market_location)s")
            query_values["market_location"] = market_location
        if delivery_location is not NO_VALUE:
            query_conditions.append(" delivery_location = %(delivery_location)s")
            query_values["delivery_location"] = delivery_location
        if start is not NO_VALUE:
            query_conditions.append(" start = %(start)s")
            query_values["start"] = start
        if end is not NO_VALUE:
            query_conditions.append(" end = %(end)s")
            query_values["end"] = end
        if auction_sale is not NO_VALUE:
            query_conditions.append(" auction_sale = %(auction_sale)s")
            query_values["auction_sale"] = auction_sale
        if group_name is not NO_VALUE:
            query_conditions.append(" group_name = %(group_name)s")
            query_values["group_name"] = group_name
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if delivery_location_type is not NO_VALUE:
            query_conditions.append(" delivery_location_type = %(delivery_location_type)s")
            query_values["delivery_location_type"] = delivery_location_type
        if price is not NO_VALUE:
            query_conditions.append(" price = %(price)s")
            query_values["price"] = price
        if is_sold is not NO_VALUE:
            query_conditions.append(" is_sold = %(is_sold)s")
            query_values["is_sold"] = is_sold
        if buyer_account_id is not NO_VALUE:
            query_conditions.append(" buyer_account_id = %(buyer_account_id)s")
            query_values["buyer_account_id"] = buyer_account_id
        if category is not NO_VALUE:
            query_conditions.append(" category = %(category)s")
            query_values["category"] = category
        if breed_comments is not NO_VALUE:
            query_conditions.append(" breed_comments = %(breed_comments)s")
            query_values["breed_comments"] = breed_comments
        if weighing_conditions is not NO_VALUE:
            query_conditions.append(" weighing_conditions = %(weighing_conditions)s")
            query_values["weighing_conditions"] = weighing_conditions

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        sales_groups = self._db.execute_d(query, query_values)
        if len(sales_groups) > 0:
            return sales_groups
        return []