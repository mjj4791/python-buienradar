"""Testing json parsing."""
import json
from datetime import datetime, timedelta

import pytz

from buienradar.buienradar import get_data, parse_data
from buienradar.buienradar_json import (
    __ACTUAL,
    __LAT,
    __LON,
    __STATIONID,
    __STATIONMEASUREMENTS,
    __STATIONNAME,
    SENSOR_TYPES,
    __get_float,
    __get_int,
    __get_str,
    __get_windazimuth,
    __get_windspeed,
    __get_ws_distance,
    __getBarFC,
    __getBarFCName,
    __getBarFCNameNL,
    __parse_precipfc_data,
    __to_localdatetime
)
from buienradar.constants import (
    CONDITION,
    CONTENT,
    DATA,
    FEELTEMPERATURE,
    FORECAST,
    GROUNDTEMP,
    HUMIDITY,
    IRRADIANCE,
    MEASURED,
    MESSAGE,
    PRECIPITATION,
    PRESSURE,
    RAINCONTENT,
    RAINLAST24HOUR,
    RAINLASTHOUR,
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

__TIMEZONE = 'Europe/Amsterdam'
__DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def get_imageurl(img):
    """Get the image url helper function."""
    result = 'https://www.buienradar.nl/'
    result += 'resources/images/icons/weather/30x30/'
    result += img
    result += '.png'
    return result


def test_to_localdatetime():
    """Check he workign of the to_localdatetime function."""
    #  "timestamp": "2019-02-03T19:20:00",

    # check invalid dates:
    dt = __to_localdatetime('')
    assert(dt is None)

    dt = __to_localdatetime(None)
    assert(dt is None)

    dt = __to_localdatetime('2017-01-02T03:04:05')
    assert(("%s" % dt) == '2017-01-02 03:04:05+01:00')

    # (invalid) month:
    dt = __to_localdatetime('2017-00-02T03:04:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-12-02T03:04:05')
    assert(("%s" % dt) == '2017-12-02 03:04:05+01:00')

    dt = __to_localdatetime('2017-13-02T03:04:05')
    assert(dt is None)

    # (invalid) day:
    dt = __to_localdatetime('2017-01-00T03:04:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-31T03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('2017-01-32T03:04:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-02-28T03:04:05')
    assert(("%s" % dt) == '2017-02-28 03:04:05+01:00')

    dt = __to_localdatetime('2017-02-29T03:04:05')
    assert(dt is None)

    # (invalid) year:
    dt = __to_localdatetime('17-01-01T03:04:05')
    assert(dt is None)

    dt = __to_localdatetime('017-01-1T03:04:05')
    assert(dt is None)

    # (invalid) hour:
    dt = __to_localdatetime('2017-01-31T00:04:05')
    assert(("%s" % dt) == '2017-01-31 00:04:05+01:00')

    dt = __to_localdatetime('2017-01-31T03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('2017-01-31T23:04:05')
    assert(("%s" % dt) == '2017-01-31 23:04:05+01:00')

    dt = __to_localdatetime('2017-01-01T24:04:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-01T25:04:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-01T01:04:05 PM')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-01T01:04:05 AM')
    assert(dt is None)

    # (invalid) minute:
    dt = __to_localdatetime('2017-01-31T03:00:05')
    assert(("%s" % dt) == '2017-01-31 03:00:05+01:00')

    dt = __to_localdatetime('2017-01-31T03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = __to_localdatetime('2017-01-31T03:59:05')
    assert(("%s" % dt) == '2017-01-31 03:59:05+01:00')

    dt = __to_localdatetime('2017-01-01T03:60:05')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-01T25:-4:05')
    assert(dt is None)

    # (invalid) second:
    dt = __to_localdatetime('2017-01-31T03:04:00')
    assert(("%s" % dt) == '2017-01-31 03:04:00+01:00')

    dt = __to_localdatetime('2017-01-31T03:04:01')
    assert(("%s" % dt) == '2017-01-31 03:04:01+01:00')

    dt = __to_localdatetime('2017-01-31T03:04:59')
    assert(("%s" % dt) == '2017-01-31 03:04:59+01:00')

    dt = __to_localdatetime('2017-01-01T24:04:60')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-01T25:04:-5')
    assert(dt is None)

    dt = __to_localdatetime('2017-01-31T03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    # check DST/tz offset:
    dt = __to_localdatetime('2017-01-02T01:02:03')
    assert(("%s" % dt) == '2017-01-02 01:02:03+01:00')

    dt = __to_localdatetime('2017-02-28T13:31:11')
    assert(("%s" % dt) == '2017-02-28 13:31:11+01:00')

    dt = __to_localdatetime('2017-12-31T13:31:11')
    assert(("%s" % dt) == '2017-12-31 13:31:11+01:00')

    dt = __to_localdatetime('2017-07-10T13:31:11')
    assert(("%s" % dt) == '2017-07-10 13:31:11+02:00')


def test_rain_data():
    """Test format of retrieved rain data."""
    result = get_data(usexml=False)

    # we must have content:
    assert(result[CONTENT] is not None)
    assert(result[RAINCONTENT] is not None)

    # check raindata:
    lines = result[RAINCONTENT].splitlines()

    for line in lines:
        (val, key) = line.split("|")

        try:
            # value must be a integer value:
            val = int(val)
        except ValueError:
            print("Unable to parse line: <%s>, not na integer." % (line))
            assert(False)

        try:
            datetime.strptime(key, '%H:%M')
        except ValueError:
            print("Unable to parse line: <%s>, not na time (HH:MM)." % (line))


def test_json_data():
    """Check json data elements."""
    result = get_data(usexml=False)

    # we must have content:
    assert(result[CONTENT] is not None)
    assert(result[RAINCONTENT] is not None)

    # check all elements we use from the xml:
    jsondata = json.loads(result[CONTENT])
    actueelweer = jsondata[__ACTUAL]
    assert(actueelweer is not None)

    weerstations = actueelweer[__STATIONMEASUREMENTS]
    assert(weerstations is not None)

    weerstation = weerstations[1]
    assert(weerstation[__LAT] is not None)
    assert(weerstation[__LON] is not None)

    assert(weerstation[__STATIONID] is not None)
    assert(weerstation[__STATIONNAME] is not None)
    assert(weerstation[SENSOR_TYPES[HUMIDITY][0]] is not None)
    assert(weerstation[SENSOR_TYPES[GROUNDTEMP][0]] is not None)
    assert(weerstation[SENSOR_TYPES[IRRADIANCE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[MEASURED][0]] is not None)
    assert(weerstation[SENSOR_TYPES[PRECIPITATION][0]] is not None)
    assert(weerstation[SENSOR_TYPES[PRESSURE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[STATIONNAME][0]] is not None)
    assert(weerstation[SENSOR_TYPES[CONDITION][0]] is not None)
    assert(weerstation[SENSOR_TYPES[TEMPERATURE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[VISIBILITY][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDSPEED][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDFORCE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDDIRECTION][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDAZIMUTH][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDGUST][0]] is not None)
    assert(weerstation[SENSOR_TYPES[RAINLAST24HOUR][0]] is not None)
    assert(weerstation[SENSOR_TYPES[RAINLASTHOUR][0]] is not None)
    assert(weerstation[SENSOR_TYPES[FEELTEMPERATURE][0]] is not None)


def test_precip_fc():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "000|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    expect = {'average': 0.0, 'total': 0.0, 'timeframe': 60}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc2():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    expect = {'average': 0.52, 'timeframe': 60, 'total': 0.52}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc3():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +                  # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    expect = {'average': 0.52, 'timeframe': 30, 'total': 0.26}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc4():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "077|%s\n" % (datetime.now() +              # noqa: ignore=W504
                              timedelta(minutes=n * 5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    expect = {'average': 0.1, 'timeframe': 30, 'total': 0.05}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc5():
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
    expect = {'total': 302.54, 'timeframe': 30, 'average': 605.09}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_decimal_values():
    """Test parsing precipitation forecast data containing decimal values."""
    def timeframe(minutes=0):
        return (datetime.now() + timedelta(minutes=minutes)).strftime("%H:%M")

    data = ""
    data += "10,10|%s\n" % timeframe(0)
    data += "100|%s\n" % timeframe(5)
    data += "192,456798213|%s\n" % timeframe(10)
    data += "55.55|%s\n" % timeframe(15)

    result = __parse_precipfc_data(data, 20)
    expect = {'total': 33.84, 'timeframe': 20, 'average': 135.36}

    # test calling results in the loop close cleanly
    assert (result == expect)


def test_parse_timeframe():
    """Test loading and parsing xml file."""
    data = None
    raindata = None

    latitude = 51.50
    longitude = 6.20
    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 4, usexml=False)
        # timeframe=4 should raise a ValueError, so:
        assert(False)
    except ValueError:
        # timeframe=4 should raise a ValueError, so:
        assert(True)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 5, usexml=False)
        # timeframe=5 should NOT raise a ValueError, so:
        assert(True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=5 should NOT raise a ValueError, so:
        assert(False)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 121, usexml=False)
        # timeframe=121 should raise a ValueError, so:
        assert(False)
    except ValueError:
        # timeframe=121 should raise a ValueError, so:
        assert(True)

    try:
        result = parse_data(data, raindata,
                            latitude, longitude, 120, usexml=False)
        # timeframe=120 should NOT raise a ValueError, so:
        assert(True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=120 should NOT raise a ValueError, so:
        assert(False)


def test_readdata1():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/json/buienradar.json', 'r')
    data = file.read()
    file.close()

    file = open('tests/raindata.txt', 'r')
    raindata = file.read()
    file.close()

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, raindata, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6391)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = datetime(year=2019, month=2, day=5, hour=0, minute=0)
    fc2 = datetime(year=2019, month=2, day=6, hour=0, minute=0)
    fc3 = datetime(year=2019, month=2, day=7, hour=0, minute=0)
    fc4 = datetime(year=2019, month=2, day=8, hour=0, minute=0)
    fc5 = datetime(year=2019, month=2, day=9, hour=0, minute=0)

    fc1 = pytz.timezone(__TIMEZONE).localize(fc1)
    fc2 = pytz.timezone(__TIMEZONE).localize(fc2)
    fc3 = pytz.timezone(__TIMEZONE).localize(fc3)
    fc4 = pytz.timezone(__TIMEZONE).localize(fc4)
    fc5 = pytz.timezone(__TIMEZONE).localize(fc5)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2019, 2, 4, hour=21, minute=0, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'success': True,
        'data': {
            'windgust': 9.73,
            'windforce': 4,
            'condition': {'condcode': 'c',
                          'exact_nl': 'Zwaar bewolkt',
                          'condition': 'cloudy',
                          'image': get_imageurl('cc'),
                          'detailed': 'cloudy',
                          'exact': 'Heavily clouded',
                          'night': True},
            'stationname': 'Arcen (6391)',
            'measured': measured,
            'barometerfc': 0,
            'barometerfcname': None,
            'barometerfcnamenl': None,
            'precipitation': 0.0,
            'groundtemperature': 3.0,
            'humidity': 70,
            'feeltemperature': -0.8,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded',
                                        'night': False},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'Z', 'windazimuth': 180,
                          'temperature': 6.0, 'windforce': 3, 'windspeed': 3.6,
                          'sunchance': 20, 'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10, 'maxtemp': 10.0,
                          'datetime': fc2},
                         {'snow': 0, 'rain': 5.5,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 6.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 3.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 8.0, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 20,
                          'maxtemp': 9.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False
                                        },
                          'mintemp': 3.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 5,
                          'windspeed': 8.23, 'sunchance': 20,
                          'maxtemp': 10.0, 'datetime': fc5}],
            'temperature': 3.6,
            'winddirection': 'ZW',
            'pressure': 0.0,
            'attribution': 'Data provided by buienradar.nl',
            'rainlast24hour': 0.0,
            'windspeed': 5.69,
            'precipitation_forecast': {'total': 0.0,
                                       'timeframe': 60,
                                       'average': 0.0},
            'rainlasthour': 0.0,
            'visibility': 0,
            'windazimuth': 215},
        'msg': None,
        'distance': 0.0
    }
    assert(expect == result)

    result = parse_data(data, raindata, latitude, longitude, 30, usexml=False)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6391)' in result[DATA][STATIONNAME])

    expect = {
        'success': True,
        'data': {
            'windgust': 9.73,
            'windforce': 4,
            'condition': {'condcode': 'c',
                          'exact_nl': 'Zwaar bewolkt',
                          'condition': 'cloudy',
                          'image': get_imageurl('cc'),
                          'detailed': 'cloudy',
                          'exact': 'Heavily clouded',
                          'night': True},
            'stationname': 'Arcen (6391)',
            'measured': measured,
            'barometerfc': 0,
            'barometerfcname': None,
            'barometerfcnamenl': None,
            'precipitation': 0.0,
            'groundtemperature': 3.0,
            'humidity': 70,
            'feeltemperature': -0.8,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded',
                                        'night': False},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'Z', 'windazimuth': 180,
                          'temperature': 6.0, 'windforce': 3,
                          'windspeed': 3.6, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 5.5,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 6.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 3.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 8.0, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 20,
                          'maxtemp': 9.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 5,
                          'windspeed': 8.23, 'sunchance': 20,
                          'maxtemp': 10.0, 'datetime': fc5}],
            'temperature': 3.6,
            'winddirection': 'ZW',
            'pressure': 0.0,
            'attribution': 'Data provided by buienradar.nl',
            'rainlast24hour': 0.0,
            'windspeed': 5.69,
            'precipitation_forecast': {'total': 0.0,
                                       'timeframe': 30,
                                       'average': 0.0},
            'rainlasthour': 0.0,
            'visibility': 0,
            'windazimuth': 215},
        'msg': None,
        'distance': 0.0
    }
    assert(expect == result)


