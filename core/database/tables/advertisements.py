from ..no_value import NoValue

NO_VALUE = NoValue()

ADVERTISEMENT_CATEGORY_NAMES_TO_IDS = {
    "Genetics": 0,
    "Feed": 1
}
ADVERTISEMENT_CATEGORY_IDS_TO_NAMES = {
    value: key for key, value in ADVERTISEMENT_CATEGORY_NAMES_TO_IDS.items()
}

class Advertisements:

    def __init__(self, db):
        self._db = db

    def insert(self, ad_company_id=None, ad_category_id=None, short_description=None, long_description=None, is_archived=None):
        """
        Inserts an advertisement

        Params:
            ad_company_id: Name of the company posting the advertisement
            ad_category_id: Category of advertisement
            short_description: Subheader for the ad
            long_description: Long description for the ad
            is_archived: Indicates if the ad is archived
        """
        self._db.execute(
            """
            INSERT INTO advertisements (ad_company_id, ad_category_id, short_description, long_description, is_archived)
            VALUES (%(ad_company_id)s, %(ad_category_id)s, %(short_description)s, %(long_description)s, %(is_archived)s)
            """, 
            {
                "ad_company_id": ad_company_id,
                "ad_category_id": ad_category_id,
                "short_description": short_description,
                "long_description": long_description,
                "is_archived": is_archived
            })


    def get(self, id=NO_VALUE, ad_company_id=NO_VALUE, ad_category_id=NO_VALUE, is_archived=NO_VALUE, get_related_advertising_company=False):
        """
        Gets the advertisements based on the attributes provided

        Params:
            id: ID of the advertisement
            ad_company_id: Name of the company posting the advertisement
            company_logo_file_id: File ID of uploaded company logo file
            is_archived: Indicates if the ad is archived

        Returns:
            A list of advertisement rows or an empty list
        """
        base_query = "SELECT * FROM advertisements"
        if get_related_advertising_company :
            base_query = base_query + " LEFT JOIN advertisement_companies ON advertisements.ad_company_id = advertisement_companies.id "

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if ad_company_id is not NO_VALUE:
            query_conditions.append(" ad_company_id = %(ad_company_id)s")
            query_values["ad_company_id"] = ad_company_id
        if ad_category_id is not NO_VALUE:
            query_conditions.append(" ad_category_id = %(ad_category_id)s")
            query_values["ad_category_id"] = ad_category_id
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        advertisement_rows = self._db.execute_d(query, query_values)
        if len(advertisement_rows) > 0:
            return advertisement_rows
        else:
            return []

    def update(self, id, ad_company_id=NO_VALUE, ad_category_id=NO_VALUE, short_description=NO_VALUE, long_description=NO_VALUE, is_archived=NO_VALUE):
        """
        Updates the advertisement based on the ID provided

        Params:
            id: ID of the advertisement
            ad_company_id: Name of the company posting the advertisement
            ad_category_id: Category of advertisement
            short_description: Subheader for the ad
            long_description: Long description for the ad
            is_archived: Indicates if the ad is archived
        """
        base_query = "UPDATE advertisements"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if ad_company_id is not NO_VALUE:
            query_conditions.append(" ad_company_id = %(ad_company_id)s")
            query_values["ad_company_id"] = ad_company_id
        if ad_category_id is not NO_VALUE:
            query_conditions.append(" ad_category_id = %(ad_category_id)s")
            query_values["ad_category_id"] = ad_category_id
        if short_description is not NO_VALUE:
            query_conditions.append(" short_description = %(short_description)s")
            query_values["short_description"] = short_description
        if long_description is not NO_VALUE:
            query_conditions.append(" long_description = %(long_description)s")
            query_values["long_description"] = long_description
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Advertisements")