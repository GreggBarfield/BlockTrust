def format_field(field):
    """Format a input field.

    Params:
        field: The input field (str)
    """
    if field is None:
        raise ValueError("field can't be None")
    if b'\x00' in field.encode("utf-8"):
        raise ValueError("Null bytes in the field??? Stop whatever is going on")
    field.strip(" \n\r\t")
    return field if field != '' else None