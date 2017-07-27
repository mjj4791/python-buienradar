"""testing xml parsing."""
from datetime import datetime, timedelta

import pytz
import xmltodict

from buienradar.buienradar import (
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
    SENSOR_TYPES,
    STATIONNAME,
    SUCCESS,
    SYMBOL,
    TEMPERATURE,
    VISIBILITY,
    WINDAZIMUTH,
    WINDDIRECTION,
    WINDFORCE,
    WINDGUST,
    WINDSPEED,
    __get_ws_distance,
    __parse_precipfc_data,
    get_data,
    parse_data,
    to_localdatetime
)

__TIMEZONE = 'Europe/Amsterdam'
__DATE_FORMAT = '%m/%d/%Y %H:%M:%S'


def get_imageurl():
    """Get the image url helper function."""
    result = 'https://www.buienradar.nl/'
    result += 'resources/images/icons/weather/30x30/cc.png'
    return result


def test_to_localdatetime():
    """Check he workign of the to_localdatetime function."""
    # check invalid dates:
    dt = to_localdatetime('')
    assert(dt is None)

    dt = to_localdatetime(None)
    assert(dt is None)

    dt = to_localdatetime('01/02/2017 03:04:05')
    assert(("%s" % dt) == '2017-01-02 03:04:05+01:00')

    # (invalid) month:
    dt = to_localdatetime('00/02/2017 03:04:05')
    assert(dt is None)

    dt = to_localdatetime('12/02/2017 03:04:05')
    assert(("%s" % dt) == '2017-12-02 03:04:05+01:00')

    dt = to_localdatetime('13/02/2017 03:04:05')
    assert(dt is None)

    # (invalid) day:
    dt = to_localdatetime('01/00/2017 03:04:05')
    assert(dt is None)

    dt = to_localdatetime('01/31/2017 03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = to_localdatetime('01/32/2017 03:04:05')
    assert(dt is None)

    dt = to_localdatetime('02/28/2017 03:04:05')
    assert(("%s" % dt) == '2017-02-28 03:04:05+01:00')

    dt = to_localdatetime('02/29/2017 03:04:05')
    assert(dt is None)

    # (invalid) year:
    dt = to_localdatetime('01/01/17 03:04:05')
    assert(dt is None)

    dt = to_localdatetime('01/1/017 03:04:05')
    assert(dt is None)

    # (invalid) hour:
    dt = to_localdatetime('01/31/2017 00:04:05')
    assert(("%s" % dt) == '2017-01-31 00:04:05+01:00')

    dt = to_localdatetime('01/31/2017 03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = to_localdatetime('01/31/2017 23:04:05')
    assert(("%s" % dt) == '2017-01-31 23:04:05+01:00')

    dt = to_localdatetime('01/1/2017 24:04:05')
    assert(dt is None)

    dt = to_localdatetime('01/1/2017 25:04:05')
    assert(dt is None)

    dt = to_localdatetime('01/1/2017 01:04:05 PM')
    assert(dt is None)

    dt = to_localdatetime('01/1/2017 01:04:05 AM')
    assert(dt is None)

    # (invalid) minute:
    dt = to_localdatetime('01/31/2017 03:00:05')
    assert(("%s" % dt) == '2017-01-31 03:00:05+01:00')

    dt = to_localdatetime('01/31/2017 03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    dt = to_localdatetime('01/31/2017 03:59:05')
    assert(("%s" % dt) == '2017-01-31 03:59:05+01:00')

    dt = to_localdatetime('01/01/2017 03:60:05')
    assert(dt is None)

    dt = to_localdatetime('01/1/2017 25:-4:05')
    assert(dt is None)

    # (invalid) second:
    dt = to_localdatetime('01/31/2017 03:04:00')
    assert(("%s" % dt) == '2017-01-31 03:04:00+01:00')

    dt = to_localdatetime('01/31/2017 03:04:01')
    assert(("%s" % dt) == '2017-01-31 03:04:01+01:00')

    dt = to_localdatetime('01/31/2017 03:04:59')
    assert(("%s" % dt) == '2017-01-31 03:04:59+01:00')

    dt = to_localdatetime('01/1/2017 24:04:60')
    assert(dt is None)

    dt = to_localdatetime('01/1/2017 25:04:-5')
    assert(dt is None)

    dt = to_localdatetime('01/31/2017 03:04:05')
    assert(("%s" % dt) == '2017-01-31 03:04:05+01:00')

    # check DST/tz offset:
    dt = to_localdatetime('01/02/2017 01:02:03')
    assert(("%s" % dt) == '2017-01-02 01:02:03+01:00')

    dt = to_localdatetime('02/28/2017 13:31:11')
    assert(("%s" % dt) == '2017-02-28 13:31:11+01:00')

    dt = to_localdatetime('12/31/2017 13:31:11')
    assert(("%s" % dt) == '2017-12-31 13:31:11+01:00')

    dt = to_localdatetime('07/10/2017 13:31:11')
    assert(("%s" % dt) == '2017-07-10 13:31:11+02:00')


def test_rain_data():
    """Test format of retrieved rain data."""
    result = get_data()

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
            print("Uunable to parse line: <%s>, not na integer." % (line))
            assert(False)

        try:
            datetime.strptime(key, '%H:%M')
        except ValueError:
            print("Unable to parse line: <%s>, not na time (HH:MM)." % (line))


def test_xml_data():
    """Check xml data elements/xsd."""
    result = get_data()

    # we must have content:
    assert(result[CONTENT] is not None)
    assert(result[RAINCONTENT] is not None)

    # check all elements we use from the xml:
    xmldata = xmltodict.parse(result[CONTENT])[__BRROOT]
    weergegevens = xmldata[__BRWEERGEGEVENS]
    assert(weergegevens is not None)

    actueelweer = weergegevens[__BRACTUEELWEER]
    assert(actueelweer is not None)

    weerstations = actueelweer[__BRWEERSTATIONS]
    assert(weerstations is not None)

    weerstation = weerstations[__BRWEERSTATION]
    assert(weerstation is not None)

    weerstation = weerstation[1]
    assert(weerstation[__BRLAT] is not None)
    assert(weerstation[__BRLON] is not None)

    assert(weerstation[__BRSTATIONCODE] is not None)
    assert(weerstation[__BRSTATIONNAAM] is not None)
    assert(weerstation[__BRSTATIONNAAM][__BRTEXT] is not None)
    assert(weerstation[SENSOR_TYPES[HUMIDITY][0]] is not None)
    assert(weerstation[SENSOR_TYPES[GROUNDTEMP][0]] is not None)
    assert(weerstation[SENSOR_TYPES[IRRADIANCE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[MEASURED][0]] is not None)
    assert(weerstation[SENSOR_TYPES[PRECIPITATION][0]] is not None)
    assert(weerstation[SENSOR_TYPES[PRESSURE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[STATIONNAME][0]] is not None)
    assert(weerstation[SENSOR_TYPES[SYMBOL][0]] is not None)
    assert(weerstation[SENSOR_TYPES[SYMBOL][0]][__BRZIN] is not None)
    assert(weerstation[SENSOR_TYPES[SYMBOL][0]][__BRTEXT] is not None)
    assert(weerstation[SENSOR_TYPES[TEMPERATURE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[VISIBILITY][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDSPEED][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDFORCE][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDDIRECTION][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDAZIMUTH][0]] is not None)
    assert(weerstation[SENSOR_TYPES[WINDGUST][0]] is not None)


def test_precip_fc():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "000|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    expect = {'average': 0.0, 'total': 0.0, 'timeframe': 60}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc2():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 60)
    expect = {'average': 0.52, 'timeframe': 60, 'total': 0.52}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc3():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    expect = {'average': 0.52, 'timeframe': 30, 'total': 0.26}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc4():
    """Test parsing precipitation forecast data."""
    data = ""
    for n in range(0, 24):
        data += "077|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 30)
    expect = {'average': 0.1, 'timeframe': 30, 'total': 0.05}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc5():
    """Test parsing precipitation forecast data."""
    data = ""
    data += "000|%s\n" % (datetime.now() +
                          timedelta(minutes=0)).strftime("%H:%M")
    data += "217|%s\n" % (datetime.now() +
                          timedelta(minutes=5)).strftime("%H:%M")
    data += "208|%s\n" % (datetime.now() +
                          timedelta(minutes=15)).strftime("%H:%M")
    data += "145|%s\n" % (datetime.now() +
                          timedelta(minutes=20)).strftime("%H:%M")
    data += "131|%s\n" % (datetime.now() +
                          timedelta(minutes=25)).strftime("%H:%M")
    data += "00|%s\n" % (datetime.now() +
                         timedelta(minutes=30)).strftime("%H:%M")
    data += "00|%s\n" % (datetime.now() +
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
        result = parse_data(data, raindata, latitude, longitude, 4)
        # timeframe=4 should raise a ValueError, so:
        assert(False)
    except ValueError:
        # timeframe=4 should raise a ValueError, so:
        assert(True)

    try:
        result = parse_data(data, raindata, latitude, longitude, 5)
        # timeframe=5 should NOT raise a ValueError, so:
        assert(True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=5 should NOT raise a ValueError, so:
        assert(False)

    try:
        result = parse_data(data, raindata, latitude, longitude, 121)
        # timeframe=121 should raise a ValueError, so:
        assert(False)
    except ValueError:
        # timeframe=121 should raise a ValueError, so:
        assert(True)

    try:
        result = parse_data(data, raindata, latitude, longitude, 120)
        # timeframe=120 should NOT raise a ValueError, so:
        assert(True and result[SUCCESS] is False)
    except ValueError:
        # timeframe=120 should NOT raise a ValueError, so:
        assert(False)


def test_readdata1():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
    data = file.read()
    file.close()

    file = open('tests/raindata.txt', 'r')
    raindata = file.read()
    file.close()

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, raindata, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6391)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=1))
    fc2 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=2))
    fc3 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=3))
    fc4 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=4))
    fc5 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=5))

    fc1 = fc1.replace(hour=12, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=12, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=12, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=12, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=12, minute=0, second=0, microsecond=0)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2017, 5, 19, hour=0, minute=20, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'data': {
            'windgust': 4.4,
            'windspeed': 3.13,
            'temperature': 16.3,
            'stationname': 'Arcen (6391)',
            'windazimuth': 77,
            'symbol': 'Zwaar bewolkt',
            'windforce': 2,
            'pressure': 1021.23,
            'winddirection': 'ONO',
            'humidity': 95,
            'image': get_imageurl(),
            'attribution': 'Data provided by buienradar.nl',
            'groundtemperature': 15.9,
            'precipitation': 2.0,
            'precipitation_forecast': {'average': 0.0,
                                       'timeframe': 60,
                                       'total': 0.0},
            'measured': measured,
            'irradiance': 614,
            'visibility': 38400,
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': 0,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': 0,
                 'rain': 4.4, 'windforce': 4}
                ],
            },
        'success': True,
        'msg': None,
        'distance': 0.0
    }
    assert(expect == result)

    result = parse_data(data, raindata, latitude, longitude, 30)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6391)' in result[DATA][STATIONNAME])

    expect = {
        'data': {
            'windgust': 4.4,
            'windspeed': 3.13,
            'temperature': 16.3,
            'stationname': 'Arcen (6391)',
            'windazimuth': 77,
            'symbol': 'Zwaar bewolkt',
            'windforce': 2,
            'pressure': 1021.23,
            'winddirection': 'ONO',
            'humidity': 95,
            'image': get_imageurl(),
            'attribution': 'Data provided by buienradar.nl',
            'groundtemperature': 15.9,
            'precipitation': 2,
            'precipitation_forecast': {'average': 0.0,
                                       'timeframe': 30,
                                       'total': 0.0},
            'measured': measured,
            'irradiance': 614,
            'visibility': 38400,
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': 0,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': 0,
                 'rain': 4.4, 'windforce': 4}
                ],
            },
        'success': True,
        'msg': None,
        'distance': 0.0
    }
    assert(expect == result)


