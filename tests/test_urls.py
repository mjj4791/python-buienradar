"""Test for URL utilities."""
from urllib.parse import urlparse, parse_qs

from buienradar.urls import (
    xml_precipitation_forecast_url,
    json_precipitation_forecast_url,
    radar_url,
)


def parse_qs_dict(url):
    """
    Parse a url and get a dictionary of query string elements in a dictionary.

    Raises ValueError when an element is repeated (to safely return a dict of
    strings instead of an dict of lists of strings.
    """
    token_dict = parse_qs(urlparse(url).query)
    res = {}

    for k, val in token_dict.items():
        if len(val) > 1:
            raise ValueError('Key {} has {} values'.format(k, len(val)))

        res[k] = val[0]

    return res


def test_base_urls():
    json_url = json_precipitation_forecast_url(1.23, 4.56)
    xml_url = xml_precipitation_forecast_url(1.23, 4.56)

    assert 'https://gpsgadget.buienradar.nl/data/raintext?' in json_url
    assert 'http://gadgets.buienradar.nl/data/raintext/?' in xml_url

    assert 'https://api.buienradar.nl/image/1.0/RadarMapNL?' in radar_url()


def test_util():
    """Test the utility function for dictionaries."""
    try:
        res = parse_qs_dict("http://example.org/?foo=1&bar=2")
        assert res['foo'] == '1'
        assert res['bar'] == '2'

        parse_qs_dict("http://example.org/?foo=1&foo=2")
        # Unreachable
        assert False
    except ValueError:
        assert True


def test_precipitation_forecast_url():
    """Test both variations of the precipation forcecast URL-builder."""
    for func in (xml_precipitation_forecast_url,
                 json_precipitation_forecast_url):
        # should return an url including identical 2-decimal lat/lon
        url = func(1.23, 4.56)
        tokens = parse_qs_dict(url)

        assert tokens['lat'] == '1.23' and tokens['lon'] == '4.56'

        # should return an url with truncated values
        url = func(1.23456, 7.890123)
        tokens = parse_qs_dict(url)

        assert tokens['lat'] == '1.23' and tokens['lon'] == '7.89'

        # that are rounded (up)
        url = func(1.235, 7.890123)
        tokens = parse_qs_dict(url)

        assert tokens['lat'] == '1.24'


def test_radar_url():
    """
    Test the generated radar url's.

      * Check that it echoes the correct values in the result.
      * Check that it excepts the extreme values of it's domain.

    Pairs used are valid size and some minimum/maximum sizes.
    """
    # test default value:
    tokens = parse_qs_dict(radar_url())
    default_w = int(tokens['w'])
    default_h = int(tokens['h'])

    assert (default_w >= 120 and default_w <= 700 and
            default_h >= 120 and default_h <= 700)

    # test pairs:
    for width, height in [(120, 120),
                          (300, 300),
                          (700, 700),
                          (700, 765)]:
        tokens = parse_qs_dict(radar_url(width, height))
        assert tokens['w'] == str(width) and tokens['h'] == str(height)


def test_radar_url_bounds():
    """Test illegal values for radar image url."""
    # outside of minimum/maximum width
    for width in [119, 701]:
        try:
            radar_url(width, 125)
            assert False
        except ValueError:
            assert True

    # outside of minimum/maximum height
    for height in [119, 766]:
        try:
            radar_url(125, height)
            assert False
        except ValueError:
            assert True

    # Check that it also raises when both are out of range
    try:
        radar_url(1234, 4567)
        assert False
    except ValueError:
        assert True
