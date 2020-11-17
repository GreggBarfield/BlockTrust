# Note: this is a dictionary to stress that the keys should not be changed
# This definitely needs to be changed

sectors_by_id = {
    4: "Cow-Calf",
    5: "Auction House",
    6: "Feedlot",
    7: "Packer"
}

sectors_by_name = {
    value: key
    for key, value in sectors_by_id.items()
}

