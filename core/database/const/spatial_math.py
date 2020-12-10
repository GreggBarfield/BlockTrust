import math

def lla_wgs84_to_ecef(lat, lon, alt=0):
    """Converts wgs84 lat/lon/alt to ECEF.

    Params:
        lat, lon: degrees
        alt: meters (default 0)
    Returns:
        x, y, z ECEF in meters
    """
    # From https://gis.stackexchange.com/questions/230160/converting-wgs84-to-ecef-in-python
    rad_lat = lat * (math.pi / 180.0)
    rad_lon = lon * (math.pi / 180.0)

    a = 6378137.0
    finv = 298.257223563
    f = 1 / finv
    e2 = 1 - (1 - f) * (1 - f)
    v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

    x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
    y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
    z = (v * (1 - e2) + alt) * math.sin(rad_lat)

    return x, y, z

def miles_to_meters(miles):
    """Converts miles to meters.

    Params:
        miles: The distance in miles
    
    Returns:
        The distance in meters
    """
    return miles * 1609.344

def distance(p1, p2):
    """Calculates the distance in meters between two points in ECEF meters.

    Params:
        p1, p2: ECEF in meters
    
    Returns:
        Distance in meters
    """
    return math.sqrt(sum((
        (p1[0] - p2[0])
        for i in range(3)
    )))