def test_readdata2():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
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
    result = parse_data(data, raindata, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6260)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=1))
    fc2 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=2))
    fc3 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=3))
    fc4 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=4))
    fc5 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=5))

    fc1 = fc1.replace(hour=12, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=12, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=12, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=12, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=12, minute=0, second=0, microsecond=0)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2017, 5, 19, hour=0, minute=20, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'data': {
            'humidity': 88,
            'windforce': 3,
            'windgust': 6.4,
            'windspeed': 4.64,
            'winddirection': 'ONO',
            'visibility': 14800,
            'attribution': 'Data provided by buienradar.nl',
            'symbol': 'Zwaar bewolkt',
            'temperature': 16.0,
            'measured': measured,
            'groundtemperature': 15.4,
            'pressure': 1008.72,
            'image': get_imageurl(),
            'stationname': 'De Bilt (6260)',
            'precipitation': 0.0,
            'precipitation_forecast':  {'average': 0.1,
                                        'timeframe': 60,
                                        'total': 0.1},
            'windazimuth': 72,
            'irradiance': 0,
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': 0,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': 0,
                 'rain': 4.4, 'windforce': 4}
            ],
        },
        'success': True,
        'distance': 1.306732,
        'msg': None}
    assert(expect == result)

    result = parse_data(data, raindata, latitude, longitude, 30)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6260)' in result[DATA][STATIONNAME])

    expect = {
        'data': {
            'humidity': 88,
            'windforce': 3,
            'windgust': 6.4,
            'windspeed': 4.64,
            'winddirection': 'ONO',
            'visibility': 14800,
            'attribution': 'Data provided by buienradar.nl',
            'symbol': 'Zwaar bewolkt',
            'temperature': 16.0,
            'measured': measured,
            'groundtemperature': 15.4,
            'pressure': 1008.72,
            'image': get_imageurl(),
            'stationname': 'De Bilt (6260)',
            'precipitation': 0.0,
            'precipitation_forecast':  {'average': 0.1,
                                        'timeframe': 30,
                                        'total': 0.05},
            'windazimuth': 72,
            'irradiance': 0,
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': 0.0, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': 0,
                 'rain': 0.0, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': 0,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': 0,
                 'rain': 4.4, 'windforce': 4}
            ],
        },
        'success': True,
        'distance': 1.306732,
        'msg': None}
    assert(expect == result)