def test_readdata2():
    """Test loading and parsing json file."""
    # load buienradar.json
    file = open('tests/json/buienradar.json', 'r')
    data = file.read()
    file.close()

    file = open('tests/raindata77.txt', 'r')
    raindata = file.read()
    file.close()

    # select non-first weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation De Bilt (6260)
    latitude = 52.11
    longitude = 5.19
    result = parse_data(data, raindata, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6260)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = datetime(year=2019, month=2, day=5, hour=0, minute=0)
    fc2 = datetime(year=2019, month=2, day=6, hour=0, minute=0)
    fc3 = datetime(year=2019, month=2, day=7, hour=0, minute=0)
    fc4 = datetime(year=2019, month=2, day=8, hour=0, minute=0)
    fc5 = datetime(year=2019, month=2, day=9, hour=0, minute=0)

    fc1 = pytz.timezone(__TIMEZONE).localize(fc1)
    fc2 = pytz.timezone(__TIMEZONE).localize(fc2)
    fc3 = pytz.timezone(__TIMEZONE).localize(fc3)
    fc4 = pytz.timezone(__TIMEZONE).localize(fc4)
    fc5 = pytz.timezone(__TIMEZONE).localize(fc5)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2019, 2, 4, hour=21, minute=0, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'success': True,
        'data': {
            'windgust': 10.95,
            'windforce': 4,
            'condition': {'condcode': 'q',
                          'exact_nl': 'Zwaar bewolkt en regen',
                          'condition': 'rainy',
                          'image': get_imageurl('qq'),
                          'detailed': 'rainy',
                          'exact': 'Heavily clouded with rain',
                          'night': True},
            'stationname': 'De Bilt (6260)',
            'measured': measured,
            'precipitation': 0.1,
            'groundtemperature': 2.7,
            'humidity': 96,
            'feeltemperature': -2.0,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded',
                                        'night': False},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'Z', 'windazimuth': 180,
                          'temperature': 6.0, 'windforce': 3,
                          'windspeed': 3.6, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 5.5,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 6.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 3.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 8.0, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 20,
                          'maxtemp': 9.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 5,
                          'windspeed': 8.23, 'sunchance': 20,
                          'maxtemp': 10.0, 'datetime': fc5}],
            'temperature': 2.9,
            'winddirection': 'ZZW',
            'pressure': 1022.14,
            'attribution': 'Data provided by buienradar.nl',
            'barometerfc': 6,
            'barometerfcname': 'Stable',
            'barometerfcnamenl': 'Mooi',
            'rainlast24hour': 2.5,
            'windspeed': 6.57,
            'precipitation_forecast': {'total': 0.1,
                                       'timeframe': 60,
                                       'average': 0.1},
            'rainlasthour': 0.2,
            'visibility': 4320,
            'windazimuth': 207},
        'msg': None,
        'distance': 1.306732
    }
    assert(expect == result)

    result = parse_data(data, raindata, latitude, longitude, 30, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6260)' in result[DATA][STATIONNAME])

    expect = {
        'success': True,
        'data': {
            'windgust': 10.95,
            'windforce': 4,
            'condition': {'condcode': 'q',
                          'exact_nl': 'Zwaar bewolkt en regen',
                          'condition': 'rainy',
                          'image': get_imageurl('qq'),
                          'detailed': 'rainy',
                          'exact': 'Heavily clouded with rain',
                          'night': True},
            'stationname': 'De Bilt (6260)',
            'measured': measured,
            'precipitation': 0.1,
            'groundtemperature': 2.7,
            'humidity': 96,
            'barometerfc': 6,
            'barometerfcname': 'Stable',
            'barometerfcnamenl': 'Mooi',
            'feeltemperature': -2.0,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded',
                                        'night': False},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'Z', 'windazimuth': 180,
                          'temperature': 6.0, 'windforce': 3,
                          'windspeed': 3.6, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 5.5,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 6.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 3.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 8.0, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 20,
                          'maxtemp': 9.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 5,
                          'windspeed': 8.23, 'sunchance': 20,
                          'maxtemp': 10.0, 'datetime': fc5}],
            'temperature': 2.9,
            'winddirection': 'ZZW',
            'pressure': 1022.14,
            'attribution': 'Data provided by buienradar.nl',
            'rainlast24hour': 2.5,
            'windspeed': 6.57,
            'precipitation_forecast': {'total': 0.05,
                                       'timeframe': 30,
                                       'average': 0.1},
            'rainlasthour': 0.2,
            'visibility': 4320,
            'windazimuth': 207},
        'msg': None,
        'distance': 1.306732
    }
    assert(expect == result)


