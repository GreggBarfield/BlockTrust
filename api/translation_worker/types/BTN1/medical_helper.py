def format_data(
    product=None, method=None, location=None, symptom=None, fatal=None, category=None, diagnosis=None
):

    data = {}

    def is_something(s):
        return s is not None and s.strip().lower() not in (
            "n/a", "none", "", "na", "other", "unknown"
        )

    if is_something(product):
        data["product"] = product
    if is_something(location):
        data["location"] = location
    if is_something(symptom):
        data["symptom"] = symptom
    if is_something(method):
        data["method"] = method
    if fatal:
        data["fatal"] = fatal
    if is_something(category):
        data["category"] = category
    if is_something(diagnosis):
        data["diagnosis"] = diagnosis

    return data
