class AuctionSalesException(Exception):
    """AuctionSalesException exception."""

    def __init__(self, reason):
        """Constructor for AuctionSalesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class AuctionSales:

    def __init__(self, db):
        self._db = db
    
    def get_auction_sale_by_id(self, auction_sale_id):
        """Gets an auction sale by its ID

        Params:
            auction_sale_id: The record to retrieve
        
        Returns:
            The row retrieved

            Enhanced with account_name
        
        Raises:
            AuctionSalesException on row not found or multiple rows found
        """
        rows = self._db.execute_d(
            """
                SELECT auction_sales.*, accounts.company AS account_name FROM auction_sales
                    LEFT JOIN accounts ON accounts.id=auction_sales.account
                    WHERE auction_sales.id=%(auction_sale_id)s
            """,
            {
                "auction_sale_id": auction_sale_id
            }
        )
        if len(rows) != 1:
            raise AuctionSalesException("Didn't find a single record matching ID")
        return rows[0]

    def new_auction_sale(self, name, at, account_id, comments, published):
        """Creates a new auction sale.

        Params:
            name: The name of the auction sale
            at: The unix time when the sale occurs
            account_id: The account owning the auction sale
            comments: The comments available on the auction sale
            published: Whether the sale is published or not
        """
        self._db.execute("""
            INSERT INTO auction_sales (name, at, account, comments, published)
                VALUES (%(name)s, %(at)s, %(account)s, %(comments)s, %(published)s)
            """,
            {
                "name": name,
                "at": at,
                "account": account_id,
                "comments": comments,
                "published": published
            }
        )
    
    def update_auction_sale(self, auction_sale_id, name, at, comments, published):
        """Updates an auction sale.

        Params:
            auction_sale_id: The ID of the auction sale
            name: The name of the sale (to update)
            at: The unix time of when the sale occurs (to update)
            comments: Comments on the sale (to update)
            published: Whether the sale is published (to update)
        """
        self._db.execute("""
            UPDATE auction_sales
                SET name=%(name)s, at=%(at)s, comments=%(comments)s,
                    published=%(published)s
                WHERE id=%(auction_sale_id)s
            """,
            {
                "name": name,
                "at": at,
                "comments": comments,
                "published": published,
                "auction_sale_id": auction_sale_id
            }
        )

    def get_auction_sales_by_account(self, account_id):
        """Gets auction sales by account ID.

        Gets ALL of them, including unpublished.

        Params:
            account_id: The ID of the account to get auction sales for.
        
        Returns:
            A (possibly empty) list of rows
        """
        return self._db.execute_d(
            """
                SELECT * FROM auction_sales
                    WHERE auction_sales.account=%(account_id)s
            """,
            {
                "account_id": account_id
            }
        )
    
    def search_auction_sales(self, name):
        """Gets published only auction sales similar to name or account name ordered by
            applicability. Only 10 returned.
        
        Params:
            name: A name to search
        
        Returns:
            A (possibly empty) list of rows)

            Enhanced with account_name
        """
        return self._db.execute_d(
            """
                SELECT auction_sales.*, accounts.company AS account_name FROM auction_sales
                    LEFT JOIN accounts ON accounts.id=auction_sales.account
                    WHERE
                        auction_sales.published > 0 AND
                        (
                            auction_sales.name LIKE CONCAT('%', %(name)s, '%') OR
                            accounts.company LIKE CONCAT('%', %(name)s, '%')
                        )
                    ORDER BY auction_sales.id DESC
                    LIMIT 10
            """,
            {
                "name": name
            }
        )
