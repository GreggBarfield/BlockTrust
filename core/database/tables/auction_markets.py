from ..no_value import NoValue

NO_VALUE = NoValue()
auction_market_cols = ("id", "name", "address", "city", "state", "zip_code", "email", "phone", "is_archived")


class AuctionMarkets:

    def __init__(self, db):
        self._db = db

    def get_auction_markets(self, id=NO_VALUE, name=NO_VALUE, address=NO_VALUE, city=NO_VALUE, state=NO_VALUE,
                            zip_code=NO_VALUE, email=NO_VALUE, phone=NO_VALUE, is_archived=NO_VALUE,
                            auction_markets_order_by=NO_VALUE, auction_markets_sort_by=NO_VALUE):
        """
        Gets the auction markets based on attributes provided

        Params:
            id: ID of auction market
            name: Auction Market name
            address: Auction market address
            city: Auction market city
            state: Auction market state
            zip_code: Auction market zip code
            email: Auction market email
            phone: Auction market phone number
            is_archived: Indicates if the auction market is archived

        Returns:
            A list of auction markets or an empty list
        """
        base_query = "SELECT * FROM auction_markets"

        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if name is not NO_VALUE:
            query_conditions.append(" name = %(name)s")
            query_values["name"] = name
        if address is not NO_VALUE:
            query_conditions.append(" address = %(address)s")
            query_values["address"] = address
        if city is not NO_VALUE:
            query_conditions.append(" city = %(city)s")
            query_values["city"] = city
        if state is not NO_VALUE:
            query_conditions.append(" state = %(state)s")
            query_values["state"] = state
        if zip_code is not NO_VALUE:
            query_conditions.append(" zip_code = %(zip_code)s")
            query_values["zip_code"] = zip_code
        if email is not NO_VALUE:
            query_conditions.append(" email = %(email)s")
            query_values["email"] = email
        if phone is not NO_VALUE:
            query_conditions.append(" phone = %(phone)s")
            query_values["phone"] = phone
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if auction_markets_order_by is not NO_VALUE:
            if auction_markets_order_by not in auction_market_cols:
                raise Exception("auction_markets_order_by column doesn't exist")
            order_by_clause = "ORDER BY " + auction_markets_order_by
            if auction_markets_sort_by is not NO_VALUE:
                if auction_markets_sort_by not in ("ASC", "DESC"):
                    raise Exception("Incorrect value for auction_markets_sort_by")
                order_by_clause += " " + auction_markets_sort_by

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions) + " " + order_by_clause
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        auction_market_rows = self._db.execute_d(query, query_values)
        if len(auction_market_rows) > 0:
            return auction_market_rows
        else:
            return []

    def insert_auction_market(self, name=None, address=None, city=None, state=None,
                              email=None, phone=None, zip_code=None):
        """
        Inserts a new account market

        Params:
            id: ID of auction market
            name: Auction Market name
            address: Auction market address
            city: Auction market city
            state: Auction market state
            zip_code: Auction market zip code
            email: Auction market email
            phone: Auction market phone number
        """
        self._db.execute(
            """
            INSERT INTO auction_markets (name, address, city, state, zip_code, email, phone)
            VALUES (%(name)s, %(address)s, %(city)s, %(state)s, %(zip_code)s, %(email)s, %(phone)s)
            """,
            {
                "name": name,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "email": email,
                "phone": phone
            }
        )
        return self._db.last_row_id()
