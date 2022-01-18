# This dictionary specifies the product type for each product in the products table

product_types_by_id = {
    1: "Dual Frequency",
    2: "High Frequency",
    3: "Low Frequency",
    4: "USDA 840"
}

product_types_by_name = {
    value: key
    for key, value in product_types_by_id.items()
}
