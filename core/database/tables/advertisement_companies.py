from ..no_value import NoValue

NO_VALUE = NoValue()


class Advertisements:

    def __init__(self, db):
        self._db = db

    def insert_advertisement_company(self, ad_company_name=None, ad_company_email=None, ad_company_contact_name=None,
                                       ad_company_address=None, ad_company_city=None, ad_company_state=None, ad_account_zip_code=None,
                                       ad_company_phone=None, ad_company_integrated_with_blocktrust=None, ad_company_logo_file_id=None):
        """
        Inserts an advertisement company

        Params:
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_company_zip_code: Zip code of company
            ad_company_integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            ad_company_logo_file_id: File ID of uploaded company logo file
        """
        self._db.execute(
            """
            INSERT INTO advertisements (ad_company_name, ad_company_email, ad_company_contact_name, ad_company_address, ad_company_city,
            ad_company_state, ad_account_zip_code, ad_company_phone, ad_company_integrated_with_blocktrust, ad_company_logo_file_id)
            VALUES (%(ad_company_name)s, %(ad_company_email)s, %(ad_company_contact_name)s, %(ad_company_address)s, %(ad_company_city)s,%(ad_company_state)s,
            %(ad_account_zip_code)s, %(ad_company_phone)s, %(ad_company_integrated_with_blocktrust)s, %(ad_company_logo_file_id)s)
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
                "ad_company_integrated_with_blocktrust": ad_company_integrated_with_blocktrust,
                "ad_company_logo_file_id": ad_company_logo_file_id
            })

    def get_advertisement_company(self, id=NO_VALUE, ad_company_name=NO_VALUE, ad_company_email=NO_VALUE, ad_company_contact_name=NO_VALUE,
                                  ad_company_address=NO_VALUE, ad_company_city=NO_VALUE, ad_company_state=NO_VALUE, ad_company_zip_code=NO_VALUE, 
                                  ad_company_phone=NO_VALUE, ad_company_integrated_with_blocktrust=NO_VALUE, ad_company_logo_file_id=NO_VALUE):
        """
        Gets the advertisement company based on the attributes provided

        Params:
            id: Id of the advertisement comapny
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_company_zip_code: Zip code of company
            ad_company_integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            ad_company_logo_file_id: File ID of uploaded company logo file

            Returns:
            A list of advertisement companies or an empty list
        """
        base_query = "SELECT * FROM advertisement_companies"

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
        if ad_company_zip_code is not NO_VALUE:
            query_conditions.append(" ad_company_zip_code = %(ad_company_zip_code)s")
            query_values["ad_company_zip_code"] = ad_company_zip_code
        if ad_company_phone is not NO_VALUE:
            query_conditions.append(" ad_company_phone = %(ad_company_phone)s")
            query_values["ad_company_phone"] = ad_company_phone
        if ad_company_integrated_with_blocktrust is not NO_VALUE:
            query_conditions.append(" ad_company_integrated_with_blocktrust = %(ad_company_integrated_with_blocktrust)s")
            query_values["ad_company_integrated_with_blocktrust"] = ad_company_integrated_with_blocktrust
        if ad_company_logo_file_id is not NO_VALUE:
            query_conditions.append(" ad_company_logo_file_id = %(ad_company_logo_file_id)s")
            query_values["ad_company_logo_file_id"] = ad_company_logo_file_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition + " ORDER BY ID DESC"

        advertisement_company_rows = self._db.execute_d(query, query_values)
        if len(advertisement_company_rows) > 0:
            return advertisement_company_rows
        else:
            return []

    def update_advertisement_company(self, id, ad_company_name=NO_VALUE, ad_company_email=NO_VALUE, ad_company_contact_name=NO_VALUE,
                                     ad_company_address=NO_VALUE, ad_company_city=NO_VALUE, ad_company_state=NO_VALUE, ad_company_zip_code=NO_VALUE, 
                                     ad_company_phone=NO_VALUE, ad_company_integrated_with_blocktrust=NO_VALUE, ad_company_logo_file_id=NO_VALUE):
        """
        Updates the advertisement company based on the ID provided

        Params:
            id: Id of the advertisement comapny
            ad_company_name: Name of the company posting the advertisement
            ad_company_email: Email of the company posting the advertisement
            ad_company_contact_name: Contact Name of the company posting the advertisement
            ad_company_phone: Phone number of the company posting the advertisement
            ad_company_address: Street address of company
            ad_company_city: City of company
            ad_company_state: State of company
            ad_company_zip_code: Zip code of company
            ad_company_integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            ad_company_logo_file_id: File ID of uploaded company logo file
        """
        base_query = "UPDATE advertisement_company"

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
        if ad_company_zip_code is not NO_VALUE:
            query_conditions.append(" ad_company_zip_code = %(ad_company_zip_code)s")
            query_values["ad_company_zip_code"] = ad_company_zip_code
        if ad_company_phone is not NO_VALUE:
            query_conditions.append(" ad_company_phone = %(ad_company_phone)s")
            query_values["ad_company_phone"] = ad_company_phone
        if ad_company_integrated_with_blocktrust is not NO_VALUE:
            query_conditions.append(" ad_company_integrated_with_blocktrust = %(ad_company_integrated_with_blocktrust)s")
            query_values["ad_company_integrated_with_blocktrust"] = ad_company_integrated_with_blocktrust
        if ad_company_logo_file_id is not NO_VALUE:
            query_conditions.append(" ad_company_logo_file_id = %(ad_company_logo_file_id)s")
            query_values["ad_company_logo_file_id"] = ad_company_logo_file_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Advertisement Company")