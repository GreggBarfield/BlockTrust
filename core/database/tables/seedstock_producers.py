from ..no_value import NoValue
from ... import config
from ...utilities.aws import aws
from .files import MARKETPLACE_FILES_S3_PATH

NO_VALUE = NoValue()

seedstock_producers_cols = ("id", "account_id", "marketplace_account_name", "marketplace_account_email",
                            "marketplace_account_contact_name", "marketplace_account_phone", "short_description",
                            "long_description", "is_archived", "logo_file_id")

class SeedstockProducers:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, marketplace_account_name=None, marketplace_account_email=None,
               marketplace_account_contact_name=None, marketplace_account_phone=None,
               short_description=None, long_description=None, logo_file_id=None, website_url=None):
        """
        Inserts a new seedstock producer marketplace advertisement

        Params:
            account_id: Account ID of seedstock producer
            marketplace_account_name: Account naem to be displayed on Ad
            marketplace_account_email: EMail ID to be displayed on Ad
            short_description: Short description for Ad
            long_description: Long description for Ad
            is_archived: If ad is archived
            logo_file_id: Logo file ID
        """
        self._db.execute(
            """
            INSERT INTO seedstock_producers(account_id, marketplace_account_name, marketplace_account_email,
            marketplace_account_contact_name, marketplace_account_phone, short_description, long_description,
            logo_file_id, website_url)
            VALUES(%(account_id)s, %(marketplace_account_name)s, %(marketplace_account_email)s,
            %(marketplace_account_contact_name)s, %(marketplace_account_phone)s, %(short_description)s,
            %(long_description)s, %(logo_file_id)s, %(website_url)s)
            """,
            {
                "account_id": account_id,
                "marketplace_account_name": marketplace_account_name,
                "marketplace_account_email": marketplace_account_email,
                "marketplace_account_contact_name": marketplace_account_contact_name,
                "marketplace_account_phone": marketplace_account_phone,
                "short_description": short_description,
                "long_description": long_description,
                "logo_file_id": logo_file_id,
                "website_url": website_url
            }
        )

    def get(self, id=NO_VALUE, account_id=NO_VALUE, marketplace_account_name=NO_VALUE,
            marketplace_account_email=NO_VALUE, marketplace_account_contact_name=NO_VALUE,
            marketplace_account_phone=NO_VALUE, short_description=NO_VALUE, long_description=NO_VALUE,
            logo_file_id=NO_VALUE, is_archived=NO_VALUE, website_url=NO_VALUE, include_logo_url=False):
        """
        Gets the seedstock producer data based on attributes provided

        Params:
            id: ID of record
            account_id: Account ID of seedstock producer
            marketplace_account_name: Account naem to be displayed on Ad
            marketplace_account_email: EMail ID to be displayed on Ad
            short_description: Short description for Ad
            long_description: Long description for Ad
            is_archived: If ad is archived
            logo_file_id: Logo file ID

        Returns:
            Seedstock Producers rows based on attributes provided or an empty list
        """
        base_query = "SELECT * FROM seedstock_producers"

        query_conditions = []
        query_values = {}
        
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if marketplace_account_name is not NO_VALUE:
            query_conditions.append("marketplace_account_name = %(marketplace_account_name)s")
            query_values["marketplace_account_name"] = marketplace_account_name
        if marketplace_account_email is not NO_VALUE:
            query_conditions.append("marketplace_account_email = %(marketplace_account_email)s")
            query_values["marketplace_account_email"] = marketplace_account_email
        if marketplace_account_contact_name is not NO_VALUE:
            query_conditions.append("marketplace_account_contact_name = %(marketplace_account_contact_name)s")
            query_values["marketplace_account_contact_name"] = marketplace_account_contact_name
        if marketplace_account_phone is not NO_VALUE:
            query_conditions.append("marketplace_account_phone = %(marketplace_account_phone)s")
            query_values["marketplace_account_phone"] = marketplace_account_phone
        if short_description is not NO_VALUE:
            query_conditions.append("short_description = %(short_description)s")
            query_values["short_description"] = short_description
        if long_description is not NO_VALUE:
            query_conditions.append("long_description = %(long_description)s")
            query_values["long_description"] = long_description
        if logo_file_id is not NO_VALUE:
            query_conditions.append("logo_file_id = %(logo_file_id)s")
            query_values["logo_file_id"] = logo_file_id
        if is_archived is not NO_VALUE:
            query_conditions.append("is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if website_url is not NO_VALUE:
            query_conditions.append("website_url = %(website_url)s")
            query_values["website_url"] = website_url
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        rows = self._db.execute_d(query, query_values)
        if len(rows) > 0:
            if include_logo_url is True:
                for row in rows:
                    if row["logo_file_id"] is not None:
                        row["logo_url"] = aws.get_s3_client().generate_presigned_url(
                            ClientMethod="get_object", 
                            Params={
                                "Bucket": config.AWS_S3_BUCKET, 
                                "Key": MARKETPLACE_FILES_S3_PATH + str(row["logo_file_id"])
                            }
                        )
                    else:
                        row["logo_url"] = None
        return rows

    def update(self, id, account_id=NO_VALUE, marketplace_account_name=NO_VALUE, marketplace_account_email=NO_VALUE,
               marketplace_account_contact_name=NO_VALUE, marketplace_account_phone=NO_VALUE,
               short_description=NO_VALUE, long_description=NO_VALUE, logo_file_id=NO_VALUE, is_archived=NO_VALUE,
               website_url=NO_VALUE):
        """
        Updates the seedstock producer data based on attributes provided

        Params:
            id: ID of record
            account_id: Account ID of seedstock producer
            marketplace_account_name: Account naem to be displayed on Ad
            marketplace_account_email: EMail ID to be displayed on Ad
            short_description: Short description for Ad
            long_description: Long description for Ad
            is_archived: If ad is archived
            logo_file_id: Logo file ID
        """
        base_query = "UPDATE seedstock_producers"

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if marketplace_account_name is not NO_VALUE:
            query_conditions.append("marketplace_account_name = %(marketplace_account_name)s")
            query_values["marketplace_account_name"] = marketplace_account_name
        if marketplace_account_email is not NO_VALUE:
            query_conditions.append("marketplace_account_email = %(marketplace_account_email)s")
            query_values["marketplace_account_email"] = marketplace_account_email
        if marketplace_account_contact_name is not NO_VALUE:
            query_conditions.append("marketplace_account_contact_name = %(marketplace_account_contact_name)s")
            query_values["marketplace_account_contact_name"] = marketplace_account_contact_name
        if marketplace_account_phone is not NO_VALUE:
            query_conditions.append("marketplace_account_phone = %(marketplace_account_phone)s")
            query_values["marketplace_account_phone"] = marketplace_account_phone
        if short_description is not NO_VALUE:
            query_conditions.append("short_description = %(short_description)s")
            query_values["short_description"] = short_description
        if long_description is not NO_VALUE:
            query_conditions.append("long_description = %(long_description)s")
            query_values["long_description"] = long_description
        if logo_file_id is not NO_VALUE:
            query_conditions.append("logo_file_id = %(logo_file_id)s")
            query_values["logo_file_id"] = logo_file_id
        if is_archived is not NO_VALUE:
            query_conditions.append("is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        if website_url is not NO_VALUE:
            query_conditions.append("website_url = %(website_url)s")
            query_values["website_url"] = website_url
        
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update!")