def test_readdata3():
    """Test loading and parsing json file."""
    # load buienradar.json
    file = open('tests/json/buienradar.json', 'r')
    data = file.read()
    file.close()

    # select last weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation Zeeplatform K13 (6252)
    latitude = 53.23
    longitude = 3.23
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6252)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = datetime(year=2019, month=2, day=5, hour=0, minute=0)
    fc2 = datetime(year=2019, month=2, day=6, hour=0, minute=0)
    fc3 = datetime(year=2019, month=2, day=7, hour=0, minute=0)
    fc4 = datetime(year=2019, month=2, day=8, hour=0, minute=0)
    fc5 = datetime(year=2019, month=2, day=9, hour=0, minute=0)

    fc1 = pytz.timezone(__TIMEZONE).localize(fc1)
    fc2 = pytz.timezone(__TIMEZONE).localize(fc2)
    fc3 = pytz.timezone(__TIMEZONE).localize(fc3)
    fc4 = pytz.timezone(__TIMEZONE).localize(fc4)
    fc5 = pytz.timezone(__TIMEZONE).localize(fc5)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2019, 2, 4, hour=20, minute=50, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'success': True,
        'data': {
            'windgust': 10.35,
            'windforce': 4,
            'condition': {'condcode': 'c',
                          'exact_nl': 'Zwaar bewolkt',
                          'condition': 'cloudy',
                          'image': get_imageurl('cc'),
                          'detailed': 'cloudy',
                          'exact': 'Heavily clouded',
                          'night': True},
            'stationname': 'Zeeplatform K13 (6252)',
            'measured': measured,
            'precipitation': 0.0,
            'barometerfc': 5,
            'barometerfcname': 'Unstable',
            'barometerfcnamenl': 'Veranderlijk',
            'groundtemperature': 0.0,
            'humidity': 0,
            'feeltemperature': 0.0,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded',
                                        'night': False},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'Z', 'windazimuth': 180,
                          'temperature': 6.0, 'windforce': 3,
                          'windspeed': 3.6, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 5.5,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 6.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 10,
                          'maxtemp': 10.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 3.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 8.0, 'windforce': 4,
                          'windspeed': 5.66, 'sunchance': 20,
                          'maxtemp': 9.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain',
                                        'night': False},
                          'mintemp': 3.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'ZW', 'windazimuth': 225,
                          'temperature': 9.5, 'windforce': 5,
                          'windspeed': 8.23, 'sunchance': 20,
                          'maxtemp': 10.0, 'datetime': fc5}],
            'temperature': 0.0,
            'winddirection': 'WNW',
            'pressure': 1018.36,
            'attribution': 'Data provided by buienradar.nl',
            'rainlast24hour': 0.0,
            'windspeed': 7.94,
            'precipitation_forecast': None,
            'rainlasthour': 0.0,
            'visibility': 0,
            'windazimuth': 286},
        'msg': None,
        'distance': 1.297928
    }
    assert(expect == result)


