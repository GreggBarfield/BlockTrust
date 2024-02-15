# Note: this is a dictionary to stress that the keys should not be changed

MATCH_TYPES_ID_TO_NAME = {
    1: "Sighting",
    4: "Born",
    10: "Visual ID",
    11: "Weaned",
    12: "First Birth",
    14: "Hot Weight",
    15: "Packer",
    16: "USDA Quality Grade",
    17: "USDA Yield Grade",
    18: "Died",
    19: "Railed",
    20: "Medical",
    21: "Sold",
    22: "Insemination"
}

MATCH_TYPES_NAME_TO_ID = {
    value: key
    for key, value in MATCH_TYPES_ID_TO_NAME.items()
}


def convert_match_type_names_to_ids(value):
    """Converts value from name to id.

    Params:
        value: either a str or a list/tuple of strs

    Returns:
        The value as ID (int) or a tuple of the conversions
    """
    if isinstance(value, (list, tuple)):
        return tuple(convert_match_type_names_to_ids(v) for v in value)

    return MATCH_TYPES_NAME_TO_ID[value]
