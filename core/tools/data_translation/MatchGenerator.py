# Class MatchGenerator

class MatchGenerator:
    """ MatchGenerator is a base class
        to describe specific MatchGenerator 
        Implementations.
        
        Its purpose is to make developing
        match generating objects more easily
    """
    def generate_matches(self, insert):
        """ generate_matches is a general function
            that will be called to make match objects
            from insert objects. All MatchGenerator objects
            will implment this function.

            Params:
                insert: An InsertModel instance corresponding
                        to table data.

            Returns: A list of MatchModel objects corresponding to possible
                     matches given the data.
        """
        matches = []

        return matches