def test_nojson():
    """Test loading and parsing invalid json file."""
    # load nojson_file
    file = open('tests/json/buienradar_nojson.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and                    # noqa: ignore=W504
            result[MESSAGE] == 'Unable to parse content as json.')


def test_nows():
    """Test loading and parsing invalid json file; no weatherstation."""
    file = open('tests/json/buienradar_nows.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and                    # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/json/buienradar_nows2.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and                    # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/json/buienradar_nows3.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and                    # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')

    file = open('tests/json/buienradar_nows5.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and                    # noqa: ignore=W504
            result[MESSAGE] == 'No location selected.')


def test_wsdistancen_with_none():
    """Test distance function without valid input."""
    latitude = 51.50
    longitude = 6.20
    distance = __get_ws_distance(None, latitude, longitude)
    print(distance)
    assert (distance is None)


def test_nofc():
    """Test loading and parsing invalid json file: no forecast data."""
    file = open('tests/json/buienradar_nofc.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == 'Unable to extract forecast data.')


def test_nofc2():
    """Test loading and parsing invalid json file; no forecast."""
    file = open('tests/json/buienradar_nofc2.json', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None, usexml=False)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            len(result[DATA][FORECAST]) == 0)


def test_missing_data():
    """Test loading and parsing invalid json file; missing data fields."""
    file = open('tests/json/buienradar_missing.json', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: stationname "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][STATIONNAME] == None)

    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: feeltemperature "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][FEELTEMPERATURE] == None
            )

    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: humidity "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][HUMIDITY] == None
            )

    latitude = 52.10
    longitude = 5.18
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: groundtemperature "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][GROUNDTEMP] == None
            )

    latitude = 52.92
    longitude = 4.78
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: temperature "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][TEMPERATURE] == None
            )

    latitude = 51.45
    longitude = 5.42
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: windspeed "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][WINDSPEED] == None
            )

    latitude = 51.20
    longitude = 5.77
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: windspeedBft "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][WINDFORCE] == None
            )

    latitude = 52.00
    longitude = 3.28
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: winddirectiondegrees "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == None and
            result[DATA][WINDAZIMUTH] == None
            )

    latitude = 51.57
    longitude = 4.93
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: winddirection "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] is None and
            result[DATA][WINDDIRECTION] == None
            )

    latitude = 52.07
    longitude = 6.65
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)

    # expectedmsg = "Missing key(s) in br data: "
    assert (result[SUCCESS] and
            result[MESSAGE] is None and
            result[DATA][PRESSURE] is None
            )

    latitude = 52.43
    longitude = 6.27
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: windgusts "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] is None and
            result[DATA][WINDGUST] is None
            )

    latitude = 51.87
    longitude = 5.15
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: precipitation "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] is None and
            result[DATA][PRECIPITATION] is None
            )

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    # "Missing key(s) in br data: sunpower "
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] is None and
            result[DATA][IRRADIANCE] is None
            )


