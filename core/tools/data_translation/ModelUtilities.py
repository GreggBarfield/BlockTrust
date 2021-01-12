#Model Utilities
import json

"""
    This file is meant to provide
    functions and data to make dealing with 
    model class types in a simpler manner.
"""

# Potential matches (This will likely be changed later)
match_types_by_id = {
    1: "Sighting",
    4: "Born",
    10: "Visual ID",
    11: "Weaned",
    12: "First Birth",
    13: "Visual ID Complex",
    14: "Hot Weight",
    15: "Packer",
    16: "USDA Quality Grade",
    17: "USDA Yield Grade",
    18: "Died",
    19: "Railed",
    20: "Medical",
    21: "Sold"
}


def verify_nullable_int(val):
    """ verify_nullable_int is a function
        meant to verify that a value is potentially
        a valid nullable sql integer value

        params:
            val: A string, integer, or None type

        Returns:
            True: The value is valid for sql upload
            False: The value is invalid for sql upload

    """
    if isinstance(val, str):
        if (val != ''):
            try:
                integer_val = int(val)
                return True
            except:
                print ('Tried checking string version')
                return False
        else:
            return True
    elif isinstance(val, int):
        #go ahead and continue, unless you want to verify that the integer 
        #is within a particular range
        return True
    elif (val == None):
        #nonetype is allowed, go ahead and continue
        return True
    else:
        print ('Tried else case')
        return False

def verify_nullable_float(val):
    """ verify_nullable_float is meant to determine
        whether a value is a valid nullable double/float value
        for sql

        Params:
            val: a string, float, integer, or None type that
                 could be a valid sql string.
        Returns:
            True: The value is valid for sql
            False: The value is not valid for sql

    """

    if isinstance(val, str):
        if (val != ''):
            try:
                float_val = float(val)
                return True
            except:
                return False
        else:
            return True
    elif isinstance(val, float):
        #go ahead and continue, unless you want to verify that the integer 
        #is within a particular range
        return True
    elif (val == None):
        #nonetype is allowed, go ahead and continue
        return True
    else:
        return False

def verify_nullable_json(val):
    """ verify_nullable_json verifies that
        a value may be a valid json string for uploading to SQL

        Params:
            val: A string, list, number, tuple, dictionary, or None type

        Returns: 
            True: The value can be considered valid for uploading
            False: The value cannot be considered valid.
    """
    if isinstance(val, str):
        if (val != ''):
            try:
                json_val = json.loads(val)
                return True
            except:
                #It is still allowed, but will just be a string
                return True
        else:
            return True
    elif (val == None):
        #nonetype is allowed, go ahead and continue
        return True
    else:
        try:
            json_val = json.loads(val)
            return True
        except:
            return False

def verify_nullable_str(val):
    """
        verify_nullable_str determines whether a value
        could be uploaded as a nullable varchar into sql.

        Params:
            val: The object in question to check

        Returns: 
            True: The object is valid for upload into sql.
            False: The object is not valid for upload. 
    """
    if (val == None or val == ''):
        return True
    else:
        return False

def verify_type_by_id(val):
    """
        verify_type_by_id is a function that verifies
        that the type value for a match is a valid match type.

        Params:
            val: an integer type value

        Returns:
            True: The given value is a valid match type id.
            False: The given value is not a valid match type key.
    """
    try:
        if int(val) in match_types_by_id.keys():
            return True
        else:
            return False
    except:
        return False
