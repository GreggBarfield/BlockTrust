import MatchGenerator
import MatchModel
import InsertModel
from datetime import datetime
class MatchGeneratorMFA(MatchGenerator.MatchGenerator):
    """ MatchGeneratorMFA is an implementation of MatchGenerator
        It's purpose is to generate MatchModel objects given
        InsertModel objects.

        One call to generate_matches is meant to generate all possible matches for
        a given InsertModel object in the MFA namespace.

        IMPORTANT: Many specific instances of generate_[type]_match exist. To make
        this file less cluttered, they all will be described here.
        These should only be considered private functions though.

            Params: 
                insert: An instance of the InsertModel class.

            Returns:
                new_match: An instance of the MatchModel class.
                None: In the case no match could be made
    
    """
    def __init__(self):
        pass

    def generate_matches(self, insert):
        """ generate_matches is the main, callable function of MatchGeneratorMFA
            It generate all possible matches for the InsertModel that it is given.

            Params:
                insert: an instance of an InsertModel object corresponding
                        to a a row in the inserts table

            Returns:
                matches: a list of MatchModel objects

        """
        matches = []

        temp_matches = self.generate_weaned_match(insert)
        if (temp_matches):
            matches.append(temp_matches)

        temp_matches = self.generate_died_match(insert)
        if (temp_matches):
            matches.append(temp_matches)

        temp_matches = self.generate_born_match(insert)
        if (temp_matches):
            matches.append(temp_matches)

        temp_matches = self.generate_visual_id_match(insert)
        if (temp_matches):
            matches.append(temp_matches)

        return matches

    def generate_matches_for_animal(self, insert):
        matches = []

        return matches

    def generate_sighting_match(self, insert):
        pass

    def generate_born_match(self, insert):
        # Look for Birthdate or Birthweight field
        try:
            if 'Birthdate' in insert.fields:
                birth_date = insert.get_data_dict()['Birthdate']
                if (birth_date == '' or birth_date == None):
                    return None

                new_match = MatchModel.MatchModel()
                new_match.account = insert.account
                new_match.eid = insert.get_data_dict()['EID']
                new_match.type = 4

                created_date = insert.created
                created_date = self.date_to_epoch(created_date)
                new_match.created = created_date

                birth_date = self.date_to_epoch(birth_date)
                new_match.time = birth_date
                return new_match
            else:
                return None
        except Exception as e:
            print('generate_born_match failed.')
            return None


    def generate_visual_id_match(self, insert):
        # Look for VisualID field
        try:
            if 'VisualID' in insert.fields:
                visual_id = insert.get_data_dict()['VisualID']
                if (visual_id == ''):
                    return None

                new_match = MatchModel.MatchModel()
                new_match.account = insert.account
                new_match.eid = insert.get_data_dict()['EID']
                new_match.type = 10

                created_date = insert.created
                created_date = self.date_to_epoch(created_date)
                new_match.created = created_date

                new_match.data = str(visual_id)
                return new_match
            else:
                return None
        except Exception as e:
            print('generate_visual_id_match failed.')
            return None


    def generate_weaned_match(self, insert):
        # look for WeanDate field
        try:
            if 'WeanDate' in insert.fields:
                new_match = MatchModel.MatchModel()
                new_match.account = insert.account
                new_match.eid = insert.get_data_dict()['EID']
                new_match.type = 11

                created_date = insert.created
                created_date = self.date_to_epoch(created_date)
                new_match.created = created_date
                return new_match
            else:
                return None
        except Exception as e:
            print('generate_weaned_match failed.')
            return None

    def generate_first_birth_match(self, insert):
        pass

    def generate_visual_id_complex_match(self, insert):
        pass

    def generate_hot_weight_match(self, insert):
        pass
    
    def generate_packer_match(self, insert):
        pass

    def generate_usda_quality_grade_match(self, insert):
        pass

    def generate_usda_yield_grade_match(self, insert):
        pass

    def generate_died_match(self, insert):
        # Look for DeathDate field
        try:
            if 'DeathDate' in insert.fields:

                death_date = insert.get_data_dict()['DeathDate']
                if (death_date == '' or death_date == None):
                    return None

                new_match = MatchModel.MatchModel()
                new_match.account = insert.account
                new_match.eid = insert.get_data_dict()['EID']

                new_match.type = 18

                created_date = insert.created
                created_date = self.date_to_epoch(created_date)
                new_match.created = created_date

                death_date = self.date_to_epoch(death_date)
                new_match.time = death_date

                return new_match
            else:
                return None
        except Exception as e:
            print('generate_died_match failed')
            return None

    def generate_railed_match(self, insert):
        pass

    def generate_medical_match(self, insert):
        pass

    def generate_sold_match(self, insert):
        pass

    def date_to_epoch(self, s):
        """ date_to_epoch converts a date time string from sql into 
            its epoch equivalent.

            Params:
                s: a date time string from sql

            Returns:
                the epoch date time value as an integer.
        """
        n_in = False
        digits = ''.join([str(i) for i in range(10)])
        for c in s:
            if c in digits:
                n_in = True
        if not n_in:
            return 0
        date, time = s.split(" ")
        year, month, day = list(map(int, date.split("-")))
        if year <= 1800:
            return 0
        hms = list(map(int, time.split(":")))
        return int(datetime(year,month,day,*hms).timestamp())