def test_invalid_data():
    """Test loading and parsing json file with data that cannot be parsed."""
    file = open('tests/json/buienradar_invalid.json', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] is False)
    assert(result[MESSAGE] == 'Location data is invalid.')

    file = open('tests/json/buienradar_invalidfc1.json', 'r')
    data = file.read()
    file.close()

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           result[MESSAGE] is None)
    # test Temperature (average):
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][0][TEMPERATURE] == 6.5)
    # test missing maxtemperatureMin:
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][1][TEMPERATURE] == 10)
    # test missing maxtemperatureMax:
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][2][TEMPERATURE] == 9)
    # test missing maxtemperatureMin and maxtemperatureMax:
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][3][TEMPERATURE] is None)

    # read xml with invalid ws coordinates
    file = open('tests/json/buienradar_invalidws1.json', 'r')
    data = file.read()
    file.close()

    # 'Meetstation Arcen' contains invalid gps info,
    # 'Meetstation Volkel' will be selected as alternative
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6375)' in result[DATA][STATIONNAME])

    # 'Meetstation Arnhem' contains invalid gps info,
    # 'Meetstation De Bilt' will be selected as alternative
    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6260)' in result[DATA][STATIONNAME])

    # 'Meetstation Berkhout' contains invalid gps info,
    # 'Meetstation Wijdenes' will be selected as alternative
    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert(result[SUCCESS] and                              # noqa: ignore=W504
           '(6248)' in result[DATA][STATIONNAME])


