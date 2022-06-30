from ..objects.product import Product
from ..no_value import NoValue
from ... import config
from ...utilities.aws import aws

NO_VALUE = NoValue()

class ProductTableException(Exception):
    """Generic Product exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for ProductException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class NoProductFoundException(ProductTableException):
    """Product was not found."""
    pass


class ProductTable:

    def __init__(self, db):
        self._db = db

    def get_products(self, id=NO_VALUE, product=NO_VALUE, pic_1=NO_VALUE, pic_2=NO_VALUE, price=NO_VALUE, post=NO_VALUE,
                     subheader=NO_VALUE, details=NO_VALUE, unit=NO_VALUE, partner=NO_VALUE,
                     is_premise_id_required=NO_VALUE, product_type=NO_VALUE, include_images=False):
        """
        Gets the product based on the attributes provided

        Params:
            id: Product ID
            product: Product name
            pic_1: Thumbnail Image
            pic_2: Description Image
            price: Product price
            post: Product is posted or not
            subheader: Description subheader
            details: Product details
            unit: Product units
            partner: Partner the product is related to
            is_premise_id_required: Indicates if premise ID is required for a product
            product_type: Product category

        Returns:
            A list of products or an empty list
        """
        # base query
        base_query = "SELECT * FROM products"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if product is not NO_VALUE:
            query_conditions.append("product = %(product)s")
            query_values["product"] = product
        if pic_1 is not NO_VALUE:
            query_conditions.append("pic_1 = %(pic_1)s")
            query_values["pic_1"] = pic_1
        if pic_2 is not NO_VALUE:
            query_conditions.append("pic_2 = %(pic_2)s")
            query_values["pic_2"] = pic_2
        if price is not NO_VALUE:
            query_conditions.append("price = %(price)s")
            query_values["price"] = price
        if post is not NO_VALUE:
            query_conditions.append("post = %(post)s")
            query_values["post"] = post
        if subheader is not NO_VALUE:
            query_conditions.append("subheader = %(subheader)s")
            query_values["subheader"] = subheader
        if details is not NO_VALUE:
            query_conditions.append("details = %(details)s")
            query_values["details"] = details
        if unit is not NO_VALUE:
            query_conditions.append("unit = %(unit)s")
            query_values["unit"] = unit
        if partner is not NO_VALUE:
            query_conditions.append("partner = %(partner)s")
            query_values["partner"] = partner
        if is_premise_id_required is not NO_VALUE:
            query_conditions.append("is_premise_id_required = %(is_premise_id_required)s")
            query_values["is_premise_id_required"] = is_premise_id_required
        if product_type is not NO_VALUE:
            query_conditions.append("product_type = %(product_type)s")
            query_values["product_type"] = product_type

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        product_rows = self._db.execute_d(query, query_values)
        if len(product_rows) > 0:
            if include_images is True:
                for product_row in product_rows:
                    product_row["pic_1_url"] = aws.get_s3_client().generate_presigned_url(
                        ClientMethod="get_object", Params={"Bucket": config.AWS_S3_BUCKET, "Key": "products/" + product_row["pic_1"]}
                    )
                    product_row["pic_2_url"] = aws.get_s3_client().generate_presigned_url(
                        ClientMethod="get_object", Params={"Bucket": config.AWS_S3_BUCKET, "Key": "products/" + product_row["pic_2"]}
                    )
            return product_rows
        else:
            return []
