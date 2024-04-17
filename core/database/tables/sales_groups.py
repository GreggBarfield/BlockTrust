import json
from time import time
from core.database.no_value import NoValue
from core.database.tables.auction_sales import AuctionSales
from core.database.tables.files import Files
from core.utilities.constants import SECONDS_IN_ONE_DAY
from core.utilities.data.zip_codes_data import ZIP_CODES
from core.utilities.zip_codes import get_locations, zips_nearby_zip

from ...common_exceptions import ExportException

NO_VALUE = NoValue()
sales_group_cols = ("id", "reported", "account", "published", "sale_date", "zip", "market_location",
                    "delivery_location", "auction_sale", "group_name", "is_archived", "delivery_location_type",
                    "price", "sold", "is_sold", "buyer_account_id", "accept_offers")

TARGET_DATE_KEYS_TO_DESC = {
    "ASAP": "ASAP",
    "<30": "Under 30 Days",
    "<60": "Under 60 Days",
    "<90": "Under 90 Days",
    ">90": "Over 90 Days"
}


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
        SELECT sales_groups.*, accounts.name AS account_name, accounts.is_stripe_payouts_enabled AS is_account_payouts_enabled,
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

    def insert_sales_group(self, reported, published=None, zip_code=None, account=None,
                           delivery_location=None, sale_date=None, auction_sale=None,
                           group_name=None, is_archived=None, delivery_location_type=None, price=None,
                           category=None, breed_comments=None, weighing_conditions=None, auction_market_id=None,
                           seller_id=None, vaccination_date=None, vaccination_summary=None, herd_sire=None,
                           ranch_source_county=None, ranch_size=None, home_raised=None, family_farm_or_ranch=None,
                           show_account_carcass_data=None, is_api_insert=None):
        """
        Inserts a new sales group into the table
        Params:
            account: Account owning the sales group
            reported: Data to be added in reported col (dict)
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            sale_date: The sale_date time
            auction_sale: The auction sale ID
            is_archived: 0 for no, 1 for yes
            category: Category of the sales group
            breed_comments: Breed comments for sales group
            weighing_conditions: Weighing conditions comment for sales group
            show_account_carcass_data: Show carcass data for account
            is_api_insert: Indicates if sales group is an API insert 

        Returns:
            Sales group ID of new Sales group
        """
        self._db.execute(
            """
            INSERT INTO sales_groups (account, reported, published, zip, delivery_location, auction_market_id, sale_date,
                auction_sale, group_name, is_archived, delivery_location_type, price, category, breed_comments, weighing_conditions,
                seller_id, vaccination_date, vaccination_summary, herd_sire, ranch_source_county, ranch_size, 
                home_raised, family_farm_or_ranch, show_account_carcass_data, is_api_insert
            )
            VALUES (
                %(account)s, %(reported)s, %(published)s, %(zip_code)s, %(delivery_location)s, %(auction_market_id)s, %(sale_date)s,
                %(auction_sale)s, %(group_name)s, %(is_archived)s, %(delivery_location_type)s, %(price)s, %(category)s,
                %(breed_comments)s, %(weighing_conditions)s, %(seller_id)s, %(vaccination_date)s,
                %(vaccination_summary)s, %(herd_sire)s, %(ranch_source_county)s, %(ranch_size)s, %(home_raised)s,
                %(family_farm_or_ranch)s, %(show_account_carcass_data)s, %(is_api_insert)s
            )
            """, {
                "account": account,
                "reported": json.dumps(reported),
                "published": published,
                "zip_code": zip_code,
                "delivery_location": delivery_location,
                "auction_market_id": auction_market_id,
                "sale_date": sale_date,
                "auction_sale": auction_sale,
                "group_name": group_name,
                "is_archived": is_archived,
                "delivery_location_type": delivery_location_type,
                "price": price,
                "category": category,
                "breed_comments": breed_comments,
                "weighing_conditions": weighing_conditions,
                "seller_id": seller_id,
                "vaccination_date": vaccination_date,
                "vaccination_summary": vaccination_summary,
                "herd_sire": herd_sire,
                "ranch_source_county": ranch_source_county,
                "ranch_size": ranch_size,
                "home_raised": home_raised,
                "family_farm_or_ranch": family_farm_or_ranch,
                "show_account_carcass_data": show_account_carcass_data,
                "is_api_insert": is_api_insert
            }
        )
        return self._db.last_row_id()

    def update_sales_group(self, id, reported=NO_VALUE, published=NO_VALUE,
                           zip_code=NO_VALUE, delivery_location=NO_VALUE, auction_market_id=NO_VALUE,
                           sale_date=NO_VALUE, auction_sale=NO_VALUE, group_name=NO_VALUE, is_archived=NO_VALUE,
                           delivery_location_type=NO_VALUE, price=NO_VALUE, is_sold=NO_VALUE, buyer_account_id=NO_VALUE,
                           category=NO_VALUE, breed_comments=NO_VALUE, weighing_conditions=NO_VALUE,
                           seller_id=NO_VALUE, vaccination_date=NO_VALUE, vaccination_summary=NO_VALUE,
                           herd_sire=NO_VALUE, ranch_source_county=NO_VALUE, ranch_size=NO_VALUE, home_raised=NO_VALUE,
                           family_farm_or_ranch=NO_VALUE, show_account_carcass_data=NO_VALUE, is_paid=NO_VALUE,
                           payment_id=NO_VALUE):
        """Updates a row.

        Params:
            id: The row ID
            reported: New data to be updated for reported col (dict)
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            sale_date: The sale_date time
            auction_sale: The auction sale ID
            is_archived: 0 for no, 1 for yes
            category: Category of the sales group
            breed_comments: Breed comments for sales group
            weighing_conditions: Weighing conditions comment for sales group
            show_account_carcass_data: Shoe carcass data for account
        """

        # base query
        base_query = "UPDATE sales_groups "

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if reported is not NO_VALUE:
            query_conditions.append("reported = %(reported)s")
            query_values["reported"] = json.dumps(reported)
        if published is not NO_VALUE:
            query_conditions.append("published = %(published)s")
            query_values["published"] = published
        if zip_code is not NO_VALUE:
            query_conditions.append("zip = %(zip_code)s")
            query_values["zip_code"] = zip_code
            if zip_code:
                market_location = get_locations(zip_code)
                query_conditions.append("market_location = %(market_location)s")
                query_values["market_location"] = market_location
        if delivery_location is not NO_VALUE:
            query_conditions.append("delivery_location = %(delivery_location)s")
            query_values["delivery_location"] = delivery_location
        if auction_market_id is not NO_VALUE:
            query_conditions.append("auction_market_id = %(auction_market_id)s")
            query_values["auction_market_id"] = auction_market_id
        if sale_date is not NO_VALUE:
            query_conditions.append("sale_date = %(sale_date)s")
            query_values["sale_date"] = sale_date
        if auction_sale is not NO_VALUE:
            query_conditions.append("auction_sale = %(auction_sale)s")
            query_values["auction_sale"] = auction_sale
        if group_name is not NO_VALUE:
            query_conditions.append("group_name = %(group_name)s")
            query_values["group_name"] = group_name
        if is_archived is not NO_VALUE:
            query_conditions.append("is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if delivery_location_type is not NO_VALUE:
            query_conditions.append("delivery_location_type = %(delivery_location_type)s")
            query_values["delivery_location_type"] = delivery_location_type
        if price is not NO_VALUE:
            query_conditions.append("price = %(price)s")
            query_values["price"] = price
        if is_sold is not NO_VALUE:
            query_conditions.append("is_sold = %(is_sold)s")
            query_values["is_sold"] = is_sold
        if buyer_account_id is not NO_VALUE:
            query_conditions.append("buyer_account_id = %(buyer_account_id)s")
            query_values["buyer_account_id"] = buyer_account_id
        if category is not NO_VALUE:
            query_conditions.append("category = %(category)s")
            query_values["category"] = category
        if breed_comments is not NO_VALUE:
            query_conditions.append("breed_comments = %(breed_comments)s")
            query_values["breed_comments"] = breed_comments
        if weighing_conditions is not NO_VALUE:
            query_conditions.append("weighing_conditions = %(weighing_conditions)s")
            query_values["weighing_conditions"] = weighing_conditions
        if seller_id is not NO_VALUE:
            query_conditions.append("seller_id = %(seller_id)s")
            query_values["seller_id"] = seller_id
        if vaccination_date is not NO_VALUE:
            query_conditions.append("vaccination_date = %(vaccination_date)s")
            query_values["vaccination_date"] = vaccination_date
        if vaccination_summary is not NO_VALUE:
            query_conditions.append("vaccination_summary = %(vaccination_summary)s")
            query_values["vaccination_summary"] = vaccination_summary
        if herd_sire is not NO_VALUE:
            query_conditions.append("herd_sire = %(herd_sire)s")
            query_values["herd_sire"] = herd_sire
        if ranch_source_county is not NO_VALUE:
            query_conditions.append("ranch_source_county = %(ranch_source_county)s")
            query_values["ranch_source_county"] = ranch_source_county
        if ranch_size is not NO_VALUE:
            query_conditions.append("ranch_size = %(ranch_size)s")
            query_values["ranch_size"] = ranch_size
        if home_raised is not NO_VALUE:
            query_conditions.append("home_raised = %(home_raised)s")
            query_values["home_raised"] = home_raised
        if family_farm_or_ranch is not NO_VALUE:
            query_conditions.append("family_farm_or_ranch = %(family_farm_or_ranch)s")
            query_values["family_farm_or_ranch"] = family_farm_or_ranch
        if show_account_carcass_data is not NO_VALUE:
            query_conditions.append("show_account_carcass_data = %(show_account_carcass_data)s")
            query_values["show_account_carcass_data"] = show_account_carcass_data
        if is_paid is not NO_VALUE:
            query_conditions.append("is_paid = %(is_paid)s")
            query_values["is_paid"] = is_paid
        if payment_id is not NO_VALUE:
            query_conditions.append("payment_id = %(payment_id)s")
            query_values["payment_id"] = payment_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Sales Group")

    def search_within(
        self, zip_code, miles, sale_date, skip=0, limit=10, is_archived=0,
        categories=None, breeds=None, minimum_weight=None, preconditioning_program=None, programs=None,
        maximum_weight=None, target_date_description=None
    ):
        """Searches for sales groups.

        Params:
            zip_code: Origin zip code
            miles: Radius in miles
            sale_date: sale_date time
            skip: Number of records to skip
            limit: Number of records to select
            breed, minimum_weight, preconditioning_program, process_verified_program:
                Searches in reported, None (default) to disable

        Returns:
            A list of sales group rows

            Enhanced with account_name, auction_sale_name
        """
        zip_codes = zips_nearby_zip(zip_code, miles)

        additionals = []
        sql_additionals_total = ""

        if categories is not None:
            categories_clause = []
            for category in categories:
                categories_clause.append("%s")
                additionals.append(category)
            sql_additionals_total += f" AND category IN ({','.join(categories_clause)})"

        if breeds is not None:
            breeds_clause = []
            for breed in breeds:
                breeds_clause.append("JSON_CONTAINS(reported, %s, '$.breeds')")
                additionals.append(json.dumps(breed))
            sql_additionals_total += "AND (" + " OR ".join(breeds_clause) + ")"

        if preconditioning_program is not None:
            sql_additionals_total += " AND JSON_CONTAINS(reported, %s, '$.preconditioning_program')"
            additionals.append(json.dumps(preconditioning_program))

        if programs is not None:
            programs_clause = []
            for p in programs:
                programs_clause.append("JSON_CONTAINS(reported, %s, '$.program')")
                additionals.append(json.dumps(p))
            sql_additionals_total += f"AND ({' OR '.join(programs_clause)})"

        if minimum_weight is not None:
            sql_additionals_total += " AND JSON_EXTRACT(reported, '$.weight') >= %s"
            additionals.append(minimum_weight)

        if maximum_weight is not None:
            sql_additionals_total += " AND JSON_EXTRACT(reported, '$.weight') <= %s"
            additionals.append(maximum_weight)

        if target_date_description is not None:
            if target_date_description == TARGET_DATE_KEYS_TO_DESC["<30"]:
                required_time = int(time()) + SECONDS_IN_ONE_DAY * 30
                sql_additionals_total += " AND sale_date < %s"
                additionals.append(required_time)
            elif target_date_description == TARGET_DATE_KEYS_TO_DESC["<60"]:
                required_time = int(time()) + SECONDS_IN_ONE_DAY * 60
                sql_additionals_total += " AND sale_date < %s"
                additionals.append(required_time)
            elif target_date_description == TARGET_DATE_KEYS_TO_DESC["<90"]:
                required_time = int(time()) + SECONDS_IN_ONE_DAY * 90
                sql_additionals_total += " AND sale_date < %s"
                additionals.append(required_time)
            elif target_date_description == TARGET_DATE_KEYS_TO_DESC[">90"]:
                required_time = int(time()) + SECONDS_IN_ONE_DAY * 90
                sql_additionals_total += " AND sale_date >= %s"
                additionals.append(required_time)

        sql_zip_codes = ','.join(("%s" for i in zip_codes))

        sql = SalesGroups._STANDARD_SELECT + """
                WHERE
                    (
                        %s <= sale_date
                    )
                    AND sales_groups.is_archived = %s
                    AND sales_groups.published > 0
                    AND sales_groups.zip IN (""" + sql_zip_codes + """)
                    """ + sql_additionals_total + """
        """

        sales_groups = self._db.execute_d(
            sql,
            [sale_date, is_archived] + zip_codes + additionals
        )
        return self._translate_json(sales_groups)

    def validate_or_fail_sales_group(self, group_name, zip, account_id, delivery_location_type, count, weight,
                                     breeds, sale_date, delivery_location, auction_market_location,
                                     images, price, category, slide, weighing_conditions, published):
        """
        Validates that the values received for a sales group is valid

        Params:
            group_name: Nickname for the sales group
            zip: Zip code of the sales group
            account_id: Account ID of the owner account
            delivery_location_type: Direct/Off Ranch or auction market
            count: Cattle count
            weight: Average weight for cattle in group
            breeds: Breeds of cattle in group
            usda_frame_size: Frame size
            muscling: Muscling type
            horns: Horns type
            sale_date: sale_date date for sale
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
        if delivery_location_type == "Direct/Off Ranch":
            if len(delivery_location.strip()) == 0:
                raise ExportException("Delivery Location cannot be blank")
        elif delivery_location_type == "Auction":
            if not auction_market_location or auction_market_location == "None":
                raise ExportException("Please select an auction market location")
        elif delivery_location_type == "Video Auction":
            if len(slide.strip()) == 0:
                raise ExportException("Video Auction Slide cannot be blank")
            if len(weighing_conditions.strip()) == 0:
                raise ExportException("Video Auction Weighing Conditions cannot be blank")
        if zip and zip not in ZIP_CODES:
            raise ExportException("Zip code is invalid")
        if published:
            if zip is None:
                raise ExportException("Zip code cannot be blank")
            if sale_date is None:
                raise ExportException("Sorry, sale date date missing.")
            if delivery_location_type is None:
                raise ExportException("Sale location type is not selected.")
            if category == "":
                raise ExportException("Please select a category")
            if len(breeds) == 0:
                raise ExportException("Please select one or more breeds")
            if weight is None:
                raise ExportException("Base weight does not have a value")
            if price == "0":
                raise ExportException("Sales Group price is not provided")

    def get_sales_groups(self, id=NO_VALUE, reported=NO_VALUE, published=NO_VALUE, zip_code=NO_VALUE,
                         delivery_location=NO_VALUE, sale_date=NO_VALUE, auction_sale=NO_VALUE,
                         group_name=NO_VALUE, is_archived=NO_VALUE, delivery_location_type=NO_VALUE, price=NO_VALUE,
                         is_sold=NO_VALUE, buyer_account_id=NO_VALUE, account_id=NO_VALUE, category=NO_VALUE,
                         breed_comments=NO_VALUE, weighing_conditions=NO_VALUE, sales_group_cols=[],
                         auction_market_id=NO_VALUE, payment_id_is_not_null=False, is_paid=NO_VALUE, account_ids=()):
        """
        Gets the sales groups based on attributes provided
        
        Params:
            id: The sales group ID
            reported: Reported data for sales group
            published: A number for the reported col
            zip_code: The zip code
            delivery_location_type: Sale location type
            delivery_location: city and state of the zip code
            sale_date: The sale_date time
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
        base_query += " FROM sales_groups"
        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append("account = %(account_id)s")
            query_values["account_id"] = account_id
        if reported is not NO_VALUE:
            query_conditions.append("reported = %(reported)s")
            query_values["reported"] = json.dumps(reported)
        if published is not NO_VALUE:
            query_conditions.append("published = %(published)s")
            query_values["published"] = published
        if zip_code is not NO_VALUE:
            query_conditions.append("zip = %(zip_code)s")
            query_values["zip_code"] = zip_code
            market_location = get_locations(zip_code)
            query_conditions.append("market_location = %(market_location)s")
            query_values["market_location"] = market_location
        if delivery_location is not NO_VALUE:
            query_conditions.append("delivery_location = %(delivery_location)s")
            query_values["delivery_location"] = delivery_location
        if sale_date is not NO_VALUE:
            query_conditions.append("sale_date = %(sale_date)s")
            query_values["sale_date"] = sale_date
        if auction_sale is not NO_VALUE:
            query_conditions.append("auction_sale = %(auction_sale)s")
            query_values["auction_sale"] = auction_sale
        if group_name is not NO_VALUE:
            query_conditions.append("group_name = %(group_name)s")
            query_values["group_name"] = group_name
        if is_archived is not NO_VALUE:
            query_conditions.append("is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if delivery_location_type is not NO_VALUE:
            query_conditions.append("delivery_location_type = %(delivery_location_type)s")
            query_values["delivery_location_type"] = delivery_location_type
        if price is not NO_VALUE:
            query_conditions.append("price = %(price)s")
            query_values["price"] = price
        if is_sold is not NO_VALUE:
            query_conditions.append("is_sold = %(is_sold)s")
            query_values["is_sold"] = is_sold
        if buyer_account_id is not NO_VALUE:
            query_conditions.append("buyer_account_id = %(buyer_account_id)s")
            query_values["buyer_account_id"] = buyer_account_id
        if category is not NO_VALUE:
            query_conditions.append("category = %(category)s")
            query_values["category"] = category
        if breed_comments is not NO_VALUE:
            query_conditions.append("breed_comments = %(breed_comments)s")
            query_values["breed_comments"] = breed_comments
        if weighing_conditions is not NO_VALUE:
            query_conditions.append("weighing_conditions = %(weighing_conditions)s")
            query_values["weighing_conditions"] = weighing_conditions
        if auction_market_id is not NO_VALUE:
            query_conditions.append("auction_market_id = %(auction_market_id)s")
            query_values["auction_market_id"] = auction_market_id
        if is_paid is not NO_VALUE:
            query_conditions.append("is_paid = %(is_paid)s")
            query_values["is_paid"] = is_paid
        if payment_id_is_not_null:
            query_conditions.append("payment_id IS NOT NULL")
        if account_ids:
            if not all(isinstance(id, int) for id in account_ids):
                raise Exception("Incorrect account id")
            query_conditions.append(f"account IN ({', '.join(str(id) for id in account_ids)})")

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        sales_groups = self._db.execute_d(query, query_values)
        if len(sales_groups) > 0:
            for sales_group in sales_groups:
                if "reported" in sales_group:
                    sales_group["reported"] = json.loads(sales_group["reported"])
            return sales_groups
        return []
