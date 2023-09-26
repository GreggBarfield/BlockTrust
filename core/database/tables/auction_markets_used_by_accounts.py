from ..no_value import NoValue

NO_VALUE = NoValue()

class AuctionMarketsUsedByAccounts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, auction_market_id=None):
        """
        Inserts a row for an auction market used by an account

        Params:
            account_id: ID of the account
            auction_market_id: ID of the Auction Market
        """
        self._db.execute(
            """
            INSERT INTO auction_markets_used_by_accounts (account_id, auction_market_id)
            VALUES (%(account_id)s, %(auction_market_id)s)
            """,
            {
                "account_id": account_id,
                "auction_market_id": auction_market_id
            }
        )
    
    def get(self, id=NO_VALUE, account_id=NO_VALUE, auction_market_id=NO_VALUE):
        """
        Gets the auction markets used by an account based on attributes provided
        
        Params:
            id: ID of the row
            account_id: ID of the account
            auction_market_id: ID of the Auction Market

        Returns:
            The matching rows or an empty list
        """
        base_query = "SELECT * FROM auction_markets_used_by_accounts"
        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if auction_market_id is not NO_VALUE:
            query_conditions.append(" auction_market_id = %(auction_market_id)s")
            query_values["auction_market_id"] = auction_market_id
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        auction_markets_used_by_accounts_rows = self._db.execute_d(query, query_values)
        if len(auction_markets_used_by_accounts_rows) > 0:
            return auction_markets_used_by_accounts_rows
        else:
            return []