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

    def insert_advertisement(self, ad_company_name=None, ad_company_email=None, ad_company_contact_name=None, ad_company_address=None, ad_company_city=None,
                             ad_company_state=None, ad_account_zip_code=None, ad_company_phone=None, ad_category=None, ad_account_integrated_with_btn=None,
                             company_logo_file_id=None, short_description=None, long_description=None, is_archived=None):
        """
        Inserts an advertisement

        Params:
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_account_zip_code: Zip code of company
            ad_category: Category of advertisement
            ad_account_integrated_with_btn: Flag indicating if account is integrated with BlockTrust Network
            company_logo_file_id: File ID of uploaded company logo file
            short_description: Subheader for the ad
            long_description: Long description for the ad
            is_archived: Indicates if the ad is archived
        """
        self._db.execute(
            """
            INSERT INTO advertisements (ad_company_name, ad_company_email, ad_company_contact_name, ad_company_address, ad_company_city,
            ad_company_state, ad_account_zip_code, ad_company_phone, ad_category, ad_account_intergrated_with_btn, company_logo_file_id,
            short_description, long_description, is_archived)
            VALUES (%(ad_company_name)s, %(ad_company_email)s, %(ad_company_contact_name)s, %(ad_company_address)s, %(ad_company_city)s,%(ad_company_state)s,
            %(ad_account_zip_code)s, %(ad_company_phone)s, %(ad_category)s, %(ad_account_integrated_with_btn)s, %(company_logo_file_id)s, %(short_description)s,
            %(long_description)s, %(is_archived)s)
            """, 
            {
                "ad_company_name": ad_company_name,
                "ad_company_email": ad_company_email,
                "ad_company_contact_name": ad_company_contact_name,
                "ad_company_address": ad_company_address,
                "ad_company_city": ad_company_city,
                "ad_company_state": ad_company_state,
                "ad_account_zip_code": ad_account_zip_code,
                "ad_company_phone": ad_company_phone,
                "ad_category": ad_category,
                "ad_account_integrated_with_btn": ad_account_integrated_with_btn,
                "company_logo_file_id": company_logo_file_id,
                "short_description": short_description,
                "long_description": long_description,
                "is_archived": is_archived
            })


    def get_advertisements(self, id=NO_VALUE, ad_company_name=NO_VALUE, ad_company_email=NO_VALUE, ad_company_contact_name=NO_VALUE,
                           ad_company_address=NO_VALUE, ad_company_city=NO_VALUE, ad_company_state=NO_VALUE, ad_account_zip_code=NO_VALUE, 
                           ad_company_phone=NO_VALUE, ad_category=NO_VALUE, ad_account_intergrated_with_btn=NO_VALUE, company_logo_file_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Gets the advertisements based on the attributes provided

        Params:
            id: ID of the advertisement
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_account_zip_code: Zip code of company
            ad_category: Category of advertisement
            ad_account_integrated_with_btn: Flag indicating if account is integrated with BlockTrust Network
            company_logo_file_id: File ID of uploaded company logo file
            is_archived: Indicates if the ad is archived

        Returns:
            A list of advertisement rows or an empty list
        """
        base_query = "SELECT * FROM advertisements"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if ad_company_name is not NO_VALUE:
            query_conditions.append(" ad_company_name = %(ad_company_name)s")
            query_values["ad_company_name"] = ad_company_name
        if ad_company_email is not NO_VALUE:
            query_conditions.append(" ad_company_email = %(ad_company_email)s")
            query_values["ad_company_email"] = ad_company_email
        if ad_company_contact_name is not NO_VALUE:
            query_conditions.append(" ad_company_contact_name = %(ad_company_contact_name)s")
            query_values["ad_company_contact_name"] = ad_company_contact_name
        if ad_company_address is not NO_VALUE:
            query_conditions.append(" ad_company_address = %(ad_company_address)s")
            query_values["ad_company_address"] = ad_company_address
        if ad_company_city is not NO_VALUE:
            query_conditions.append(" ad_company_city = %(ad_company_city)s")
            query_values["ad_company_city"] = ad_company_city
        if ad_company_state is not NO_VALUE:
            query_conditions.append(" ad_company_state = %(ad_company_state)s")
            query_values["ad_company_state"] = ad_company_state
        if ad_account_zip_code is not NO_VALUE:
            query_conditions.append(" ad_account_zip_code = %(ad_account_zip_code)s")
            query_values["ad_account_zip_code"] = ad_account_zip_code
        if ad_company_phone is not NO_VALUE:
            query_conditions.append(" ad_company_phone = %(ad_company_phone)s")
            query_values["ad_company_phone"] = ad_company_phone
        if ad_category is not NO_VALUE:
            query_conditions.append(" ad_category = %(ad_category)s")
            query_values["ad_category"] = ad_category
        if ad_account_intergrated_with_btn is not NO_VALUE:
            query_conditions.append(" ad_account_intergrated_with_btn = %(ad_account_intergrated_with_btn)s")
            query_values["ad_account_intergrated_with_btn"] = ad_account_intergrated_with_btn
        if company_logo_file_id is not NO_VALUE:
            query_conditions.append(" company_logo_file_id = %(company_logo_file_id)s")
            query_values["company_logo_file_id"] = company_logo_file_id
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition + " ORDER BY ID DESC"

        advertisement_rows = self._db.execute_d(query, query_values)
        if len(advertisement_rows) > 0:
            return advertisement_rows
        else:
            return []

    def update_advertisement(self, id, ad_company_name=NO_VALUE, ad_company_email=NO_VALUE, ad_company_contact_name=NO_VALUE,
                             ad_company_address=NO_VALUE, ad_company_city=NO_VALUE, ad_company_state=NO_VALUE, ad_account_zip_code=NO_VALUE, 
                             ad_company_phone=NO_VALUE, ad_category=NO_VALUE, ad_account_intergrated_with_btn=NO_VALUE, company_logo_file_id=NO_VALUE,
                             short_description=NO_VALUE, long_description=NO_VALUE, is_archived=NO_VALUE):
        """
        Updates the advertisement based on the ID provided

        Params:
            id: ID of the advertisement
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_account_zip_code: Zip code of company
            ad_category: Category of advertisement
            ad_account_integrated_with_btn: Flag indicating if account is integrated with BlockTrust Network
            company_logo_file_id: File ID of uploaded company logo file
            short_description: Subheader for the ad
            long_description: Long description for the ad
            is_archived: Indicates if the ad is archived
        """
        base_query = "UPDATE advertisements"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if ad_company_name is not NO_VALUE:
            query_conditions.append(" ad_company_name = %(ad_company_name)s")
            query_values["ad_company_name"] = ad_company_name
        if ad_company_email is not NO_VALUE:
            query_conditions.append(" ad_company_email = %(ad_company_email)s")
            query_values["ad_company_email"] = ad_company_email
        if ad_company_contact_name is not NO_VALUE:
            query_conditions.append(" ad_company_contact_name = %(ad_company_contact_name)s")
            query_values["ad_company_contact_name"] = ad_company_contact_name
        if ad_company_address is not NO_VALUE:
            query_conditions.append(" ad_company_address = %(ad_company_address)s")
            query_values["ad_company_address"] = ad_company_address
        if ad_company_city is not NO_VALUE:
            query_conditions.append(" ad_company_city = %(ad_company_city)s")
            query_values["ad_company_city"] = ad_company_city
        if ad_company_state is not NO_VALUE:
            query_conditions.append(" ad_company_state = %(ad_company_state)s")
            query_values["ad_company_state"] = ad_company_state
        if ad_account_zip_code is not NO_VALUE:
            query_conditions.append(" ad_account_zip_code = %(ad_account_zip_code)s")
            query_values["ad_account_zip_code"] = ad_account_zip_code
        if ad_company_phone is not NO_VALUE:
            query_conditions.append(" ad_company_phone = %(ad_company_phone)s")
            query_values["ad_company_phone"] = ad_company_phone
        if ad_category is not NO_VALUE:
            query_conditions.append(" ad_category = %(ad_category)s")
            query_values["ad_category"] = ad_category
        if ad_account_intergrated_with_btn is not NO_VALUE:
            query_conditions.append(" ad_account_intergrated_with_btn = %(ad_account_intergrated_with_btn)s")
            query_values["ad_account_intergrated_with_btn"] = ad_account_intergrated_with_btn
        if company_logo_file_id is not NO_VALUE:
            query_conditions.append(" company_logo_file_id = %(company_logo_file_id)s")
            query_values["company_logo_file_id"] = company_logo_file_id
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