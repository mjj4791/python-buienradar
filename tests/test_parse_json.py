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
    __get_ws_distance,
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
                          'exact': 'Heavily clouded'},
            'stationname': 'Arcen (6391)',
            'measured': measured,
            'barometerfc': 0,
            'barometerfcname': None,
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
                                        'exact': 'Heavily clouded'},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'z', 'temperature': 6.0,
                          'windforce': 3, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 11.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 7.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 5, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc5}],
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
                          'exact': 'Heavily clouded'},
            'stationname': 'Arcen (6391)',
            'measured': measured,
            'barometerfc': 0,
            'barometerfcname': None,
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
                                        'exact': 'Heavily clouded'},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'z', 'temperature': 6.0,
                          'windforce': 3, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 11.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 7.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 5, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc5}],
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
                          'exact': 'Heavily clouded with rain'},
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
                                        'exact': 'Heavily clouded'},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'z', 'temperature': 6.0,
                          'windforce': 3, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 11.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 7.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 5, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc5}],
            'temperature': 2.9,
            'winddirection': 'ZZW',
            'pressure': 1022.14,
            'attribution': 'Data provided by buienradar.nl',
            'barometerfc': 6,
            'barometerfcname': 'Stable',
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
                          'exact': 'Heavily clouded with rain'},
            'stationname': 'De Bilt (6260)',
            'measured': measured,
            'precipitation': 0.1,
            'groundtemperature': 2.7,
            'humidity': 96,
            'barometerfc': 6,
            'barometerfcname': 'Stable',
            'feeltemperature': -2.0,
            'irradiance': 0,
            'forecast': [{'snow': 0, 'rain': 0.0,
                          'condition': {'condcode': 'c',
                                        'exact_nl': 'Zwaar bewolkt',
                                        'condition': 'cloudy',
                                        'image': get_imageurl('c'),
                                        'detailed': 'cloudy',
                                        'exact': 'Heavily clouded'},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'z', 'temperature': 6.0,
                          'windforce': 3, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 11.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 7.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 5, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc5}],
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
                          'exact': 'Heavily clouded'},
            'stationname': 'Zeeplatform K13 (6252)',
            'measured': measured,
            'precipitation': 0.0,
            'barometerfc': 5,
            'barometerfcname': 'Unstable',
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
                                        'exact': 'Heavily clouded'},
                          'mintemp': 2.0, 'rainchance': 20,
                          'minrain': 0.0, 'maxrain': 0.0,
                          'winddirection': 'z', 'temperature': 6.0,
                          'windforce': 3, 'sunchance': 20,
                          'maxtemp': 6.0, 'datetime': fc1},
                         {'snow': 0, 'rain': 11.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 5.0, 'maxrain': 11.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc2},
                         {'snow': 0, 'rain': 8.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 90,
                          'minrain': 3.0, 'maxrain': 8.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 10,
                          'maxtemp': 0.0, 'datetime': fc3},
                         {'snow': 0, 'rain': 5.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 70,
                          'minrain': 1.0, 'maxrain': 5.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 4, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc4},
                         {'snow': 0, 'rain': 7.0,
                          'condition': {'condcode': 'q',
                                        'exact_nl': 'Zwaar bewolkt en regen',
                                        'condition': 'rainy',
                                        'image': get_imageurl('q'),
                                        'detailed': 'rainy',
                                        'exact': 'Heavily clouded with rain'},
                          'mintemp': 0.0, 'rainchance': 80,
                          'minrain': 3.0, 'maxrain': 7.0,
                          'winddirection': 'zw', 'temperature': 0.0,
                          'windforce': 5, 'sunchance': 20,
                          'maxtemp': 0.0, 'datetime': fc5}],
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
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: stationname ")

    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: feeltemperature ")

    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: humidity ")

    latitude = 52.10
    longitude = 5.18
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: groundtemperature ")

    latitude = 52.92
    longitude = 4.78
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: temperature ")

    latitude = 51.45
    longitude = 5.42
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windspeed ")

    latitude = 51.20
    longitude = 5.77
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windspeedBft ")

    latitude = 52.00
    longitude = 3.28
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] ==                              # noqa: ignore=W504
            "Missing key(s) in br data: winddirectiondegrees ")

    latitude = 51.57
    longitude = 4.93
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: winddirection ")

    latitude = 52.07
    longitude = 6.65
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)

    expectedmsg = "Missing key(s) in br data: "
    expectedmsg += "airpressure airpressure airpressure "
    assert (result[SUCCESS])
    assert (result[MESSAGE] == expectedmsg)

    latitude = 52.43
    longitude = 6.27
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: windgusts ")

    latitude = 51.87
    longitude = 5.15
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: precipitation ")

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude, usexml=False)
    print(result)
    assert (result[SUCCESS] and                             # noqa: ignore=W504
            result[MESSAGE] == "Missing key(s) in br data: sunpower ")


def test_invalid_data():
    """Test loading and parsing xml file with data that cannot be parsed."""
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
    # test missing maxtemp:
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][0][TEMPERATURE] == 0.0)
    # test missing maxgtemp and maxtempmax:
    assert(len(result[DATA][FORECAST]) == 5 and             # noqa: ignore=W504
           result[DATA][FORECAST][2][TEMPERATURE] == 0.0)

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
