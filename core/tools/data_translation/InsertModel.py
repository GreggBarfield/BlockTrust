import json
class InsertModel:
    def __init__(self):
        self.num_cols = 7

        self.id = None
        self.account = None
        self.namespace = None
        self.type = None
        self.fields = None
        self.row = None
        self.created = None


    def load_from_list(self, insert_list):
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
        insert_dict = dict(insert_dict)

        self.id = None
        self.account = None
        self.namespace = None
        self.type = None
        self.fields = None
        self.row = None
        self.created = None

        if 'id' in insert_dict.keys():
            self.id = insert_dict['id']

        if 'account' in insert_dict.keys():
            self.account = insert_dict['account']

        if 'namespace' in insert_dict.keys():
            self.account = insert_dict['namespace']
        
        if 'type' in insert_dict.keys():
            self.type = insert_dict['type']

        if 'fields' in insert_dict.keys():
            self.fields = insert_dict['fields']

        if 'row' in insert_dict.keys():
            self.row = insert_dict['row']

        if 'created' in insert_dict.keys():
            self.created = insert_dict['created']


    def to_list(self):
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
        output_json = json.dumps(self.to_dict())
        return output_json

    def get_data_dict(self):
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