def test__get_str():
    """Test get_str function."""
    section = {"key1": "value", "key2": "", "key3": None}
    value = __get_str(section, "key1")
    assert(value == "value")

    value = __get_str(section, "key2")
    assert(value == "")

    value = __get_str(section, "key3")
    assert(value is None)


def test__get_windspeed():
    """Test __get_windspeed function."""
    speeds = {0: 0.25, 1: 0.51, 2: 2.06, 3: 3.6, 4: 5.66,
              5: 8.23, 6: 11.32, 7: 14.4, 8: 17.49, 9: 21.09,
              10: 24.69, 11: 28.81, 12: 32.41, 13: None, -1: None, None: None}
    for k, expected in speeds.items():
        value = __get_windspeed(k)
        assert(value == expected)


def test__get_windazimuth():
    """Test __get_windazimuth function."""
    tests = {'n': 0, 'nno': 22.5, 'no': 45, 'ono': 67.5, 'o': 90,
             'ozo': 112.5, 'zo': 135, 'zzo': 157.5, 'z': 180,
             'zzw': 202.5, 'zw': 225, 'wzw': 247.5, 'w': 270,
             'wnw': 292.5, 'nw': 315, 'nnw': 237.5,
             'nne': 22.5, 'ne': 45, 'ene': 67.5, 'e': 90,
             'ese': 112.5, 'se': 135, 'sse': 157.5, 's': 180,
             'ssw': 202.5, 'sw': 225, 'wsw': 247.5,
             'N': 0, 'NNO': 22.5, 'NO': 45, 'ONO': 67.5, 'O': 90,
             'OZO': 112.5, 'ZO': 135, 'ZZO': 157.5, 'Z': 180,
             'ZZW': 202.5, 'ZW': 225, 'WZW': 247.5, 'W': 270,
             'WNW': 292.5, 'NW': 315, 'NNW': 237.5,
             'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90,
             'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
             'SSW': 202.5, 'SW': 225, 'WSW': 247.5}
    for k, expected in tests.items():
        value = __get_windazimuth(k)
        assert(value == expected)


