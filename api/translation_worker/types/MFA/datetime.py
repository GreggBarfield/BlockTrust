from ...exceptions import ExecutionException
from dateutil.parser import isoparse


def all_to_unix(d):
    """Converts a date time string to Unix format.

    Returns:
        An int or None if conversion failed or would be meaningless
    """
    if isinstance(d, int):
        return d
    if not isinstance(d, str):
        return None

    d = d.strip("\r\n ")

    invalids = ["", "null", "true", "false"]

    for invalid in invalids:
        if d.lower() == invalid:
            return None

    # ISO-8601 'T' type, standard date
    if 'T' in d or len(d) == len("0000-00-00") and d.count("-") == 2:
        try:
            return int(isoparse(d).timestamp())
        except ValueError:
            raise ExecutionException("Failed to convert expected iso-8601: " + d)

    raise ExecutionException("Did not recognize date: " + d)
