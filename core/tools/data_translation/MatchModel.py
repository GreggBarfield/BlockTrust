import json
class MatchModel:
    def __init__(self):
        self.num_cols = 11

        #int
        self.id = None
        #int
        self.account = None
        #int
        self.account_link = None
        #bigint
        self.eid = None
        #double
        self.lat = None
        #double
        self.lon = None
        #int
        self.time = None
        #int
        self.created = None
        #int
        self.type = None
        # varchar(127)
        self.raw_identifier = None
        # json
        self.data = None

    def load_from_list(self, match_list):
        # This assumes that all values are given in order of DB
        if (len(match_list) == self.num_cols):
            self.id = None
            self.account = None
            self.account_link = None
            self.eid = None
            self.lat = None
            self.lon = None
            self.time = None
            self.created = None
            self.type = None
            self.raw_identifier = None
            self.data = None

            return True
        else:
            return False

    def load_from_dict(self, match_dict):
        match_dict = dict(match_dict)

        self.id = None
        self.account = None
        self.account_link = None
        self.eid = None
        self.lat = None
        self.lon = None
        self.time = None
        self.created = None
        self.type = None
        self.raw_identifier = None
        self.data = None

        if 'id' in match_dict.keys():
            self.id = match_dict['id']

        if 'account' in match_dict.keys():
            self.accountk = match_dict['account']

        if 'account_link' in match_dict.keys():
            self.account_link = match_dict['account_link']

        if 'eid' in match_dict.keys():
            self.eid = match_dict['eid']

        if 'lat' in match_dict.keys():
            self.lat = match_dict['lat']

        if 'lon' in match_dict.keys():
            self.lon = match_dict['lon']

        if 'time' in match_dict.keys():
            self.time = match_dict['time']

        if 'created' in match_dict.keys():
            self.created = match_dict['created']

        return True

        



    def to_list(self):
        output_list = []

        output_list.append(self.id)
        output_list.append(self.account)
        output_list.append(self.account_link)
        output_list.append(self.eid)
        output_list.append(self.lat)
        output_list.append(self.lon)
        output_list.append(self.time)
        output_list.append(self.created)
        output_list.append(self.type)
        output_list.append(self.raw_identifier)
        output_list.append(self.data)

        return output_list

    def to_dict(self):
        output_dict = {}

        output_dict['id'] = self.id
        output_dict['account'] = self.account
        output_dict['account_link'] = self.account_link
        output_dict['eid'] =  self.eid
        output_dict['lat'] = self.lat
        output_dict['lon'] = self.lon
        output_dict['time'] = self.time
        output_dict['created'] = self.created
        output_dict['type'] = self.type
        output_dict['raw_identifier'] = self.raw_identifier
        output_dict['data'] = self.data

        return output_dict 

    def to_json(self):
        output_json = json.dumps(self.to_dict())
        return output_json

    def verify_values(self):
        is_valid = False
        #Returns whether the data can be uploaded to the matches table
        #id - integer - not null - auto increment
        #account - int - nullable
        #account link - nullable
        #eid - nullable
        #lat - double - nullable
        #lon - double - nullable
        #time - int - nullable
        #created - int - nullable
        #type - int - nullable
        #raw_identifier - varchar - nullable
        #data - json - nullable
        return is_valid