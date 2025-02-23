"""(functions that generate) URL's to access the buienradar api."""
JSON_FEED_URL = 'https://data.buienradar.nl/2.0/feed/json'
XML_FEED_URL = 'https://xml.buienradar.nl/'
XML_SECONDARY_FEED_URL = 'https://api.buienradar.nl/'

JSON_PRECIPITATION_URL_TEMPLATE = (
    'https://gps.buienradar.nl/getrr.php?lat={lat}&lon={lon}'
)
XML_PRECIPITATION_URL_TEMPLATE = (
    'https://gps.buienradar.nl/getrr.php?lat={lat}&lon={lon}'
)
RADAR_URL_TEMPLATE = (
    'https://api.buienradar.nl/image/1.0/RadarMapNL?w={w}&h={h}'
)


def xml_precipitation_forecast_url(latitude: float, longitude: float) -> str:
    """Build URL to precipation forecast URL."""
    return XML_PRECIPITATION_URL_TEMPLATE.format(
        lat=round(latitude, 2),
        lon=round(longitude, 2)
    )


def json_precipitation_forecast_url(latitude: float, longitude: float) \
        -> str:
    """Build URL to precipation forecast URL (used from json)."""
    return JSON_PRECIPITATION_URL_TEMPLATE.format(
        lat=round(latitude, 2),
        lon=round(longitude, 2)
    )


def radar_url(width: int = 500, height: int = 512) -> str:
    """
    Build Buienradar radar image URL.

    :param width width of output (120 <= w <= 700)
    :param height height of output (120 <= h <= 765)
    """
    if width < 120 or width > 700:
        raise ValueError("Illegal width, valid range: 120-700")
    if height < 120 or height > 765:
        raise ValueError("Illegal height, valid rang: 120-765")

    return RADAR_URL_TEMPLATE.format(w=width, h=height)
