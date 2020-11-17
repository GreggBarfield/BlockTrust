# Note: this is a dictionary to stress that the keys should not be changed
# This definitely needs to be changed

# Match description should be printable

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

match_types_by_name = {
    value: key
    for key, value in match_types_by_id.items()
}
