from ..no_value import NoValue

NO_VALUE = NoValue()

ADVERTISEMENT_CATEGORIES_NAME_TO_ID = {
    "Genetics": 0,
    "Feed": 1
}
ADVERTISEMENT_CATEGORIES_ID_TO_NAME = {
    value: key for key, value in ADVERTISEMENT_CATEGORIES_NAME_TO_ID.items()
}

class Advertisements:

    def __init__(self, db):
        self._db = db

    def get_advertisements(self, id=NO_VALUE, ad_account_name=NO_VALUE, ad_account_email=NO_VALUE, ad_account_contact_name=NO_VALUE,
                           ad_account_address=NO_VALUE, ad_account_city=NO_VALUE, ad_account_state=NO_VALUE, ad_account_zip_code=NO_VALUE, 
                           ad_account_phone=NO_VALUE, ad_category=NO_VALUE, ad_account_intergrated_with_btn=NO_VALUE, company_logo_file_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Gets the advertisements based on the attributes provided

        Params:
            id: ID of the advertisement
            ad_account_name: Name of the account posting the advertisement
            ad_account_email: Email of the account posting the advertisement
            ad_account_contact_name: Contact Name of the account posting the advertisement
            ad_account_phone: Phone number of the account posting the advertisement
            ad_account_address: Street address of account
            ad_account_city: City of account
            ad_account_state: State of account
            ad_account_zip_code: Zip code of account
            ad_category: Category of advertisement
            ad_account_integrated_with_btn: Flag indicating if account is integrated with BlockTrust Network
            company_logo_file_id: File ID of uploaded company logo file
        """
        base_query = "SELECT * FROM advertisements"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if ad_account_name is not NO_VALUE:
            query_conditions.append(" ad_account_name = %(ad_account_name)s")
            query_values["ad_account_name"] = ad_account_name
        if ad_account_email is not NO_VALUE:
            query_conditions.append(" ad_account_email = %(ad_account_email)s")
            query_values["ad_account_email"] = ad_account_email
        if ad_account_contact_name is not NO_VALUE:
            query_conditions.append(" ad_account_contact_name = %(ad_account_contact_name)s")
            query_values["ad_account_contact_name"] = ad_account_contact_name
        if ad_account_address is not NO_VALUE:
            query_conditions.append(" ad_account_address = %(ad_account_address)s")
            query_values["ad_account_address"] = ad_account_address
        if ad_account_city is not NO_VALUE:
            query_conditions.append(" ad_account_city = %(ad_account_city)s")
            query_values["ad_account_city"] = ad_account_city
        if ad_account_state is not NO_VALUE:
            query_conditions.append(" ad_account_state = %(ad_account_state)s")
            query_values["ad_account_state"] = ad_account_state
        if ad_account_zip_code is not NO_VALUE:
            query_conditions.append(" ad_account_zip_code = %(ad_account_zip_code)s")
            query_values["ad_account_zip_code"] = ad_account_zip_code
        if ad_account_phone is not NO_VALUE:
            query_conditions.append(" ad_account_phone = %(ad_account_phone)s")
            query_values["ad_account_phone"] = ad_account_phone
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

    def update_advertisement(self, id, ad_account_name=NO_VALUE, ad_account_email=NO_VALUE, ad_account_contact_name=NO_VALUE,
                             ad_account_address=NO_VALUE, ad_account_city=NO_VALUE, ad_account_state=NO_VALUE, ad_account_zip_code=NO_VALUE, 
                             ad_account_phone=NO_VALUE, ad_category=NO_VALUE, ad_account_intergrated_with_btn=NO_VALUE, company_logo_file_id=NO_VALUE,
                             short_description=NO_VALUE, long_description=NO_VALUE, is_archived=NO_VALUE):
        """
        Uppdates the advertisement based on the ID provided

        Params:
            id: ID of the advertisement
            ad_account_name: Name of the account posting the advertisement
            ad_account_email: Email of the account posting the advertisement
            ad_account_contact_name: Contact Name of the account posting the advertisement
            ad_account_phone: Phone number of the account posting the advertisement
            ad_account_address: Street address of account
            ad_account_city: City of account
            ad_account_state: State of account
            ad_account_zip_code: Zip code of account
            ad_category: Category of advertisement
            ad_account_integrated_with_btn: Flag indicating if account is integrated with BlockTrust Network
            company_logo_file_id: File ID of uploaded company logo file
            short_description: Subheader for the ad
            long_description: Long description for the ad
        """
        base_query = "UPDATE advertisements"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if ad_account_name is not NO_VALUE:
            query_conditions.append(" ad_account_name = %(ad_account_name)s")
            query_values["ad_account_name"] = ad_account_name
        if ad_account_email is not NO_VALUE:
            query_conditions.append(" ad_account_email = %(ad_account_email)s")
            query_values["ad_account_email"] = ad_account_email
        if ad_account_contact_name is not NO_VALUE:
            query_conditions.append(" ad_account_contact_name = %(ad_account_contact_name)s")
            query_values["ad_account_contact_name"] = ad_account_contact_name
        if ad_account_address is not NO_VALUE:
            query_conditions.append(" ad_account_address = %(ad_account_address)s")
            query_values["ad_account_address"] = ad_account_address
        if ad_account_city is not NO_VALUE:
            query_conditions.append(" ad_account_city = %(ad_account_city)s")
            query_values["ad_account_city"] = ad_account_city
        if ad_account_state is not NO_VALUE:
            query_conditions.append(" ad_account_state = %(ad_account_state)s")
            query_values["ad_account_state"] = ad_account_state
        if ad_account_zip_code is not NO_VALUE:
            query_conditions.append(" ad_account_zip_code = %(ad_account_zip_code)s")
            query_values["ad_account_zip_code"] = ad_account_zip_code
        if ad_account_phone is not NO_VALUE:
            query_conditions.append(" ad_account_phone = %(ad_account_phone)s")
            query_values["ad_account_phone"] = ad_account_phone
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