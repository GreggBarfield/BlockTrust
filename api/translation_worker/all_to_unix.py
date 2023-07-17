from .exceptions import ExecutionException
from dateutil.parser import isoparse, parse
from datetime import datetime, timezone
import re  # Note that it automatically caches up to MAXCACHE
from pytz import timezone as pytz_timezone


def all_to_unix(d, tz=pytz_timezone('Etc/GMT+11')):
    """Converts a date time string to Unix timestamp.

    Params:
        d: String

    Returns:
        An int or None if it would be meaningless (null, 0-0-0, etc)
    """
    if not isinstance(d, str):
        raise ExecutionException("Failed to convert date, bad type")

    d = d.strip("\r\n\t ")

    equivalent_invalids = ["", "null", "true", "false"]

    for invalid in equivalent_invalids:
        if d.lower() == invalid:
            return None

    contains_invalids = ["12/31/9999", "01/01/0001", "01/01/01"]

    for invalid in contains_invalids:
        if invalid in d.lower():
            return None

    # Check for lack of any digits
    digit_exists = False

    for c in d:
        if c in (str(n) for n in range(0, 10)):
            break
    else:
        return None

    # Datetime is not bad

    try:
        result = parse(d)
    except (ValueError, OverflowError):
        raise ExecutionException("Dateutil failed to parse date: " + d)

    if result.tzinfo is None:
        result = result.replace(tzinfo=tz)

    # These checks shouldn't return None as we should have already validated
    # that it is a good date.

    if result.year < 1800:
        raise ExecutionException(
            "Failed to convert date, older than 1800: " + d
        )

    if result.year > datetime.now().year + 10:
        raise ExecutionException(
            "Failed to convert date, older than " + str(datetime.now().year + 10) + ": " + d
        )

    return result.timestamp()


def _old_all_to_unix(d):
    """Converts a date time string to Unix format.

    Assumed to be UTC/GMT.

    Warning: Broken

    Returns:
        An int or None if conversion failed or would be meaningless
    """
    if not isinstance(d, str):
        raise ExecutionException("Failed to convert date, bad type")

    d = d.strip("\r\n ")

    invalids = ["", "null", "true", "false"]

    for invalid in invalids:
        if d.lower() == invalid:
            return None

    if re.fullmatch("\\d*/\\d*/\\d*", d):
        month, day, year = list(map(int, d.split("/")))
        if year < 1800:
            raise ExecutionException(
                "Failed to convert american date, older than 1800: " + d
            )
        return int(datetime(year, month, day, tzinfo=timezone.utc).timestamp())

    elif re.fullmatch("\\d+/\\d+/\\d+ \\d+:\\d+:\\d+ (AM|PM)", d):
        p_date, p_time, p_period = d.split(" ")
        month, day, year = map(int, p_date.split("/"))
        hours, minutes, seconds = map(int, p_time.split(":"))

        if year < 1800:
            raise ExecutionException(
                "Failed to convert american date, older than 1800: " + d
            )

        if hours == 12 and p_period == "AM":
            hours = 0
        elif hours == 12 and p_period == "PM":
            hours = 12
        elif hours <= 12 and p_period == "PM":
            hours = hours + 12

        return int(datetime(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
            second=seconds,
            tzinfo=timezone.utc
        ).timestamp())

    # ISO-8601 'T' type, standard date
    if 'T' in d or len(d) == len("0000-00-00") and d.count("-") == 2:
        try:
            return int(isoparse(d).timestamp())
        except ValueError:
            raise ExecutionException("Failed to convert expected iso-8601: " + d)

    raise ExecutionException("Did not recognize date: " + d)
