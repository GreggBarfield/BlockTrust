from ..no_value import NoValue

NO_VALUE = NoValue()


class AdvertisementCompanies:

    def __init__(self, db):
        self._db = db

    def insert(self, name=None, email=None, contact_name=None, address=None, city=None, state=None, zip_code=None,
               phone=None, integrated_with_blocktrust=None, logo_file_id=None):
        """
        Inserts an advertisement company

        Params:
            name: Name of the company posting the advertisement
            email: Email of the company posting the advertisement
            contact_name: Contact Name of the company posting the advertisement
            phone: Phone number of the company posting the advertisement
            address: Street address of company
            city: City of company
            state: State of company
            zip_code: Zip code of company
            integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            logo_file_id: File ID of uploaded company logo file
        """
        self._db.execute(
            """
            INSERT INTO advertisement_companies (name, email, contact_name, address, city,
            state, zip_code, phone, integrated_with_blocktrust, logo_file_id)
            VALUES (%(name)s, %(email)s, %(contact_name)s, %(address)s, %(city)s,%(state)s,
            %(zip_code)s, %(phone)s, %(integrated_with_blocktrust)s, %(logo_file_id)s)
            """, 
            {
                "name": name,
                "email": email,
                "contact_name": contact_name,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "phone": phone,
                "integrated_with_blocktrust": integrated_with_blocktrust,
                "logo_file_id": logo_file_id
            })

    def get(self, id=NO_VALUE, name=NO_VALUE, email=NO_VALUE, contact_name=NO_VALUE, address=NO_VALUE, city=NO_VALUE,
            state=NO_VALUE, zip_code=NO_VALUE, phone=NO_VALUE, integrated_with_blocktrust=NO_VALUE, logo_file_id=NO_VALUE):
        """
        Gets the advertisement company based on the attributes provided

        Params:
            id: Id of the advertisement comapny
            name: Name of the company posting the advertisement
            email: Email of the company posting the advertisement
            contact_name: Contact Name of the company posting the advertisement
            phone: Phone number of the company posting the advertisement
            address: Street address of company
            city: City of company
            state: State of company
            zip_code: Zip code of company
            integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            logo_file_id: File ID of uploaded company logo file

            Returns:
            A list of advertisement companies or an empty list
        """
        base_query = "SELECT * FROM advertisement_companies"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if name is not NO_VALUE:
            query_conditions.append(" name = %(name)s")
            query_values["name"] = name
        if email is not NO_VALUE:
            query_conditions.append(" email = %(email)s")
            query_values["email"] = email
        if contact_name is not NO_VALUE:
            query_conditions.append(" contact_name = %(contact_name)s")
            query_values["contact_name"] = contact_name
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
        if phone is not NO_VALUE:
            query_conditions.append(" phone = %(phone)s")
            query_values["phone"] = phone
        if integrated_with_blocktrust is not NO_VALUE:
            query_conditions.append(" integrated_with_blocktrust = %(integrated_with_blocktrust)s")
            query_values["integrated_with_blocktrust"] = integrated_with_blocktrust
        if logo_file_id is not NO_VALUE:
            query_conditions.append(" logo_file_id = %(logo_file_id)s")
            query_values["logo_file_id"] = logo_file_id

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

    def update(self, id, name=NO_VALUE, email=NO_VALUE, contact_name=NO_VALUE, address=NO_VALUE, city=NO_VALUE,
               state=NO_VALUE, zip_code=NO_VALUE, phone=NO_VALUE, integrated_with_blocktrust=NO_VALUE, logo_file_id=NO_VALUE):
        """
        Updates the advertisement company based on the ID provided

        Params:
            id: Id of the advertisement comapny
            name: Name of the company posting the advertisement
            email: Email of the company posting the advertisement
            contact_name: Contact Name of the company posting the advertisement
            phone: Phone number of the company posting the advertisement
            address: Street address of company
            city: City of company
            state: State of company
            zip_code: Zip code of company
            integrated_with_blocktrust: Flag indicating if account is integrated with BlockTrust Network
            logo_file_id: File ID of uploaded company logo file
        """
        base_query = "UPDATE advertisement_companies"

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        
        if name is not NO_VALUE:
            query_conditions.append(" name = %(name)s")
            query_values["name"] = name
        if email is not NO_VALUE:
            query_conditions.append(" email = %(email)s")
            query_values["email"] = email
        if contact_name is not NO_VALUE:
            query_conditions.append(" contact_name = %(contact_name)s")
            query_values["contact_name"] = contact_name
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
        if phone is not NO_VALUE:
            query_conditions.append(" phone = %(phone)s")
            query_values["phone"] = phone
        if integrated_with_blocktrust is not NO_VALUE:
            query_conditions.append(" integrated_with_blocktrust = %(integrated_with_blocktrust)s")
            query_values["integrated_with_blocktrust"] = integrated_with_blocktrust
        if logo_file_id is not NO_VALUE:
            query_conditions.append(" logo_file_id = %(logo_file_id)s")
            query_values["logo_file_id"] = logo_file_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Advertisement Company")