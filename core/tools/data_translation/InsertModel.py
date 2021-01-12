import json
class InsertModel:
    """ InsertModel is a class designed to make
        working with insert table records easier on the backend
        side of the application. 

        The class can be used to prepare data for later processing.
        The class can be loaded with row data provided 
        in the form of a list.

        Additionally, functions exist to make accessing embedded
        json data much simpler than doing so by hand.

    """
    def __init__(self):
        """ Constructor: Does little except 
            prepare instance variables for later use.

            Params: NONE
        """
        self.num_cols = 7

        self.id = None
        self.account = None
        self.namespace = None
        self.type = None
        self.fields = None
        self.row = None
        self.created = None


    def load_from_list(self, insert_list):
        """ load_from_list is a function
            than can be used to to populate the
            insert object with data after it has been previously
            initialized.

            Params: 
                insert_list: A python list corresponding with  a row's data
                    from the inserts table.

            Returns:
                True: Indicating the data was successfully loaded
                False: Indicated the data was not successfully loaded

        """
        # This assumes that all values are given in order of DB
        if (len(insert_list) == self.num_cols):
            self.id = str(insert_list[0])
            self.account = str(insert_list[1])
            self.namespace = str(insert_list[2])
            self.type = str(insert_list[3])
            self.fields = str(insert_list[4])
            self.fields = json.loads(self.fields)
            self.row = str(insert_list[5])
            self.row = json.loads(self.row)
            self.created = str(insert_list[6])

            return True
        else:
            return False

    def load_from_dict(self, insert_dict):
        """ load_from_dict populates the insert data from a dictionary.

            Params:
                insert_dict: a dictionary corresponding to the field names and values
                             for a row of inserts table data.

            Returns:
                nothing
        """
        insert_dict = dict(insert_dict)

        self.id = None
        self.account = None
        self.namespace = None
        self.type = None
        self.fields = None
        self.row = None
        self.created = None

        if 'id' in insert_dict.keys():
            self.id = str(insert_dict['id'])

        if 'account' in insert_dict.keys():
            self.account = str(insert_dict['account'])

        if 'namespace' in insert_dict.keys():
            self.namespace = str(insert_dict['namespace'])
        
        if 'type' in insert_dict.keys():
            self.type = str(insert_dict['type'])

        if 'fields' in insert_dict.keys():
            self.fields = str(insert_dict['fields'])
            self.fields = json.loads(self.fields)

        if 'row' in insert_dict.keys():
            self.row = str(insert_dict['row'])
            self.row = json.loads(self.row)

        if 'created' in insert_dict.keys():
            self.created = str(insert_dict['created'])


    def to_list(self):
        """ to_list is a function meant to export the insert object as a list.

            Params: None

            Returns:
                a list containing the insert's data. In order
                of field names specified by the MySQL table schema.
        """
        output_list = []

        output_list.append(self.id)
        output_list.append(self.account)
        output_list.append(self.namespace)
        output_list.append(self.type)
        output_list.append(self.fields)
        output_list.append(self.row)
        output_list.append(self.created)

        return output_list

    def to_dict(self):
        """ to_dict is a function meant to export the insert
            object in the form of a dictionary with corresponding values.

            Params: None

            returns: a dictionary holding the insert objects values
        """
        output_dict = {}

        output_dict['id'] = self.id
        output_dict['account'] = self.account
        output_dict['namespace'] = self.namespace
        output_dict['type'] = self.type
        output_dict['fields'] = self.fields
        output_dict['row'] = self.row
        output_dict['created'] = self.created

        return output_dict 

    def to_json(self):
        """
            to_json exports the insert object as a json string

            Params: None

            Returns: json string with insert object data
        """

        output_json = json.dumps(self.to_dict())
        return output_json

    def get_data_dict(self):
        """ get_data_dict returns a dictionary version of the
            embedded json fiels (fields and row). This function makes
            extracting data from the embedded json string much easier.

            Params: None

            Returns:
                data_dict: a python dictionary holding the fields and corresponding row
                data for the insert object

                or

                None: indicating a failure
        """
        data_dict = {}
        if (len(self.fields) == len(self.row) or len(self.fields) < len(self.row)):
            for i in range(0, len(self.fields)):
                data_dict[self.fields[i]] = self.row[i]
            return dict(data_dict)
        elif len(self.fields) > len(self.row):
            for i in range(0, len(self.row)):
                data_dict[self.fields[i]] = self.row[i]
            return dict(data_dict)
        else:
            return None

    def shrink_data(self):
        """ 
            shrink_data is a utility function meant to
            remove fields and row data if the corresponding
            row data item is None or an empty string.

            This removes extra fields given to the developer by
            companies utilizing the api.

            Params: None

            Returns:
                True: If shrink was successful
                False: If shrink was unsuccessful
        """
        # Goal is to remove empty fields in the fields/row data
        try: 
            data_dict = self.get_data_dict()
            shrunk_data_dict = {}
            for k in list(data_dict.keys()):
                if not (k == '' or k == None):
                    if not (data_dict[k] == '' or data_dict[k] == None):
                        shrunk_data_dict[k] = data_dict[k]

            self.fields = list(shrunk_data_dict.keys())
            self.row = list(shrunk_data_dict.values())
            return True
        except Exception as e:
            print(e)
            return False