def test__get_float():
    """Test get_float function."""
    section = {"key1": 1.2, "key2": 0.0, "key3": None}
    value = __get_float(section, "key1")
    assert(value == 1.2)

    value = __get_float(section, "key2")
    assert(value == 0.0)

    value = __get_float(section, "key3")
    assert(value == 0.0)


def test__get_int():
    """Test get_int function."""
    section = {"key1": 1.2, "key2": 0.0, "key3": None,
               "key4": 3, "key5": 1.9, "key6": -1}
    value = __get_int(section, "key1")
    assert(value == 1)

    value = __get_int(section, "key2")
    assert(value == 0)

    value = __get_int(section, "key3")
    assert(value == 0)

    value = __get_int(section, "key4")
    assert(value == 3)

    value = __get_int(section, "key5")
    assert(value == 1)

    value = __get_int(section, "key6")
    assert(value == -1)


def test__getstr():
    """Test get_str function."""
    value = __get_str(None, "test")
    assert(value == "")


def test__getBarFC():
    """Test __getBarFCName function."""
    tests = {None: 0, 'X': 1,
             0: 1,
             500: 1,
             973: 1,
             974: 2,
             981: 2,
             989: 2,
             990: 3,
             995: 3,
             1001: 3,
             1002: 4,
             1007: 4,
             1009: 4,
             1010: 5,
             1019: 5,
             1021: 5,
             1022: 6,
             1029: 6,
             1034: 6,
             1035: 7,
             1111: 7,
             9999: 7}
    for k, expected in tests.items():
        value = __getBarFC(k)
        assert(value == expected)


