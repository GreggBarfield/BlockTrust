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


def validate_email(email):
    """
    Validates the provided email

    Params:
        email: The email which needs to be validated

    Raises:
        Exception with appropriate message if the email is invalid

    Returns:
        Dictionary with result and message
    """
    if len(email) == 0:
        return {"success": False, "message": "Email is blank." } 
    if '@' not in email or '.' not in email or len(email) < 5:
        return {"success": False, "message": "The email you entered is incomplete." }
    if ' ' in email:
        return {"result": False, "message": "Spaces cannot be in the email." }
    return {"success": True, "message": "" } 
