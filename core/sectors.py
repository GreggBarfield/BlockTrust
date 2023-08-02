# Note: this is a dictionary to stress that the keys should not be changed
# This definitely needs to be changed

SECTORS_ID_TO_NAME = {
    4: "Cow-Calf",
    5: "Auction",
    6: "Feedlot",
    7: "Packer",
    8: "Buyer",
    9: "Financial",
    10: "Stocker/Backgrounder",
    11: "Producer Service"
}

SECTORS_NAME_TO_ID = {
    value: key
    for key, value in SECTORS_ID_TO_NAME.items()
}