def test__getBarFCName():
    """Test __getBarFCName function."""
    tests = {None: None,
             0: 'Thunderstorms',
             500: 'Thunderstorms',
             973: 'Thunderstorms',
             974: 'Stormy',
             981: 'Stormy',
             989: 'Stormy',
             990: 'Rain',
             995: 'Rain',
             1001: 'Rain',
             1002: 'Cloudy',
             1007: 'Cloudy',
             1009: 'Cloudy',
             1010: 'Unstable',
             1019: 'Unstable',
             1021: 'Unstable',
             1022: 'Stable',
             1029: 'Stable',
             1034: 'Stable',
             1035: 'Very dry',
             1111: 'Very dry',
             9999: 'Very dry'}

    for k, expected in tests.items():
        value = __getBarFCName(k)
        assert(value == expected)


def test__getBarFCNameNL():
    """Test __getBarFCNameNL function."""
    tests = {None: None,
             0: 'Zware storm',
             500: 'Zware storm',
             973: 'Zware storm',
             974: 'Storm',
             981: 'Storm',
             989: 'Storm',
             990: 'Regen en wind',
             996: 'Regen en wind',
             1001: 'Regen en wind',
             1002: 'Bewolkt',
             1006: 'Bewolkt',
             1009: 'Bewolkt',
             1010: 'Veranderlijk',
             1016: 'Veranderlijk',
             1021: 'Veranderlijk',
             1022: 'Mooi',
             1029: 'Mooi',
             1034: 'Mooi',
             1035: 'Zeer mooi',
             1100: 'Zeer mooi',
             9999: 'Zeer mooi'}

    for k, expected in tests.items():
        value = __getBarFCNameNL(k)
        assert(value == expected)
