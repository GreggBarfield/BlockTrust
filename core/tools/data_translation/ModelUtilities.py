#Model Utilities
import json

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
    if (val == None or val == ''):
        return True
    else:
        return False

def verify_type_by_id(val):
    try:
        if int(val) in match_types_by_id.keys():
            return True
        else:
            return False
    except:
        return False