def test_readdata3():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
    data = file.read()
    file.close()

    # select last weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation Zeeplatform K13 (6252)
    latitude = 53.23
    longitude = 3.23
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6252)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=1))
    fc2 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=2))
    fc3 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=3))
    fc4 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=4))
    fc5 = (datetime.now(pytz.timezone(__TIMEZONE)) + timedelta(days=5))

    fc1 = fc1.replace(hour=12, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=12, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=12, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=12, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=12, minute=0, second=0, microsecond=0)

    # '05/19/2017 00:20:00'
    loc_dt = datetime(2017, 5, 19, hour=0, minute=20, second=0, microsecond=0)
    measured = pytz.timezone(__TIMEZONE).localize(loc_dt)

    # Expected result:
    expect = {
        'msg': None,
        'success': True,
        'distance': 1.297928,
        'data': {
            'attribution': 'Data provided by buienradar.nl',
            'windspeed': 8.16,
            'windazimuth': 59,
            'groundtemperature': 0.0,
            'windforce': 5,
            'precipitation': 0.0,
            'precipitation_forecast': None,
            'humidity': 47,
            'pressure': 1004.95,
            'symbol': 'Zwaar bewolkt',
            'measured': measured,
            'winddirection': 'O',
            'stationname': 'Zeeplatform K13 (6252)',
            'temperature': 16.8,
            'visibility': 6200,
            'irradiance': 614,
            'windgust': 14.0,
            'image': get_imageurl(),
            'forecast': [
                    {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                     'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': 0,
                     'rain': 0.0, 'windforce': 3},
                    {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                     'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                     'rain': 0.0, 'windforce': 3},
                    {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                     'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': 0,
                     'rain': 0.0, 'windforce': 4},
                    {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                     'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': 0,
                     'rain': 1.8, 'windforce': 4},
                    {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                     'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': 0,
                     'rain': 4.4, 'windforce': 4}
                ]
            },
        }
    assert(expect == result)


def test_noxml():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noxml.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_noroot():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noroot.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_nows():
    """Test loading and parsing invalid xml file; no weatherstation."""
    file = open('tests/buienradar_nows.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows2.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows3.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows4.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows5.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')


def test_wsdistancen_with_none():
    """Test distance function without valid input."""
    latitude = 51.50
    longitude = 6.20
    distance = __get_ws_distance(None, latitude, longitude)
    print(distance)
    assert (distance is None)


def test_nofc():
    """Test loading and parsing invalid xml file: no forecast data."""
    file = open('tests/buienradar_nofc.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == 'Unable to extract forecast data.')


def test_nofc2():
    """Test loading and parsing invalid xml file; no forecast."""
    file = open('tests/buienradar_nofc2.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data, None)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and
            len(result[DATA][FORECAST]) == 0)


def test_missing_data():
    """Test loading and parsing invalid xml file; missing data fields."""
    file = open('tests/buienradar_missing.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: stationnaam ")

    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: icoonactueel ")

    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: luchtvochtigheid ")

    latitude = 52.10
    longitude = 5.18
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: temperatuurGC ")

    latitude = 52.92
    longitude = 4.78
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: temperatuur10cm ")

    latitude = 51.45
    longitude = 5.42
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidMS ")

    latitude = 51.20
    longitude = 5.77
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidBF ")

    latitude = 52.00
    longitude = 3.28
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windrichtingGR ")

    latitude = 51.57
    longitude = 4.93
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windrichting ")

    latitude = 52.07
    longitude = 6.65
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: luchtdruk ")

    latitude = 52.43
    longitude = 6.27
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windstotenMS ")

    latitude = 51.87
    longitude = 5.15
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: regenMMPU ")

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: zonintensiteitWM2 ")


def test_invalid_data():
    """Test loading and parsing xml file with data that cannot be parsed."""
    file = open('tests/buienradar_invalid.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] is False)
    assert(result[MESSAGE] == 'Location data is invalid.')

    file = open('tests/buienradar_invalidfc1.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)
    # test missing maxtemp:
    assert(len(result[DATA][FORECAST]) == 5 and
           result[DATA][FORECAST][0][TEMPERATURE] == 0.0)
    # test missing maxgtemp and maxtempmax:
    assert(len(result[DATA][FORECAST]) == 5 and
           result[DATA][FORECAST][2][TEMPERATURE] == 0.0)

    # read xml with invalid ws coordinates
    file = open('tests/buienradar_invalidws1.xml', 'r')
    data = file.read()
    file.close()

    # 'Meetstation Arcen' contains invalid gps info,
    # 'Meetstation Volkel' will be selected as alternative
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6375)' in result[DATA][STATIONNAME])

    # 'Meetstation Arnhem' contains invalid gps info,
    # 'Meetstation De Bilt' will be selected as alternative
    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6260)' in result[DATA][STATIONNAME])

    # 'Meetstation Berkhout' contains invalid gps info,
    # 'Meetstation Wijdenes' will be selected as alternative
    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, None, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6248)' in result[DATA][STATIONNAME])
