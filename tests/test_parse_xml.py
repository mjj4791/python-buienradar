"""Testing xml parsing."""
from datetime import datetime, timedelta

import requests_mock
import xmltodict

from buienradar.buienradar import get_data, parse_data
from buienradar.buienradar_xml import (
    __BRACTUEELWEER,
    __BRLAT,
    __BRLON,
    __BRROOT,
    __BRSTATIONCODE,
    __BRSTATIONNAAM,
    __BRTEXT,
    __BRWEERGEGEVENS,
    __BRWEERSTATION,
    __BRWEERSTATIONS,
    __BRZIN,
    SENSOR_TYPES,
    __get_ws_distance,
    __parse_precipfc_data,
    __to_localdatetime
)
from buienradar.constants import (
    CONDITION,
    CONTENT,
    DATA,
    FORECAST,
    GROUNDTEMP,
    HUMIDITY,
    IRRADIANCE,
    MEASURED,
    MESSAGE,
    PRECIPITATION,
    PRESSURE,
    RAINCONTENT,
    STATIONNAME,
    SUCCESS,
    TEMPERATURE,
    VISIBILITY,
    WINDAZIMUTH,
    WINDDIRECTION,
    WINDFORCE,
    WINDGUST,
    WINDSPEED
)
from buienradar.urls import XML_FEED_URL, xml_precipitation_forecast_url

__TIMEZONE = 'Europe/Amsterdam'
__DATE_FORMAT = '%m/%d/%Y %H:%M:%S'


def load_file(name):
    """Load file with test data."""
    file = open(name, 'r')
    data = file.read()
    file.close()
    return data


def get_imageurl(img):
    """Get the image url helper function."""
    result = 'https://www.buienradar.nl/'
    result += 'resources/images/icons/weather/30x30/'
    result += img
    result += '.png'
    return result


def test_to_localdatetime():
    """Check the working of the to_localdatetime function."""
    # check invalid dates:
    dt = __to_localdatetime('')
    assert (dt is None)

    dt = __to_localdatetime(None)
    assert (dt is None)

    dt = __to_localdatetime('01/02/2017 03:04:05')
    assert (("%s" % dt) == '2017-01-02 03:04:05+01:00')

    # (invalid) month:
    dt = __to_localdatetime('00/02/2017 03:04:05')
    assert (dt is None)

    dt = __to_localdatetime('12/02/2017 03:04:05')
    assert (("%s" % dt) == '2017-12-02 03:04:05+01:00')

    dt = __to_localdatetime('13/02/2017 03:04:05')
    assert (dt is None)

    # (invalid) day:
    dt = __to_localdatetime('01/00/2017 03:04:05')
    assert (dt is None)

    dt = __to_localdatetime('01/31/2017 03:04:05')
    assert (("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('01/32/2017 03:04:05')
    assert (dt is None)

    dt = __to_localdatetime('02/28/2017 03:04:05')
    assert (("%s" % dt) == '2017-02-28 03:04:05+01:00')

    dt = __to_localdatetime('02/29/2017 03:04:05')
    assert (dt is None)

    # (invalid) year:
    dt = __to_localdatetime('01/01/17 03:04:05')
    assert (dt is None)

    dt = __to_localdatetime('01/1/017 03:04:05')
    assert (dt is None)

    # (invalid) hour:
    dt = __to_localdatetime('01/31/2017 00:04:05')
    assert (("%s" % dt) == '2017-01-31 00:04:05+01:00')

    dt = __to_localdatetime('01/31/2017 03:04:05')
    assert (("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('01/31/2017 23:04:05')
    assert (("%s" % dt) == '2017-01-31 23:04:05+01:00')

    dt = __to_localdatetime('01/1/2017 24:04:05')
    assert (dt is None)

    dt = __to_localdatetime('01/1/2017 25:04:05')
    assert (dt is None)

    dt = __to_localdatetime('01/1/2017 01:04:05 PM')
    assert (dt is None)

    dt = __to_localdatetime('01/1/2017 01:04:05 AM')
    assert (dt is None)

    # (invalid) minute:
    dt = __to_localdatetime('01/31/2017 03:00:05')
    assert (("%s" % dt) == '2017-01-31 03:00:05+01:00')

    dt = __to_localdatetime('01/31/2017 03:04:05')
    assert (("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('01/31/2017 03:59:05')
    assert (("%s" % dt) == '2017-01-31 03:59:05+01:00')

    dt = __to_localdatetime('01/01/2017 03:60:05')
    assert (dt is None)

    dt = __to_localdatetime('01/1/2017 25:-4:05')
    assert (dt is None)

    # (invalid) second:
    dt = __to_localdatetime('01/31/2017 03:04:00')
    assert (("%s" % dt) == '2017-01-31 03:04:00+01:00')

    dt = __to_localdatetime('01/31/2017 03:04:01')
    assert (("%s" % dt) == '2017-01-31 03:04:01+01:00')

    dt = __to_localdatetime('01/31/2017 03:04:59')
    assert (("%s" % dt) == '2017-01-31 03:04:59+01:00')

    dt = __to_localdatetime('01/1/2017 24:04:60')
    assert (dt is None)

    dt = __to_localdatetime('01/1/2017 25:04:-5')
    assert (dt is None)

    dt = __to_localdatetime('01/31/2017 03:04:05')
    assert (("%s" % dt) == '2017-01-31 03:04:05+01:00')

    # check DST/tz offset:
    dt = __to_localdatetime('01/02/2017 01:02:03')
    assert (("%s" % dt) == '2017-01-02 01:02:03+01:00')

    dt = __to_localdatetime('02/28/2017 13:31:11')
    assert (("%s" % dt) == '2017-02-28 13:31:11+01:00')

    dt = __to_localdatetime('12/31/2017 13:31:11')
    assert (("%s" % dt) == '2017-12-31 13:31:11+01:00')

    dt = __to_localdatetime('07/10/2017 13:31:11')
    assert (("%s" % dt) == '2017-07-10 13:31:11+02:00')


def test_rain_data(snapshot):
    """Test format of retrieved LIVE rain data."""
    latitude = 52.091579
    longitude = 5.119734
    with requests_mock.Mocker() as m:
        m.get(XML_FEED_URL, text=load_file('tests/xml/buienradar.xml'))
        m.get(
            xml_precipitation_forecast_url(latitude, longitude),
            text=load_file('tests/raindata/raindata.txt')
        )

        result = get_data(latitude, longitude, usexml=True)

    # we must have content:
    assert result == snapshot
    assert (result[CONTENT] is not None)
    assert (result[RAINCONTENT] is not None)

    # check raindata:
    lines = result[RAINCONTENT].splitlines()

    for line in lines:
        (val, key) = line.split("|")

        try:
            # value must be a integer value:
            val = int(val)
        except ValueError:
            print("Uunable to parse line: <%s>, not na integer." % (line))
            assert (False)

        try:
            datetime.strptime(key, '%H:%M')
        except ValueError:
            print("Unable to parse line: <%s>, not na time (HH:MM)." % (line))


def test_xml_data(snapshot):
    """Check xml data elements/xsd."""
    latitude = 52.091579
    longitude = 5.119734
    with requests_mock.Mocker() as m:
        m.get(XML_FEED_URL, text=load_file('tests/xml/buienradar.xml'))
        m.get(
            xml_precipitation_forecast_url(latitude, longitude),
            text=load_file('tests/raindata/raindata.txt')
        )

        result = get_data(latitude, longitude, usexml=True)

    # we must have content:
    assert result == snapshot
    assert (result[CONTENT] is not None)
    assert (result[RAINCONTENT] is not None)

    # check all elements we use from the xml:
    xmldata = xmltodict.parse(result[CONTENT])[__BRROOT]
    weergegevens = xmldata[__BRWEERGEGEVENS]
    assert (weergegevens is not None)

    actueelweer = weergegevens[__BRACTUEELWEER]
    assert (actueelweer is not None)

    weerstations = actueelweer[__BRWEERSTATIONS]
    assert (weerstations is not None)

    weerstation = weerstations[__BRWEERSTATION]
    assert (weerstation is not None)

    weerstation = weerstation[1]
    assert (weerstation[__BRLAT] is not None)
    assert (weerstation[__BRLON] is not None)

    assert (weerstation[__BRSTATIONCODE] is not None)
    assert (weerstation[__BRSTATIONNAAM] is not None)
    assert (weerstation[__BRSTATIONNAAM][__BRTEXT] is not None)
    assert (weerstation[SENSOR_TYPES[HUMIDITY][0]] is not None)
    assert (weerstation[SENSOR_TYPES[GROUNDTEMP][0]] is not None)
    assert (weerstation[SENSOR_TYPES[IRRADIANCE][0]] is not None)
    assert (weerstation[SENSOR_TYPES[MEASURED][0]] is not None)
    assert (weerstation[SENSOR_TYPES[PRECIPITATION][0]] is not None)
    assert (weerstation[SENSOR_TYPES[PRESSURE][0]] is not None)
    assert (weerstation[SENSOR_TYPES[STATIONNAME][0]] is not None)
    assert (weerstation[SENSOR_TYPES[CONDITION][0]] is not None)
    assert (weerstation[SENSOR_TYPES[CONDITION][0]][__BRZIN] is not None)
    assert (weerstation[SENSOR_TYPES[CONDITION][0]][__BRTEXT] is not None)
    assert (weerstation[SENSOR_TYPES[TEMPERATURE][0]] is not None)
    assert (weerstation[SENSOR_TYPES[VISIBILITY][0]] is not None)
    assert (weerstation[SENSOR_TYPES[WINDSPEED][0]] is not None)
    assert (weerstation[SENSOR_TYPES[WINDFORCE][0]] is not None)
    assert (weerstation[SENSOR_TYPES[WINDDIRECTION][0]] is not None)
    assert (weerstation[SENSOR_TYPES[WINDAZIMUTH][0]] is not None)
    assert (weerstation[SENSOR_TYPES[WINDGUST][0]] is not None)


def test_precip_fc(snapshot):
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "000|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    assert result == snapshot


def test_precip_fc2(snapshot):
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    assert result == snapshot


def test_precip_fc3(snapshot):
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    assert result == snapshot


def test_precip_fc4(snapshot):
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "077|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    assert result == snapshot


def test_precip_fc5(snapshot):
    """Test parsing precipitation forecast data."""
    data = ""
    data += "000|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                          timedelta(minutes=0)).strftime("%H:%M")
    data += "217|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                          timedelta(minutes=5)).strftime("%H:%M")
    data += "208|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                          timedelta(minutes=15)).strftime("%H:%M")
    data += "145|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                          timedelta(minutes=20)).strftime("%H:%M")
    data += "131|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                          timedelta(minutes=25)).strftime("%H:%M")
    data += "00|%s\n" % (datetime.now() +                   # noqa: ignore=W504
                         timedelta(minutes=30)).strftime("%H:%M")
    data += "00|%s\n" % (datetime.now() +                   # noqa: ignore=W504
                         timedelta(minutes=35)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    assert result == snapshot


def test_precip_decimal_values(snapshot):
    """Test parsing precipitation forecast data containing decimal values."""
    def timeframe(minutes=0):
        return (datetime.now() + timedelta(minutes=minutes)).strftime("%H:%M")

    data = ""
    data += "10,10|%s\n" % timeframe(0)
    data += "100|%s\n" % timeframe(5)
    data += "192,456798213|%s\n" % timeframe(10)
    data += "55.55|%s\n" % timeframe(15)

    result = __parse_precipfc_data(data, 20)
    assert result == snapshot


def test_parse_timeframe():
    """Test loading and parsing xml file."""
    data = None
    raindata = None

    latitude = 51.50
    longitude = 6.20
    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 4, usexml=True)
        # timeframe=4 should raise a ValueError, so:
        assert (False)
    except ValueError:
        # timeframe=4 should raise a ValueError, so:
        assert (True)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 5, usexml=True)
        # timeframe=5 should NOT raise a ValueError, so:
        assert (True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=5 should NOT raise a ValueError, so:
        assert (False)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 121, usexml=True)
        # timeframe=121 should raise a ValueError, so:
        assert (False)
    except ValueError:
        # timeframe=121 should raise a ValueError, so:
        assert (True)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 120, usexml=True)
        # timeframe=120 should NOT raise a ValueError, so:
        assert (True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=120 should NOT raise a ValueError, so:
        assert (False)


def test_readdata1_60(snapshot):
    """Test loading and parsing xml file."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar.xml')
    raindata = load_file('tests/raindata/raindata.txt')

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, raindata, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6391)' in result[DATA][STATIONNAME])


def test_readdata1_30(snapshot):
    """Test loading and parsing xml file."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar.xml')
    raindata = load_file('tests/raindata/raindata.txt')

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20

    result = parse_data(data, raindata, latitude, longitude, 30, usexml=True)
    assert (result[SUCCESS] and result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6391)' in result[DATA][STATIONNAME])
    assert result == snapshot


def test_readdata2_60(snapshot):
    """Test loading and parsing xml file."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar.xml')
    raindata = load_file('tests/raindata/raindata77.txt')

    # select non-first weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation De Bilt (6260)
    latitude = 52.11
    longitude = 5.19
    result = parse_data(data, raindata, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6260)' in result[DATA][STATIONNAME])


def test_readdata2_30(snapshot):
    """Test loading and parsing xml file."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar.xml')
    raindata = load_file('tests/raindata/raindata77.txt')

    # select non-first weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation De Bilt (6260)
    latitude = 52.11
    longitude = 5.19

    result = parse_data(data, raindata, latitude, longitude, 30, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6260)' in result[DATA][STATIONNAME])


def test_readdata3(snapshot):
    """Test loading and parsing xml file."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar.xml')

    # select last weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation Zeeplatform K13 (6252)
    latitude = 53.23
    longitude = 3.23
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6252)' in result[DATA][STATIONNAME])


def test_noxml(snapshot):
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    data = load_file('tests/xml/buienradar_noxml.xml')

    result = parse_data(data, None, usexml=True)

    # test calling results in the loop close cleanly
    assert result == snapshot
    assert (result[SUCCESS] is False and              # noqa: ignore=W504
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_noroot(snapshot):
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    data = load_file('tests/xml/buienradar_noroot.xml')

    result = parse_data(data, None, usexml=True)

    # test calling results in the loop close cleanly
    assert result == snapshot
    assert (result[SUCCESS] is False and               # noqa: ignore=W504
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_nows(snapshot):
    """Test loading and parsing invalid xml file; no weatherstation."""
    data = load_file('tests/xml/buienradar_nows.xml')

    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False and                # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/xml/buienradar_nows2.xml', 'r')
    data = file.read()
    file.close()
    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False and                # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/xml/buienradar_nows3.xml', 'r')
    data = file.read()
    file.close()
    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False and                # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/xml/buienradar_nows4.xml', 'r')
    data = file.read()
    file.close()
    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False and                # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/xml/buienradar_nows5.xml', 'r')
    data = file.read()
    file.close()
    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False and                # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')


def test_wsdistancen_with_none():
    """Test distance function without valid input."""
    latitude = 51.50
    longitude = 6.20
    distance = __get_ws_distance(None, latitude, longitude)
    assert (distance is None)


def test_nofc():
    """Test loading and parsing invalid xml file: no forecast data."""
    data = load_file('tests/xml/buienradar_nofc.xml')

    result = parse_data(data, None, usexml=True)
    # test calling results in the loop close cleanly
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == 'Unable to extract forecast data.')


def test_nofc2(snapshot):
    """Test loading and parsing invalid xml file; no forecast."""
    data = load_file('tests/xml/buienradar_nofc2.xml')

    result = parse_data(data, None, usexml=True)
    assert result == snapshot
    # test calling results in the loop close cleanly
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            len(result[DATA][FORECAST]) == 0)


def test_missing_data(snapshot):
    """Test loading and parsing invalid xml file; missing data fields."""
    data = load_file('tests/xml/buienradar_missing.xml')

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: stationnaam ")

    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: icoonactueel ")

    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: luchtvochtigheid ")

    latitude = 52.10
    longitude = 5.18
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: temperatuurGC ")

    latitude = 52.92
    longitude = 4.78
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: temperatuur10cm ")

    latitude = 51.45
    longitude = 5.42
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidMS ")

    latitude = 51.20
    longitude = 5.77
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidBF ")

    latitude = 52.00
    longitude = 3.28
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windrichtingGR ")

    latitude = 51.57
    longitude = 4.93
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windrichting ")

    latitude = 52.07
    longitude = 6.65
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: luchtdruk ")

    latitude = 52.43
    longitude = 6.27
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windstotenMS ")

    latitude = 51.87
    longitude = 5.15
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: regenMMPU ")

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: zonintensiteitWM2 ")


def test_invalid_data(snapshot):
    """Test loading and parsing xml file with data that cannot be parsed."""
    data = load_file('tests/xml/buienradar_invalid.xml')

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] is False)
    assert (result[MESSAGE] == 'Location data is invalid.')

    data = load_file('tests/xml/buienradar_invalidfc1.xml')

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                                  # noqa: ignore=W504
           result[MESSAGE] is None)
    # test missing maxtemp:
    assert (len(result[DATA][FORECAST]) == 5 and                 # noqa: ignore=W504
           result[DATA][FORECAST][0][TEMPERATURE] == 0.0)
    # test missing maxgtemp and maxtempmax:
    assert (len(result[DATA][FORECAST]) == 5 and                 # noqa: ignore=W504
           result[DATA][FORECAST][2][TEMPERATURE] == 0.0)

    # read xml with invalid ws coordinates
    data = load_file('tests/xml/buienradar_invalidws1.xml')
    # 'Meetstation Arcen' contains invalid gps info,
    # 'Meetstation Volkel' will be selected as alternative
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and                                  # noqa: ignore=W504
           '(6375)' in result[DATA][STATIONNAME])

    # 'Meetstation Arnhem' contains invalid gps info,
    # 'Meetstation De Bilt' will be selected as alternative
    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and '(6260)' in result[DATA][STATIONNAME])

    # 'Meetstation Berkhout' contains invalid gps info,
    # 'Meetstation Wijdenes' will be selected as alternative
    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and '(6248)' in result[DATA][STATIONNAME])


def test_id_upper1(snapshot):
    """Test loading and xml file with id in uppercase."""
    # load buienradar.xml
    data = load_file('tests/xml/buienradar_id_upper.xml')
    raindata = load_file('tests/raindata/raindata.txt')

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, raindata, latitude, longitude, usexml=True)
    assert result == snapshot
    assert (result[SUCCESS] and result[MESSAGE] is None)
    # check the selected weatherstation:
    assert (result[SUCCESS] and                              # noqa: ignore=W504
           '(6391)' in result[DATA][STATIONNAME])
